# 语料管理API文档

## 概述

语料管理API提供了完整的语料数据管理功能，包括Excel文件上传、语料查询、删除和图片管理。

## API端点

### 1. 上传Excel文件

**端点:** `POST /api/v1/corpus/upload`

**描述:** 上传品质失效案例Excel文件，系统自动提取内嵌图片并处理为句子级语料

**请求:**
- Content-Type: multipart/form-data
- Body: file (Excel文件)

**响应:**
```json
{
  "success": true,
  "message": "成功处理文件 example.xlsx",
  "total_records": 50,
  "total_sentences": 150,
  "total_images": 25,
  "field_distribution": {
    "问题描述": 45,
    "原因分析": 38,
    "采取措施": 42,
    "图片": 25
  }
}
```

**功能:**
- 验证Excel文件格式
- 提取WPS内嵌图片
- 文本分句处理
- 自动标注字段来源分类
- 生成语料记录

---

### 2. 获取语料列表

**端点:** `GET /api/v1/corpus`

**描述:** 获取语料列表，支持分页和筛选

**查询参数:**
- `page` (int, 默认: 1): 页码
- `page_size` (int, 默认: 20, 最大: 100): 每页数量
- `source_field` (string, 可选): 按字段分类筛选
- `has_images` (boolean, 可选): 是否包含图片

**响应:**
```json
{
  "total": 150,
  "items": [
    {
      "text_id": "corpus_001",
      "text": "2022年02月21日，捷普产线反馈CB760-60038产品排线连锡10pcs。",
      "text_type": "问题描述",
      "source_file": "品质失效案例-2022年.xlsx",
      "source_row": 5,
      "source_field": "问题描述",
      "has_images": true,
      "images": [
        {
          "image_id": "ID_228A8CA5B0AB49848DD6699BFAAF4F35",
          "file_path": "imgs/ID_228A8CA5B0AB49848DD6699BFAAF4F35.png",
          "original_name": "image1.png",
          "width": 800,
          "height": 600
        }
      ],
      "created_at": "2024-01-19T10:30:00"
    }
  ]
}
```

**功能:**
- 分页查询
- 按字段分类筛选
- 按是否包含图片筛选
- 返回关联图片信息

---

### 3. 获取语料详情

**端点:** `GET /api/v1/corpus/{corpus_id}`

**描述:** 获取单个语料的完整信息

**路径参数:**
- `corpus_id` (string): 语料ID

**响应:**
```json
{
  "text_id": "corpus_001",
  "text": "2022年02月21日，捷普产线反馈CB760-60038产品排线连锡10pcs。",
  "text_type": "问题描述",
  "source_file": "品质失效案例-2022年.xlsx",
  "source_row": 5,
  "source_field": "问题描述",
  "has_images": true,
  "images": [
    {
      "image_id": "ID_228A8CA5B0AB49848DD6699BFAAF4F35",
      "file_path": "imgs/ID_228A8CA5B0AB49848DD6699BFAAF4F35.png",
      "original_name": "image1.png",
      "width": 800,
      "height": 600
    }
  ],
  "created_at": "2024-01-19T10:30:00"
}
```

**错误响应:**
- 404: 语料不存在

---

### 4. 删除语料

**端点:** `DELETE /api/v1/corpus/{corpus_id}`

**描述:** 删除指定语料及其关联的图片记录（级联删除）

**路径参数:**
- `corpus_id` (string): 语料ID

**响应:**
```json
{
  "success": true,
  "message": "成功删除语料 corpus_001"
}
```

**注意:**
- 会级联删除关联的图片记录
- 不会删除物理图片文件

**错误响应:**
- 404: 语料不存在
- 500: 删除失败

---

### 5. 获取语料关联图片

**端点:** `GET /api/v1/corpus/{corpus_id}/images`

**描述:** 获取指定语料的所有关联图片

**路径参数:**
- `corpus_id` (string): 语料ID

