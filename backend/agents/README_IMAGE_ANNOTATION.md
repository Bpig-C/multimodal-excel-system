# 图片标注Agent文档

## 概述

图片标注Agent用于对图片进行自动分类标注，支持整图标注和区域标注。当前实现为**简化版**，使用规则或默认标签进行分类，为后续集成多模态LLM预留了接口。

## 架构设计

### 1. 简化版Agent (`ImageAnnotationAgent`)

**特点**:
- 不依赖外部多模态LLM
- 使用规则或默认标签
- 快速响应，适合开发和测试
- 为生产环境预留扩展接口

**使用场景**:
- 开发和测试阶段
- 不需要复杂图片理解的场景
- 作为多模态LLM的fallback方案

### 2. 完整版Agent (`MultimodalLLMAgent`)

**特点**:
- 集成Qwen-VL或其他多模态LLM
- 支持图片理解和描述生成
- 支持基于上下文的智能分类
- 支持缺陷检测和定位

**使用场景**:
- 生产环境
- 需要精确图片分类的场景
- 需要缺陷检测和定位的场景

## 使用方法

### 基础使用

```python
from agents.image_annotation import ImageAnnotationAgent

# 创建Agent实例
agent = ImageAnnotationAgent()

# 单张图片标注
result = agent.annotate_image(
    image_path="/path/to/image.jpg",
    context_text="产品排线连锡缺陷",
    available_labels=["缺陷图片", "正常图片"]
)

print(f"标签: {result.label}")
print(f"置信度: {result.confidence}")
```

### 批量标注

```python
# 批量标注多张图片
results = agent.annotate_images_batch(
    image_paths=[
        "/path/to/img1.jpg",
        "/path/to/img2.jpg",
        "/path/to/img3.jpg"
    ],
    context_text="批量缺陷检测",
    available_labels=["缺陷图片"]
)

for result in results:
    print(f"{result.image_path}: {result.label}")
```

### 在批量标注服务中集成

```python
from agents.image_annotation import ImageAnnotationAgent
from models.db_models import Image, ImageEntity

def annotate_task_images(task, db):
    """为标注任务的图片生成标注"""
    agent = ImageAnnotationAgent()
    
    # 获取任务关联的图片
    images = db.query(Image).filter(
        Image.corpus_id == task.corpus_id
    ).all()
    
    # 获取可用的图片标签
    available_labels = ["缺陷图片", "缺陷区域"]
    
    # 批量标注
    for image in images:
        result = agent.annotate_image(
            image_path=image.file_path,
            context_text=task.corpus.text,
            available_labels=available_labels
        )
        
        # 创建图片实体
        image_entity = ImageEntity(
            task_id=task.id,
            entity_id=get_next_entity_id(task),
            version=1,
            image_id=image.id,
            label=result.label,
            confidence=result.confidence,
            # 整图标注，bbox为None
            bbox_x=None,
            bbox_y=None,
            bbox_width=None,
            bbox_height=None
        )
        
        db.add(image_entity)
    
    db.commit()
```

## 输出格式

### ImageAnnotationOutput

```python
class ImageAnnotationOutput(BaseModel):
    image_path: str          # 图片路径
    label: str               # 分类标签
    confidence: float        # 置信度(0-1)
    description: str         # 图片描述（可选）
```

**示例**:
```json
{
    "image_path": "/data/images/defect_001.jpg",
    "label": "缺陷图片",
    "confidence": 0.85,
    "description": "图片分类为: 缺陷图片"
}
```

## 扩展指南

### 集成Qwen-VL多模态模型

1. **安装依赖**:
```bash
pip install dashscope
```

2. **配置API Key**:
```python
import os
os.environ['DASHSCOPE_API_KEY'] = 'your-api-key'
```

3. **实现MultimodalLLMAgent**:

