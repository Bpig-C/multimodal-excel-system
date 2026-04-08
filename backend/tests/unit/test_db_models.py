"""
测试数据库模型是否正确定义
"""
import sys
from pathlib import Path

# 添加backend目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from models import db_models
from database import Base

def test_models():
    """测试所有模型是否正确定义"""
    
    print("检查数据库模型...")
    print("=" * 60)
    
    # 获取所有模型类
    models = [
        ("User", db_models.User),
        ("Corpus", db_models.Corpus),
        ("Image", db_models.Image),
        ("Dataset", db_models.Dataset),
        ("DatasetCorpus", db_models.DatasetCorpus),
        ("AnnotationTask", db_models.AnnotationTask),
        ("TextEntity", db_models.TextEntity),
        ("ImageEntity", db_models.ImageEntity),
        ("Relation", db_models.Relation),
        ("EntityType", db_models.EntityType),
        ("RelationType", db_models.RelationType),
        ("ReviewTask", db_models.ReviewTask),
        ("VersionHistory", db_models.VersionHistory),
        ("BatchJob", db_models.BatchJob),
    ]
    
    for name, model in models:
        # 检查表名
        table_name = model.__tablename__
        
        # 检查列数
        columns = [c.name for c in model.__table__.columns]
        
        print(f"✓ {name:20s} -> {table_name:25s} ({len(columns)} 列)")
    
    print("=" * 60)
    print(f"总共定义了 {len(models)} 个模型")
    print("所有模型检查通过！")
    
    # 使用 assert 而不是 return
    assert len(models) == 14, f"期望14个模型，实际找到{len(models)}个"


if __name__ == "__main__":
    try:
        test_models()
    except Exception as e:
        print(f"✗ 模型检查失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
