"""
创建默认标签配置版本
将当前的默认配置保存为不可修改的默认版本
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加backend目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from database import SessionLocal
from models.db_models import EntityType, RelationType, LabelSchemaVersion, User


def create_default_version(db):
    """创建默认版本快照"""
    
    print("\n开始创建默认标签配置版本...")
    
    # 1. 检查是否已存在默认版本
    existing_default = db.query(LabelSchemaVersion).filter(
        LabelSchemaVersion.version_id == "DEFAULT_V1.0"
    ).first()
    
    if existing_default:
        print("✓ 默认版本已存在，跳过创建")
        print(f"  版本ID: {existing_default.version_id}")
        print(f"  版本名称: {existing_default.version_name}")
        print(f"  创建时间: {existing_default.created_at}")
        return existing_default
    
    # 2. 获取当前所有实体类型
    entity_types = db.query(EntityType).all()
    entity_types_data = []
    for et in entity_types:
        entity_types_data.append({
            "type_name": et.type_name,
            "type_name_zh": et.type_name_zh,
            "color": et.color,
            "description": et.description,
            "definition": et.definition,
            "examples": et.examples,
            "disambiguation": et.disambiguation,
            "supports_bbox": et.supports_bbox,
            "is_active": et.is_active,
            "is_reviewed": et.is_reviewed
        })
    
    # 3. 获取当前所有关系类型
    relation_types = db.query(RelationType).all()
    relation_types_data = []
    for rt in relation_types:
        relation_types_data.append({
            "type_name": rt.type_name,
            "type_name_zh": rt.type_name_zh,
            "color": rt.color,
            "description": rt.description,
            "definition": rt.definition,
            "direction_rule": rt.direction_rule,
            "examples": rt.examples,
            "disambiguation": rt.disambiguation,
            "is_active": rt.is_active,
            "is_reviewed": rt.is_reviewed
        })
    
    # 4. 构建版本快照数据
    schema_data = {
        "version": "1.0",
        "created_at": datetime.utcnow().isoformat(),
        "metadata": {
            "total_entity_types": len(entity_types_data),
            "total_relation_types": len(relation_types_data),
            "active_entity_types": sum(1 for et in entity_types_data if et["is_active"]),
            "active_relation_types": sum(1 for rt in relation_types_data if rt["is_active"]),
            "is_default": True,  # 标记为默认版本
            "is_readonly": True  # 标记为只读（不可修改）
        },
        "entity_types": entity_types_data,
        "relation_types": relation_types_data
    }
    
    # 5. 获取管理员用户ID
    admin_user = db.query(User).filter(User.username == "admin").first()
    created_by = admin_user.id if admin_user else None
    
    # 6. 创建版本记录
    version = LabelSchemaVersion(
        version_id="DEFAULT_V1.0",
        version_name="默认配置 v1.0",
        description="系统默认的标签配置（16种实体类型 + 1种关系类型）。此版本为只读版本，不可修改。如需自定义，请创建新版本。",
        schema_data=json.dumps(schema_data, ensure_ascii=False, indent=2),
        is_active=True,  # 设置为活跃版本
        created_by=created_by
    )
    
    db.add(version)
    db.commit()
    
    print(f"\n✓ 成功创建默认版本:")
    print(f"  版本ID: {version.version_id}")
    print(f"  版本名称: {version.version_name}")
    print(f"  实体类型: {len(entity_types_data)} 个")
    print(f"  关系类型: {len(relation_types_data)} 个")
    print(f"  是否活跃: {version.is_active}")
    print(f"  创建时间: {version.created_at}")
    
    # 7. 打印版本内容摘要
    print("\n" + "=" * 60)
    print("版本内容摘要:")
    print("=" * 60)
    print(f"\n实体类型 ({len(entity_types_data)}个):")
    for i, et in enumerate(entity_types_data, 1):
        bbox = "✓" if et["supports_bbox"] else " "
        print(f"  {i:2d}. {et['type_name_zh']:10s} [bbox:{bbox}]")
    
    print(f"\n关系类型 ({len(relation_types_data)}个):")
    for i, rt in enumerate(relation_types_data, 1):
        print(f"  {i}. {rt['type_name_zh']} ({rt['type_name']})")
    
    return version


def main():
    """主函数"""
    print("=" * 60)
    print("创建默认标签配置版本")
    print("=" * 60)
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        version = create_default_version(db)
        
        print("\n" + "=" * 60)
        print("默认版本创建完成！")
        print("=" * 60)
        print("\n特性:")
        print("  ✓ 版本ID: DEFAULT_V1.0")
        print("  ✓ 标记为默认版本 (is_default: true)")
        print("  ✓ 标记为只读版本 (is_readonly: true)")
        print("  ✓ 设置为活跃版本 (is_active: true)")
        print("\n使用说明:")
        print("  1. 此版本在前端版本管理中显示为'默认配置'")
        print("  2. 此版本不可修改、不可删除")
        print("  3. 可以随时切换回此版本")
        print("  4. 如需自定义，请创建新版本")
        
    except Exception as e:
        print(f"\n✗ 创建失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