**响应:**
```json
[
  {
    "image_id": "ID_228A8CA5B0AB49848DD6699BFAAF4F35",
    "file_path": "imgs/ID_228A8CA5B0AB49848DD6699BFAAF4F35.png",
    "original_name": "image1.png",
    "width": 800,
    "height": 600
  },
  {
    "image_id": "ID_3B0375FA7F5C4757845B8502045543D6",
    "file_path": "imgs/ID_3B0375FA7F5C4757845B8502045543D6.png",
    "original_name": "image2.png",
    "width": 1024,
    "height": 768
  }
]
```

**错误响应:**
- 404: 语料不存在

---

## 使用示例

### Python (requests)

```python
import requests

# 上传Excel文件
with open('品质失效案例.xlsx', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/v1/corpus/upload', files=files)
    print(response.json())

# 获取语料列表（第一页，每页20条）
response = requests.get('http://localhost:8000/api/v1/corpus?page=1&page_size=20')
corpus_list = response.json()

# 筛选包含图片的语料
response = requests.get('http://localhost:8000/api/v1/corpus?has_images=true')

# 按字段筛选
response = requests.get('http://localhost:8000/api/v1/corpus?source_field=问题描述')

# 获取语料详情
corpus_id = 'corpus_001'
response = requests.get(f'http://localhost:8000/api/v1/corpus/{corpus_id}')
corpus_detail = response.json()

# 获取语料关联图片
response = requests.get(f'http://localhost:8000/api/v1/corpus/{corpus_id}/images')
images = response.json()

# 删除语料
response = requests.delete(f'http://localhost:8000/api/v1/corpus/{corpus_id}')
```

### JavaScript (fetch)

```javascript
// 上传Excel文件
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/v1/corpus/upload', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => console.log(data));

// 获取语料列表
fetch('http://localhost:8000/api/v1/corpus?page=1&page_size=20')
  .then(response => response.json())
  .then(data => console.log(data));

// 获取语料详情
fetch(`http://localhost:8000/api/v1/corpus/${corpusId}`)
  .then(response => response.json())
  .then(data => console.log(data));

// 删除语料
fetch(`http://localhost:8000/api/v1/corpus/${corpusId}`, {
  method: 'DELETE'
})
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 测试

运行单元测试:

```bash
cd backend
python -m pytest tests/test_api_corpus.py -v
```

测试覆盖:
- ✅ 空列表查询
- ✅ 带数据的列表查询
- ✅ 分页功能
- ✅ 字段筛选
- ✅ 图片筛选
- ✅ 语料详情查询
- ✅ 带图片的语料详情
- ✅ 不存在的语料查询
- ✅ 语料删除
- ✅ 级联删除（带图片）
- ✅ 删除不存在的语料
- ✅ 获取语料图片列表
- ✅ 获取空图片列表
- ✅ 获取不存在语料的图片

---

## 错误处理

所有API端点都实现了统一的错误处理:

- **400 Bad Request**: 请求参数错误或文件格式不正确
- **404 Not Found**: 请求的资源不存在
- **500 Internal Server Error**: 服务器内部错误

错误响应格式:
```json
{
  "detail": "错误描述信息"
}
```

---

## 性能考虑

- 使用数据库索引优化查询性能
- 分页查询避免一次加载大量数据
- 支持按需筛选减少数据传输
- 级联删除使用数据库外键约束

---

## 安全性

- 文件类型验证（仅允许.xlsx和.xls）
- SQL注入防护（使用ORM参数化查询）
- 事务管理确保数据一致性
- 临时文件自动清理

---

## 依赖关系

- FastAPI: Web框架
- SQLAlchemy: ORM
- Pydantic: 数据验证
- ExcelProcessingService: Excel处理服务

---

## 相关需求

本API实现满足以下需求:
- Requirements 1.8: 文件处理完成时显示处理统计信息
- Requirements 1.9: 管理员请求预览原始语料时显示分页列表