```python
from dashscope import MultiModalConversation

class MultimodalLLMAgent:
    def __init__(self, model_name: str = "qwen-vl-max"):
        self.model_name = model_name
        self.client = MultiModalConversation()
    
    def classify_image(
        self,
        image_path: str,
        context: str,
        candidate_labels: list
    ) -> Dict[str, Any]:
        """使用Qwen-VL对图片进行分类"""
        
        # 构建Prompt
        prompt = f"""
请根据以下上下文和图片内容，从候选标签中选择最合适的标签对图片进行分类。

上下文: {context}
候选标签: {', '.join(candidate_labels)}

请返回JSON格式:
{{
    "label": "选择的标签",
    "confidence": 0.95,
    "reasoning": "选择理由"
}}
"""
        
        # 调用API
        messages = [
            {
                "role": "user",
                "content": [
                    {"image": image_path},
                    {"text": prompt}
                ]
            }
        ]
        
        response = self.client.call(
            model=self.model_name,
            messages=messages
        )
        
        # 解析响应
        result = json.loads(response.output.choices[0].message.content)
        
        return result
```

### 实现缺陷检测

```python
def detect_defects(
    self,
    image_path: str,
    defect_types: list
) -> list[Dict[str, Any]]:
    """检测图片中的缺陷并返回边界框"""
    
    prompt = f"""
请检测图片中的以下类型缺陷: {', '.join(defect_types)}

对于每个检测到的缺陷，返回:
1. 缺陷类型
2. 边界框坐标 (x, y, width, height)
3. 置信度

返回JSON格式的列表。
"""
    
    # 调用多模态LLM
    response = self.call_multimodal_llm(image_path, prompt)
    
    # 解析响应，返回缺陷列表
    defects = parse_defect_response(response)
    
    return defects
```

### 添加图片预处理

```python
from PIL import Image
import numpy as np

def preprocess_image(image_path: str) -> np.ndarray:
    """图片预处理"""
    img = Image.open(image_path)
    
    # 调整大小
    img = img.resize((224, 224))
    
    # 归一化
    img_array = np.array(img) / 255.0
    
    return img_array
```

## 测试

运行测试：
```bash
cd backend
python test_image_annotation_agent.py
```

测试覆盖：
- ✅ 单张图片标注
- ✅ 批量图片标注
- ✅ 自定义标签支持
- ✅ 输出格式验证
- ✅ 默认标签列表

## 性能优化

### 1. 批量处理优化

```python
def annotate_images_batch_optimized(
    self,
    image_paths: list,
    batch_size: int = 10
) -> list[ImageAnnotationOutput]:
    """批量处理优化版本"""
    results = []
    
    # 分批处理
    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i:i+batch_size]
        
        # 并行处理批次
        batch_results = self.process_batch_parallel(batch)
        results.extend(batch_results)
    
    return results
```

### 2. 缓存机制

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_image_features(image_path: str):
    """缓存图片特征"""
    return extract_features(image_path)
```

### 3. 异步处理

```python
import asyncio

async def annotate_image_async(
    self,
    image_path: str
) -> ImageAnnotationOutput:
    """异步图片标注"""
    result = await self.call_llm_async(image_path)
    return result
```

## 最佳实践

1. **标签一致性**: 使用标签配置系统中定义的标签
2. **置信度阈值**: 设置置信度阈值，低于阈值的标注需要人工复核
3. **错误处理**: 妥善处理图片加载失败、API调用失败等异常
4. **日志记录**: 记录标注过程和结果，便于调试和审计
5. **性能监控**: 监控标注速度和准确率

## 相关文档

- [批量标注服务文档](../services/README_BATCH_ANNOTATION.md)
- [图片标注API文档](../api/README_IMAGES_API.md)
- [标签管理文档](./README_LABEL_MANAGEMENT.md)

## 未来规划

- [ ] 集成Qwen-VL多模态模型
- [ ] 实现缺陷检测和定位
- [ ] 支持多种图片格式
- [ ] 添加图片增强和预处理
- [ ] 实现主动学习机制
- [ ] 支持自定义模型fine-tuning
