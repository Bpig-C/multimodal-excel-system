"""
清理孤立的数据集数据
删除数据库中存在但语料已被删除的数据集
"""
import sys
import os
from pathlib import Path

# 添加backend目录到Python路径
BACKEND_ROOT = Path(__file__).resolve().parents[2]
os.chdir(BACKEND_ROOT)
sys.path.insert(0, str(BACKEND_ROOT))

from database import SessionLocal
from config import settings
from models.db_models import Dataset, DatasetCorpus, Corpus, AnnotationTask


def get_database_display_path() -> str:
    """获取当前数据库的可读路径（优先显示SQLite绝对路径）"""
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite:///"):
        sqlite_path = db_url.replace("sqlite:///", "", 1)
        return str((BACKEND_ROOT / sqlite_path).resolve())
    return db_url


def clean_orphan_datasets(db):
    """清理孤立的数据集"""
    
    # 获取所有数据集
    datasets = db.query(Dataset).all()
    
    if not datasets:
        print("✓ 没有数据集需要清理")
        return
    
    print(f"找到 {len(datasets)} 个数据集，开始检查...")
    
    cleaned_count = 0
    for dataset in datasets:
        # 检查数据集关联的语料是否存在
        corpus_count = db.query(Corpus).join(
            DatasetCorpus, 
            Corpus.id == DatasetCorpus.corpus_id
        ).filter(
            DatasetCorpus.dataset_id == dataset.id
        ).count()
        
        if corpus_count == 0:
            print(f"\n发现孤立数据集: {dataset.name} (ID: {dataset.dataset_id})")
            print(f"  - 该数据集没有关联的语料")
            
            # 删除关联的标注任务
            task_count = db.query(AnnotationTask).filter(
                AnnotationTask.dataset_id == dataset.id
            ).count()
            if task_count > 0:
                db.query(AnnotationTask).filter(
                    AnnotationTask.dataset_id == dataset.id
                ).delete()
                print(f"  - 删除了 {task_count} 个标注任务")
            
            # 删除数据集-语料关联
            relation_count = db.query(DatasetCorpus).filter(
                DatasetCorpus.dataset_id == dataset.id
            ).count()
            if relation_count > 0:
                db.query(DatasetCorpus).filter(
                    DatasetCorpus.dataset_id == dataset.id
                ).delete()
                print(f"  - 删除了 {relation_count} 个数据集-语料关联")
            
            # 删除数据集
            db.delete(dataset)
            print(f"  - 删除数据集: {dataset.name}")
            
            cleaned_count += 1
    
    if cleaned_count > 0:
        db.commit()
        print(f"\n✓ 清理完成，删除了 {cleaned_count} 个孤立数据集")
    else:
        print("\n✓ 所有数据集都正常，无需清理")


def main():
    """主函数"""
    print("=" * 60)
    print("开始清理孤立的数据集...")
    print("=" * 60)
    print(f"当前数据库: {get_database_display_path()}")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        clean_orphan_datasets(db)
        
        print("=" * 60)
        print("清理完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 清理失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
