"""
数据库初始化脚本
创建所有表并插入初始数据
"""
import sys
import bcrypt
from pathlib import Path

# 添加backend目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from database import init_db, SessionLocal
from models.db_models import EntityType, RelationType, User


def create_default_entity_types(db):
    """创建默认实体类型（品质失效案例领域本体）"""
    
    # 检查是否已存在实体类型
    existing_count = db.query(EntityType).count()
    if existing_count > 0:
        print(f"✓ 实体类型已存在 ({existing_count}个)")
        return
    
    # 文本实体类型
    text_entity_types = [
        {"type_name": "产品型号", "type_name_zh": "产品型号", "color": "#1f77b4", "description": "产品的具体型号标识", "supports_bbox": False},
        {"type_name": "缺陷类型", "type_name_zh": "缺陷类型", "color": "#ff7f0e", "description": "产品质量问题的具体表现", "supports_bbox": False},
        {"type_name": "客户名称", "type_name_zh": "客户名称", "color": "#2ca02c", "description": "产品的接收方或投诉方", "supports_bbox": False},
        {"type_name": "日期时间", "type_name_zh": "日期时间", "color": "#d62728", "description": "事件发生的时间", "supports_bbox": False},
        {"type_name": "地点部门", "type_name_zh": "地点部门", "color": "#9467bd", "description": "发生问题的地点或部门", "supports_bbox": False},
        {"type_name": "数量", "type_name_zh": "数量", "color": "#8c564b", "description": "涉及的数量信息", "supports_bbox": False},
        {"type_name": "处置措施", "type_name_zh": "处置措施", "color": "#e377c2", "description": "针对问题采取的处理方式", "supports_bbox": False},
        {"type_name": "产品阶段", "type_name_zh": "产品阶段", "color": "#7f7f7f", "description": "产品所处的生产阶段", "supports_bbox": False},
        {"type_name": "设备名称", "type_name_zh": "设备名称", "color": "#bcbd22", "description": "生产过程中使用的设备", "supports_bbox": False},
        {"type_name": "工艺参数", "type_name_zh": "工艺参数", "color": "#17becf", "description": "生产工艺的参数设置", "supports_bbox": False},
        {"type_name": "生产工艺", "type_name_zh": "生产工艺", "color": "#ff9896", "description": "生产过程中的工序", "supports_bbox": False},
        {"type_name": "电子元件", "type_name_zh": "电子元件", "color": "#9edae5", "description": "电子产品的组成部件", "supports_bbox": False},
        {"type_name": "人员角色", "type_name_zh": "人员角色", "color": "#c5b0d5", "description": "相关人员的角色", "supports_bbox": False},
        {"type_name": "改进措施", "type_name_zh": "改进措施", "color": "#c49c94", "description": "为防止问题再发采取的改进措施", "supports_bbox": False},
    ]
    
    # 图片实体类型
    image_entity_types = [
        {"type_name": "缺陷图片", "type_name_zh": "缺陷图片", "color": "#e74c3c", "description": "整张图片作为缺陷证据", "supports_bbox": False},
        {"type_name": "缺陷区域", "type_name_zh": "缺陷区域", "color": "#e67e22", "description": "图片中标注的特定缺陷区域", "supports_bbox": True},
    ]
    
    all_types = text_entity_types + image_entity_types
    
    for et in all_types:
        entity_type = EntityType(**et)
        db.add(entity_type)
    
    db.commit()
    print(f"✓ 创建了 {len(all_types)} 个默认实体类型")


def create_default_relation_types(db):
    """创建默认关系类型"""
    
    # 检查是否已存在关系类型
    existing_count = db.query(RelationType).count()
    if existing_count > 0:
        print(f"✓ 关系类型已存在 ({existing_count}个)")
        return
    
    relation_types = [
        {"type_name": "relates_to", "type_name_zh": "关联", "color": "#3498db", "description": "通用有向关系，表示源实体指向目标实体"},
    ]
    
    for rt in relation_types:
        relation_type = RelationType(**rt)
        db.add(relation_type)
    
    db.commit()
    print(f"✓ 创建了 {len(relation_types)} 个默认关系类型")


def create_default_admin(db):
    """创建默认管理员账户"""
    
    # 检查是否已存在管理员
    existing_admin = db.query(User).filter(User.username == "admin").first()
    
    # 使用bcrypt加密密码
    password = "admin123"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    password_hash = hashed.decode('utf-8')
    
    if existing_admin:
        # 更新现有管理员的密码
        existing_admin.password_hash = password_hash
        db.commit()
        print("✓ 更新管理员账户密码 (用户名: admin, 密码: admin123)")
    else:
        # 创建新的管理员
        admin = User(
            username="admin",
            password_hash=password_hash,
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("✓ 创建默认管理员账户 (用户名: admin, 密码: admin123)")


def main():
    """主函数"""
    print("=" * 60)
    print("开始初始化数据库...")
    print("=" * 60)
    
    # 创建所有表
    init_db()
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 插入初始数据
        create_default_entity_types(db)
        create_default_relation_types(db)
        create_default_admin(db)
        
        print("=" * 60)
        print("数据库初始化完成！")
        print("=" * 60)
        print("\n默认管理员账户:")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n请在生产环境中修改默认密码！")
        
    except Exception as e:
        print(f"✗ 初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
