"""
测试Pydantic数据模型
"""
import sys
from pathlib import Path

# 添加backend目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from models import schemas
from datetime import datetime


def test_schemas():
    """测试Pydantic模型"""
    
    print("检查Pydantic数据模型...")
    print("=" * 60)
    
    # 测试基础模型
    print("✓ 测试基础模型...")
    bbox = schemas.BoundingBox(x=10, y=20, width=100, height=50)
    entity = schemas.Entity(id=1, token="测试", label="产品型号", start_offset=0, end_offset=2)
    relation = schemas.Relation(id=1, from_id=1, to_id=2, type="relates_to")
    
    # 测试用户模型
    print("✓ 测试用户模型...")
    user_create = schemas.UserCreate(username="test", password="123456", role=schemas.UserRole.ADMIN)
    login_req = schemas.LoginRequest(username="admin", password="admin123")
    
    # 测试语料模型
    print("✓ 测试语料模型...")
    image_info = schemas.ImageInfo(image_id="img_001", file_path="imgs/test.png")
    corpus = schemas.CorpusRecord(
        text_id="corpus_001",
        text="这是测试文本",
        text_type="问题描述",
        has_images=True,
        images=[image_info],
        created_at=datetime.utcnow()
    )
    
    # 测试数据集模型
    print("✓ 测试数据集模型...")
    dataset_create = schemas.DatasetCreateRequest(
        name="测试数据集",
        description="这是一个测试数据集",
        corpus_ids=[1, 2],
        created_by=1
    )
    
    # 测试标注任务模型
    print("✓ 测试标注任务模型...")
    add_entity = schemas.AddEntityRequest(
        token="测试实体",
        label="产品型号",
        start_offset=0,
        end_offset=4
    )
    add_relation = schemas.AddRelationRequest(from_id=1, to_id=2, type="relates_to")
    
    # 测试标签配置模型
    print("✓ 测试标签配置模型...")
    entity_type = schemas.EntityTypeConfig(
        type_name="产品型号",
        type_name_zh="产品型号",
        color="#1f77b4",
        description="产品的具体型号标识"
    )
    
    # 测试批量任务模型
    print("✓ 测试批量任务模型...")
    batch_req = schemas.BatchAnnotationRequest(dataset_id="dataset_001")
    
    # 测试导出模型
    print("✓ 测试导出模型...")
    export_req = schemas.ExportRequest(
        dataset_id="dataset_001",
        status_filter=["completed"],
        train_test_split=0.8
    )
    
    # 测试响应模型
    print("✓ 测试响应模型...")
    success_resp = schemas.SuccessResponse(message="操作成功", data={"key": "value"})
    error_resp = schemas.ErrorResponse(
        error_code="TEST_ERROR",
        error_message="这是一个测试错误"
    )
    
    print("=" * 60)
    print("所有Pydantic模型测试通过！")
    
    # 测试序列化
    print("\n测试JSON序列化...")
    print(f"Entity: {entity.model_dump_json()}")
    print(f"BoundingBox: {bbox.model_dump_json()}")
    print(f"UserCreate: {user_create.model_dump_json()}")
    
    print("\n✓ JSON序列化测试通过！")
    
    # 使用 assert 而不是 return
    assert bbox.x == 10, "BoundingBox x 坐标不正确"
    assert entity.token == "测试", "Entity token 不正确"
    assert user_create.username == "test", "UserCreate username 不正确"


if __name__ == "__main__":
    try:
        test_schemas()
    except Exception as e:
        print(f"✗ 模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
