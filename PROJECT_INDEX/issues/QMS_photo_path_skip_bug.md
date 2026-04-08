# [BUG] QMS 图片路径在重复检测中被永久跳过

**记录时间**：2026-04-02  
**严重程度**：中（数据完整性问题，不影响导入流程本身）  
**状态**：已关闭——经代码核查，photo_path 问题不存在；内容哈希双轨去重已实现

---

## 问题描述

QMS 数据的文件上传与图片上传是两个独立步骤。当先上传 Excel、后上传图片 ZIP 时，若后续再上传含有重叠制令单号的 Excel，`skip_if_exists=True` 会直接跳过已有记录，导致 `photo_path` 永久无法被更新为本地路径。

## 复现路径

```
1. 上传 QMS Excel（含照片 URL 字段）
   → parser.py 解析时图片未到本地
   → QMSDefectOrder.photo_path = None 或原始 URL

2. 上传图片 ZIP
   → 图片解压到 data/processed/qms/{data_source}/imgs/
   → 数据库记录不触发更新

3. 上传含有部分重叠制令单号的新 Excel（文件哈希不同，正常进入处理）
   → QMSGraphBuilder.build_graph(skip_if_exists=True)
   → 命中 filter_by(id=event_id) → return False，直接跳过
   → photo_path 仍然是 None，不会被修正
```

## 根本原因

`qms_graph_builder.py:31-34`：

```python
if skip_if_exists:
    existing = db.query(QMSDefectOrder).filter_by(id=event_id).first()
    if existing:
        return False  # 全字段跳过，包括 photo_path
```

`skip_if_exists` 是全字段跳过，没有对关键字段做条件更新（upsert 语义）。

## 影响范围

- `QMSDefectOrder.photo_path` 字段可能永久为 None
- 涉及接口：`POST /api/v1/documents/upload`（processor_name=qms）
- 涉及文件：`backend/services/qms_graph_builder.py`

## 相关讨论

还有两个关联问题一并记录：

### 附1：主键不同内容相同的语义重复

现有去重锚点仅为 `制令单号`（主键）。若两条记录制令单号不同但其余字段完全相同，系统不会识别为重复，均会写入。  
**是否需要处理**：取决于业务——若制令单号是 QMS 系统中的唯一业务主键，此场景不会在实际数据中出现，无需处理。

### 附2：文件部分重叠的整体处理机制（已确认正常）

- 文件级：SHA256 哈希拦截完全相同文件
- 条目级：`filter_by(id=event_id)` 跳过已有主键，新条目正常插入
- 两者配合已覆盖"新旧文件有重叠行"的标准场景

## 后续核查（2026-04-02）

经阅读 `query_engine.py`，`photo_path` 问题实际不存在：

- `_build_qms_preview_urls` → `_resolve_processed_preview_url('qms', data_source, path)` 在**查询时**动态拼接 `data_source` 解析完整路径
- `photo_path` 存的相对路径 `imgs/filename` 结合 `data_source` 字段即可定位实际文件
- 图片上传后文件存在，预览 URL 自动生成，无需更新数据库记录
- 最终已实现的有效修复：**内容哈希双轨去重**（见 `graph_builder.py` / `qms_graph_builder.py`）

在 `build_graph` 的 `skip_if_exists` 分支中，对 `photo_path` 做条件更新：

```python
if skip_if_exists:
    existing = db.query(QMSDefectOrder).filter_by(id=event_id).first()
    if existing:
        # 若已有记录缺失图片路径，且新记录有图片，则补全
        new_photo = images[0] if images else None
        if not existing.photo_path and new_photo:
            existing.photo_path = new_photo
            db.commit()
        return False
```

---

*此问题由对话分析发现，尚未提交 issue 或 PR。*
