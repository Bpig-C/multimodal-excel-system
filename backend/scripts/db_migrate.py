"""
数据库迁移管理工具
支持版本化的数据库迁移
"""
import os
import sys
import json
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Settings

class DatabaseMigrator:
    """数据库迁移管理器"""
    
    def __init__(self):
        self.settings = Settings()
        self.db_path = self.settings.DATABASE_URL.replace('sqlite:///', '')
        self.migrations_dir = Path(__file__).parent.parent / 'migrations'
        self.versions_file = self.migrations_dir / 'versions.json'
        
    def get_db_connection(self):
        """获取数据库连接"""
        if not os.path.exists(self.db_path):
            print(f"⚠️  数据库文件不存在: {self.db_path}")
            print("   将在首次迁移时创建")
        return sqlite3.connect(self.db_path)
    
    def get_current_version(self):
        """获取当前数据库版本"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # 尝试从 schema_version 表读取
            cursor.execute("""
                SELECT version FROM schema_version 
                ORDER BY applied_at DESC LIMIT 1
            """)
            result = cursor.fetchone()
            if result:
                return result[0]
        except sqlite3.OperationalError:
            # 表不存在，返回0
            pass
        finally:
            conn.close()
        
        return 0
    
    def set_version(self, version, description=""):
        """设置数据库版本"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # 创建版本表（如果不存在）
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version INTEGER NOT NULL,
                    description TEXT,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 插入版本记录
            cursor.execute("""
                INSERT INTO schema_version (version, description)
                VALUES (?, ?)
            """, (version, description))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ 设置版本失败: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_migration_files(self):
        """获取所有迁移文件"""
        migrations = []
        
        for file in sorted(self.migrations_dir.glob('v*.sql')):
            # 解析文件名: v001_description.sql
            filename = file.stem
            parts = filename.split('_', 1)
            
            if len(parts) == 2:
                version_str = parts[0][1:]  # 去掉 'v' 前缀
                try:
                    version = int(version_str)
                    description = parts[1].replace('_', ' ')
                    migrations.append({
                        'version': version,
                        'description': description,
                        'file': file
                    })
                except ValueError:
                    print(f"⚠️  跳过无效的迁移文件: {file.name}")
        
        return sorted(migrations, key=lambda x: x['version'])
    
    def apply_migration(self, migration):
        """应用单个迁移"""
        print(f"\n应用迁移 v{migration['version']:03d}: {migration['description']}")
        print("-" * 60)
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # 读取迁移文件
            with open(migration['file'], 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # 分割SQL语句
            statements = []
            current_statement = []
            in_up_section = False
            
            for line in sql_content.split('\n'):
                stripped = line.strip()
                
                # 检测UP部分开始
                if '向前迁移' in stripped or 'UP' in stripped:
                    in_up_section = True
                    continue
                
                # 检测DOWN部分开始（停止处理）
                if '向后迁移' in stripped or 'DOWN' in stripped:
                    break
                
                # 跳过注释和空行
                if not stripped or stripped.startswith('--'):
                    continue
                
                if in_up_section:
                    current_statement.append(line)
                    
                    # 如果遇到分号，表示语句结束
                    if stripped.endswith(';'):
                        statement = '\n'.join(current_statement)
                        if statement.strip():
                            statements.append(statement)
                        current_statement = []
            
            # 处理最后一个语句
            if current_statement:
                statement = '\n'.join(current_statement)
                if statement.strip():
                    statements.append(statement)
            
            # 执行所有语句
            for i, statement in enumerate(statements, 1):
                try:
                    print(f"  执行语句 {i}/{len(statements)}...")
                    cursor.execute(statement)
                except sqlite3.OperationalError as e:
                    error_msg = str(e).lower()
                    if 'already exists' in error_msg or 'duplicate' in error_msg:
                        print(f"    ⚠️  已存在，跳过")
                    else:
                        raise
            
            # 记录版本
            self.set_version(migration['version'], migration['description'])
            
            conn.commit()
            print(f"✅ 迁移 v{migration['version']:03d} 应用成功")
            return True
            
        except Exception as e:
            print(f"❌ 迁移失败: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def upgrade(self, target_version=None):
        """升级数据库到指定版本（或最新版本）"""
        current_version = self.get_current_version()
        migrations = self.get_migration_files()
        
        if not migrations:
            print("❌ 没有找到迁移文件")
            return False
        
        # 确定目标版本
        if target_version is None:
            target_version = migrations[-1]['version']
        
        print(f"\n当前版本: v{current_version:03d}")
        print(f"目标版本: v{target_version:03d}")
        
        # 找到需要应用的迁移
        pending_migrations = [
            m for m in migrations 
            if m['version'] > current_version and m['version'] <= target_version
        ]
        
        if not pending_migrations:
            print("\n✅ 数据库已是最新版本")
            return True
        
        print(f"\n需要应用 {len(pending_migrations)} 个迁移:")
        for m in pending_migrations:
            print(f"  - v{m['version']:03d}: {m['description']}")
        
        # 应用迁移
        success = True
        for migration in pending_migrations:
            if not self.apply_migration(migration):
                success = False
                break
        
        if success:
            print(f"\n✅ 数据库已升级到 v{target_version:03d}")
        else:
            print(f"\n❌ 迁移过程中出现错误")
        
        return success
    
    def status(self):
        """显示迁移状态"""
        current_version = self.get_current_version()
        migrations = self.get_migration_files()
        
        print("\n" + "=" * 60)
        print("数据库迁移状态")
        print("=" * 60)
        print(f"\n数据库路径: {self.db_path}")
        print(f"当前版本: v{current_version:03d}")
        
        if not migrations:
            print("\n❌ 没有找到迁移文件")
            return
        
        latest_version = migrations[-1]['version']
        print(f"最新版本: v{latest_version:03d}")
        
        # 显示所有迁移
        print(f"\n迁移列表:")
        print("-" * 60)
        
        for migration in migrations:
            version = migration['version']
            status = "✅ 已应用" if version <= current_version else "⏳ 待应用"
            print(f"  v{version:03d}: {migration['description']:<40} {status}")
        
        # 显示待应用的迁移
        pending = [m for m in migrations if m['version'] > current_version]
        if pending:
            print(f"\n⏳ 有 {len(pending)} 个待应用的迁移")
        else:
            print(f"\n✅ 数据库已是最新版本")
        
        print("=" * 60)
    
    def create_migration(self, description):
        """创建新的迁移文件"""
        migrations = self.get_migration_files()
        
        # 确定新版本号
        if migrations:
            next_version = migrations[-1]['version'] + 1
        else:
            next_version = 1
        
        # 生成文件名
        filename = f"v{next_version:03d}_{description.replace(' ', '_')}.sql"
        filepath = self.migrations_dir / filename
        
        # 创建迁移文件模板
        template = f"""-- 迁移版本: v{next_version:03d}
-- 描述: {description}
-- 作者: [作者名]
-- 日期: {datetime.now().strftime('%Y-%m-%d')}
-- 依赖: v{next_version-1:03d} (如果有)

-- ============================================
-- 向前迁移 (UP)
-- ============================================

-- 在这里添加你的SQL语句
-- 示例:
-- CREATE TABLE IF NOT EXISTS example_table (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );


-- ============================================
-- 向后迁移 (DOWN) - 回滚用
-- ============================================

-- 在这里添加回滚SQL语句（可选）
-- 示例:
-- DROP TABLE IF EXISTS example_table;
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"\n✅ 创建迁移文件: {filename}")
        print(f"   路径: {filepath}")
        print(f"\n请编辑该文件，添加你的迁移SQL语句")
        
        return filepath

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='数据库迁移管理工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # status 命令
    subparsers.add_parser('status', help='显示迁移状态')
    
    # upgrade 命令
    upgrade_parser = subparsers.add_parser('upgrade', help='升级数据库')
    upgrade_parser.add_argument('--target', type=int, help='目标版本号')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='创建新的迁移文件')
    create_parser.add_argument('description', help='迁移描述')
    
    # set-version 命令（谨慎使用）
    set_version_parser = subparsers.add_parser('set-version', help='强制设置版本号（谨慎使用）')
    set_version_parser.add_argument('version', type=int, help='版本号')
    
    args = parser.parse_args()
    
    migrator = DatabaseMigrator()
    
    if args.command == 'status':
        migrator.status()
    
    elif args.command == 'upgrade':
        migrator.upgrade(args.target)
    
    elif args.command == 'create':
        migrator.create_migration(args.description)
    
    elif args.command == 'set-version':
        if migrator.set_version(args.version, "手动设置"):
            print(f"✅ 版本已设置为 v{args.version:03d}")
        else:
            print(f"❌ 设置版本失败")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
