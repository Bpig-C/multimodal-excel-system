# 批量自动标注权限分析报告

## 分析日期
2026-02-04

## 问题概述

批量自动标注功能存在**严重的权限和任务范围问题**，需要立即修复。

## 当前实现分析

### 前端权限控制

**位置**: `frontend/src/views/dataset/DatasetDetail.vue`

**按钮可见性**:
```vue
<el-button
  v-if="authStore.user?.role !== 'viewer'"
  type="primary"
  size="small"
  @click="handleBatchAnnotate"
>
  批量标注
</el-button>
```

**结论**: 
- ✅ 浏览员（viewer）不可见批量标注按钮
- ✅ 管理员（admin）可见
- ✅ 标注员（annotator）可见

### 后端权限控制

**位置**: `backend/api/annotations.py`

**API端点**:
```python
@router.post("/batch")
async def trigger_batch_annotation(
    dataset_id: str = Body(..., description="数据集ID"),
    created_by: Optional[int] = Body(None, description="创建人ID"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    # 没有权限检查！
    # 没有用户身份验证！
```

**问题**:
- ❌ **没有用户身份验证** - 任何人都可以调用
- ❌ **没有角色权限检查** - 不验证用户角色
- ❌ **没有数据集访问权限检查** - 不验证用户是否有权访问该数据集

### 任务范围过滤

**位置**: `backend/services/batch_annotation_service.py`

**create_batch_job 方法**:
```python
# 统计待标注任务数量
total_tasks = self.db.query(func.count(AnnotationTask.id))\
    .filter(AnnotationTask.dataset_id == dataset.id)\
    .filter(AnnotationTask.status == 'pending')\
    .scalar() or 0
```

**execute_batch_annotation 方法**:
```python
# 获取待标注任务列表
tasks = self.db.query(AnnotationTask)\
    .filter(AnnotationTask.dataset_id == batch_job.dataset_id)\
    .filter(AnnotationTask.status == 'pending')\
    .all()
```

**问题**:
- ❌ **没有任务范围过滤** - 标注所有pending任务
- ❌ **没有分配检查** - 不检查任务是否分配给当前用户
- ❌ **没有任务范围限制** - 不考虑 dataset_assignments 表中的 task_start_index 和 task_end_index

## 预期行为 vs 实际行为

### 场景 1: 管理员触发批量标注

**预期行为**:
- ✅ 管理员可以批量标注数据集的所有pending任务
- ✅ 不受任务范围限制

**实际行为**:
- ✅ 符合预期（但缺少权限验证）

### 场景 2: 标注员触发批量标注

**预期行为**:
- ✅ 标注员只能批量标注**分配给自己**的任务
- ✅ 必须遵守 dataset_assignments 表中的任务范围
- ✅ 例如：如果分配了任务 1-50，只标注这50个任务

**实际行为**:
- ❌ 标注员会标注数据集的**所有pending任务**
- ❌ 不考虑任务分配
- ❌ 不考虑任务范围限制
- ❌ **严重问题**：标注员可能标注了不属于自己的任务！

### 场景 3: 浏览员触发批量标注

**预期行为**:
- ✅ 浏览员不应该有批量标注权限
- ✅ API应该返回403错误

**实际行为**:
- ✅ 前端按钮不可见（正确）
- ❌ 但如果直接调用API，后端不会拒绝（严重安全问题）

## 安全风险

### 🔴 高风险

1. **未授权访问**
   - 任何人都可以直接调用API
   - 绕过前端权限控制

2. **数据越权**
   - 标注员可以标注不属于自己的任务
   - 可能覆盖其他标注员的工作范围

3. **资源滥用**
   - 恶意用户可以触发大量批量任务
   - 消耗服务器资源

## 修复方案

### 1. 添加权限检查（必须）

**修改**: `backend/api/annotations.py`

```python
from api.users import get_current_user
from services.dataset_assignment_service import DatasetAssignmentService

@router.post("/batch")
async def trigger_batch_annotation(
    dataset_id: str = Body(..., description="数据集ID"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: dict = Depends(get_current_user),  # 添加用户认证
    db: Session = Depends(get_db)
):
    """
    触发批量自动标注
    
    权限要求：
    - 管理员：可以批量标注任何数据集的所有任务
    - 标注员：只能批量标注分配给自己的任务
    - 浏览员：无权限
    """
    user_id = current_user['user_id']
    user_role = current_user['role']
    
    # 1. 检查角色权限
    if user_role == 'viewer':
        raise HTTPException(
            status_code=403,
            detail="浏览员没有批量标注权限"
        )
    
    # 2. 检查数据集访问权限（标注员）
    if user_role == 'annotator':
        assignment_service = DatasetAssignmentService(db)
        has_access = assignment_service.check_user_dataset_access(
            user_id=user_id,
            dataset_id=dataset_id,
            role='annotator'
        )
        if not has_access:
            raise HTTPException(
                status_code=403,
                detail="您没有权限访问该数据集"
            )
    
    try:
        service = BatchAnnotationService(db)
        
        # 创建批量任务（传递用户信息）
        batch_job = service.create_batch_job(
            dataset_id=dataset_id,
            created_by=user_id,
            user_role=user_role  # 新增参数
        )
        
        # 在后台执行批量标注（传递用户信息）
        background_tasks.add_task(
            service.execute_batch_annotation,
            batch_job.job_id,
            user_id,      # 新增参数
            user_role     # 新增参数
        )
        
        return {
            "success": True,
            "message": "批量标注任务已创建",
            "data": {
                "job_id": batch_job.job_id,
                "dataset_id": dataset_id,
                "total_tasks": batch_job.total_tasks,
                "status": batch_job.status
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建批量任务失败: {str(e)}")
```

### 2. 添加任务范围过滤（必须）

**修改**: `backend/services/batch_annotation_service.py`

```python
from services.task_query_service import TaskQueryService

class BatchAnnotationService:
    
    def create_batch_job(
        self,
        dataset_id: str,
        created_by: Optional[int] = None,
        user_role: str = 'admin'  # 新增参数
    ) -> BatchJob:
        """
        创建批量标注任务
        
        Args:
            dataset_id: 数据集ID
            created_by: 创建人ID
            user_role: 用户角色
            
        Returns:
            BatchJob: 批量任务对象
        """
        # 查询数据集
        dataset = self.db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
        
        if not dataset:
            raise ValueError(f"数据集 {dataset_id} 不存在")
        
        # 使用 TaskQueryService 获取用户可访问的任务
        task_query_service = TaskQueryService(self.db)
        
        # 构建查询
        query = self.db.query(AnnotationTask)\
            .filter(AnnotationTask.dataset_id == dataset.id)\
            .filter(AnnotationTask.status == 'pending')
        
        # 应用权限过滤
        if user_role == 'annotator' and created_by:
            # 标注员：只查询分配给自己的任务
            query = task_query_service._apply_permission_filter(
                query=query,
                user_id=created_by,
                user_role=user_role,
                dataset_id=dataset.id
            )
        
        # 统计任务数量
        total_tasks = query.count()
        
        if total_tasks == 0:
            if user_role == 'annotator':
                raise ValueError("没有分配给您的待标注任务")
            else:
                raise ValueError("没有待标注的任务")
        
        # 生成任务ID
        job_id = f"batch-{uuid.uuid4().hex[:12]}"
        
        # 创建批量任务记录
        batch_job = BatchJob(
            job_id=job_id,
            dataset_id=dataset.id,
            status='pending',
            total_tasks=total_tasks,
            completed_tasks=0,
            failed_tasks=0,
            progress=0.0,
            created_by=created_by
        )
        
        self.db.add(batch_job)
        self.db.commit()
        self.db.refresh(batch_job)
        
        return batch_job
    
    async def execute_batch_annotation(
        self,
        job_id: str,
        user_id: Optional[int] = None,  # 新增参数
        user_role: str = 'admin'         # 新增参数
    ):
        """
        执行批量标注(异步)
        
        Args:
            job_id: 任务ID
            user_id: 用户ID
            user_role: 用户角色
        """
        batch_job = self.get_batch_job(job_id)
        
        if not batch_job:
            raise ValueError(f"批量任务 {job_id} 不存在")
        
        try:
            # 更新状态为处理中
            self.update_batch_job_status(job_id, 'processing')
            
            # 使用 TaskQueryService 获取任务列表
            task_query_service = TaskQueryService(self.db)
            
            # 构建查询
            query = self.db.query(AnnotationTask)\
                .filter(AnnotationTask.dataset_id == batch_job.dataset_id)\
                .filter(AnnotationTask.status == 'pending')
            
            # 应用权限过滤
            if user_role == 'annotator' and user_id:
                query = task_query_service._apply_permission_filter(
                    query=query,
                    user_id=user_id,
                    user_role=user_role,
                    dataset_id=batch_job.dataset_id
                )
            
            # 获取任务列表
            tasks = query.all()
            
            completed_count = 0
            failed_count = 0
            
            # 逐个处理任务
            for task in tasks:
                try:
                    # 标注单个任务
                    await self._annotate_single_task(task)
                    completed_count += 1
                except Exception as e:
                    # 记录失败
                    task.status = 'failed'
                    task.error_message = str(e)
                    failed_count += 1
                
                # 更新进度
                self.update_batch_job_status(
                    job_id,
                    'processing',
                    completed_tasks=completed_count,
                    failed_tasks=failed_count
                )
                
                self.db.commit()
            
            # 更新最终状态
            final_status = 'completed' if failed_count == 0 else 'completed_with_errors'
            self.update_batch_job_status(
                job_id,
                final_status,
                completed_tasks=completed_count,
                failed_tasks=failed_count
            )
            
        except Exception as e:
            # 批量任务失败
            self.update_batch_job_status(
                job_id,
                'failed',
                error_message=str(e)
            )
            raise
```

### 3. 添加数据集访问权限检查（建议）

**新增方法**: `backend/services/dataset_assignment_service.py`

```python
def check_user_dataset_access(
    self,
    user_id: int,
    dataset_id: str,
    role: str
) -> bool:
    """
    检查用户是否有权访问数据集
    
    Args:
        user_id: 用户ID
        dataset_id: 数据集ID
        role: 角色（annotator/reviewer）
        
    Returns:
        bool: 是否有权限
    """
    dataset = self.db.query(Dataset).filter(
        Dataset.dataset_id == dataset_id
    ).first()
    
    if not dataset:
        return False
    
    assignment = self.db.query(DatasetAssignment).filter(
        DatasetAssignment.dataset_id == dataset.id,
        DatasetAssignment.user_id == user_id,
        DatasetAssignment.role == role,
        DatasetAssignment.is_active == True
    ).first()
    
    return assignment is not None
```

## 测试场景

### 测试 1: 管理员批量标注

**步骤**:
1. 以管理员身份登录
2. 访问数据集详情页面
3. 点击"批量标注"按钮

**预期结果**:
- ✅ 创建批量任务成功
- ✅ 标注数据集的所有pending任务
- ✅ 不受任务范围限制

### 测试 2: 标注员批量标注（有分配）

**步骤**:
1. 以标注员身份登录
2. 访问已分配的数据集详情页面
3. 点击"批量标注"按钮

**预期结果**:
- ✅ 创建批量任务成功
- ✅ 只标注分配给该标注员的任务
- ✅ 遵守任务范围限制（如：任务1-50）

### 测试 3: 标注员批量标注（无分配）

**步骤**:
1. 以标注员身份登录
2. 访问未分配的数据集详情页面
3. 尝试点击"批量标注"按钮

**预期结果**:
- ❌ 按钮不可见（前端控制）
- ❌ 如果直接调用API，返回403错误

### 测试 4: 浏览员批量标注

**步骤**:
1. 以浏览员身份登录
2. 访问数据集详情页面

**预期结果**:
- ❌ 按钮不可见
- ❌ 如果直接调用API，返回403错误

## 实现优先级

### 🔴 紧急（必须立即修复）

1. **添加用户认证** - 防止未授权访问
2. **添加角色权限检查** - 防止浏览员调用API
3. **添加任务范围过滤** - 防止标注员越权标注

### 🟡 重要（应该尽快实现）

4. **添加数据集访问权限检查** - 验证标注员是否有权访问数据集
5. **添加审计日志** - 记录谁触发了批量标注
6. **添加速率限制** - 防止资源滥用

### 🟢 建议（可以后续优化）

7. **添加批量任务管理界面** - 查看和管理批量任务
8. **添加批量任务取消功能** - 允许用户取消正在执行的任务
9. **添加批量任务通知** - 任务完成后通知用户

## 相关文件

**后端**:
- `backend/api/annotations.py` - 需要添加权限检查
- `backend/services/batch_annotation_service.py` - 需要添加任务范围过滤
- `backend/services/dataset_assignment_service.py` - 需要添加访问权限检查方法
- `backend/services/task_query_service.py` - 复用权限过滤逻辑

**前端**:
- `frontend/src/views/dataset/DatasetDetail.vue` - 批量标注按钮（已有基本权限控制）

## 结论

### 当前状态
❌ **批量标注功能存在严重的安全和权限问题**

### 主要问题
1. ❌ 没有用户认证
2. ❌ 没有角色权限检查
3. ❌ 没有任务范围过滤
4. ❌ 标注员可能标注不属于自己的任务

### 建议
🔴 **立即修复权限和任务范围问题，然后再开放批量标注功能**

在修复之前，建议：
- 暂时禁用批量标注功能
- 或者仅对管理员开放
- 添加明确的警告提示

## 签名

- 分析人: Kiro AI Assistant
- 分析日期: 2026-02-04
- 严重程度: 🔴 高风险
- 状态: 需要立即修复 ⚠️
