# 前端开发准备清单

**版本**: 1.0  
**更新时间**: 2026-01-19

## ✅ 开始前端开发前的准备工作

### 1. 后端环境准备

- [ ] **后端服务已启动**
  ```bash
  cd backend
  python main.py
  # 确认服务运行在 http://localhost:8000
  ```

- [ ] **API文档可访问**
  - [ ] Swagger UI: http://localhost:8000/docs
  - [ ] ReDoc: http://localhost:8000/redoc

- [ ] **测试账号可用**
  ```json
  {
    "username": "admin",
    "password": "admin123",
    "role": "admin"
  }
  ```

- [ ] **数据库已初始化**
  ```bash
  python init_db.py
  ```

### 2. 文档阅读

- [ ] **已阅读**: [前端对接指南](./FRONTEND_INTEGRATION_GUIDE.md) ⭐⭐⭐
- [ ] **已阅读**: [API文档总览](../api/API_DOCUMENTATION.md) ⭐⭐⭐
- [ ] **已阅读**: [后端项目总览](./BACKEND_PROJECT_OVERVIEW.md) ⭐⭐
- [ ] **已浏览**: Swagger UI在线文档 ⭐⭐

### 3. API测试

使用Postman/Insomnia测试以下核心API：

- [ ] **认证API**
  - [ ] POST `/api/v1/auth/login` - 登录
  - [ ] GET `/api/v1/auth/me` - 获取当前用户

- [ ] **语料管理API**
  - [ ] POST `/api/v1/corpus/upload` - 上传Excel
  - [ ] GET `/api/v1/corpus` - 获取语料列表

- [ ] **数据集API**
  - [ ] POST `/api/v1/datasets` - 创建数据集
  - [ ] GET `/api/v1/datasets` - 获取数据集列表

- [ ] **标注任务API**
  - [ ] POST `/api/v1/annotations/batch` - 批量标注
  - [ ] GET `/api/v1/annotations/{task_id}` - 获取任务详情

### 4. 技术准备

- [ ] **前端框架选择**
  - [ ] Vue 3 / React / Angular
  - [ ] 状态管理: Pinia / Redux / NgRx
  - [ ] UI组件库: Element Plus / Ant Design / Material UI

- [ ] **HTTP客户端**
  - [ ] axios / fetch
  - [ ] 请求拦截器配置
  - [ ] 响应拦截器配置

- [ ] **路由配置**
  - [ ] 路由守卫（认证检查）
  - [ ] 权限控制

### 5. 开发环境配置

- [ ] **环境变量配置**
  ```env
  VITE_API_BASE_URL=http://localhost:8000/api/v1
  VITE_UPLOAD_URL=http://localhost:8000/api/v1/corpus/upload
  ```

- [ ] **代理配置**（开发环境跨域）
  ```javascript
  // vite.config.js / vue.config.js
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
  ```

---

## 📋 前端功能模块清单（对齐原始需求）

### 核心页面（按原始任务列表27-45组织）

#### 任务27: 前端项目初始化和路由配置
- [ ] **项目结构搭建**
  - [ ] Vue3项目创建
  - [ ] Vue Router配置（页面路由）
  - [ ] Pinia状态管理配置
  - [ ] Axios配置（API请求封装）
  - [ ] Element Plus UI组件库配置
  - [ ] TypeScript类型定义

#### 任务28: 前端API服务层实现
- [ ] **API封装**
  - [ ] 语料管理API封装
  - [ ] 数据集管理API封装
  - [ ] 标注任务API封装
  - [ ] 图片标注API封装
  - [ ] 标签管理API封装
  - [ ] 复核API封装
  - [ ] 用户管理API封装
  - [ ] 统一错误处理

#### 任务29: 前端状态管理实现
- [ ] **Pinia Store**
  - [ ] 语料管理Store
  - [ ] 数据集管理Store
  - [ ] 标注任务Store
  - [ ] 标签配置Store
  - [ ] 用户认证Store

#### 任务30: Excel导入页面实现
- [ ] **语料导入页面**
  - [ ] 文件上传组件（FileUploader）
  - [ ] 处理进度显示组件（ProcessingProgress）
  - [ ] 语料预览列表组件（CorpusPreview）
  - [ ] 按字段分类筛选功能
  - [ ] 图片缩略图显示

#### 任务31: 数据集管理页面实现
- [ ] **数据集管理**
  - [ ] 数据集列表组件（DatasetList）
  - [ ] 数据集卡片组件（DatasetCard）
  - [ ] 创建数据集对话框（DatasetCreateDialog）
  - [ ] 语料选择器组件（CorpusSelector）
  - [ ] 数据集统计显示

#### 任务32: 标签配置页面实现
- [ ] **标签体系管理**
  - [ ] 实体类型配置组件（EntityTypeConfig）
    - [ ] 实体类型列表（EntityTypeList）
    - [ ] 实体类型编辑表单（EntityTypeForm）
  - [ ] 关系类型配置组件（RelationTypeConfig）
    - [ ] 关系类型列表（RelationTypeList）
    - [ ] 关系类型编辑表单（RelationTypeForm）
  - [ ] **标签定义生成组件（DefinitionGenerator）** ⭐新增
    - [ ] 调用LLM生成详细定义
    - [ ] 生成标准定义、示例、辨析
  - [ ] **标签定义审核组件（DefinitionReview）** ⭐新增
    - [ ] 编辑生成的定义
    - [ ] 审核状态标识（待审核/已审核）
  - [ ] **标签体系版本管理组件（VersionManager）** ⭐新增
    - [ ] 版本快照创建对话框（VersionSnapshotDialog）
    - [ ] 版本列表展示
    - [ ] 版本激活/切换
    - [ ] 版本比较组件（VersionCompare）
    - [ ] 版本导出
  - [ ] 标签导入导出组件（LabelImportExport）
  - [ ] Agent Prompt预览组件（PromptPreview）
  - [ ] 标签颜色选择器

#### 任务33: 文本标注编辑器核心组件实现
- [ ] **文本标注编辑器**
  - [ ] 文本显示和选择功能（use-enhanced-text-selection）
  - [ ] 实体高亮显示组件（EntityHighlight）
  - [ ] 标签选择菜单组件（LabelSelector）
  - [ ] 实体列表面板（EntityList）
  - [ ] 关系列表面板（RelationList）
  - [ ] 偏移量计算和验证

#### 任务34: 关系标注可视化组件实现
- [ ] **关系标注**
  - [ ] SVG关系箭头层组件（RelationArrowLayer）
  - [ ] 关系创建交互（点击两个实体）
  - [ ] 关系编辑和删除功能
  - [ ] 箭头自动布局算法

#### 任务35: 图片标注编辑器组件实现
- [ ] **图片标注编辑器**
  - [ ] 图片查看器组件（ImageViewer）
  - [ ] **整图标注功能**（点击图片选择标签）
  - [ ] **区域标注功能**（拖拽绘制边界框）
  - [ ] 边界框编辑和删除功能
  - [ ] 图片缩放和平移功能
  - [ ] 坐标变换保持功能

#### 任务36: 标注编辑页面集成
- [ ] **标注编辑页面**
  - [ ] 集成文本标注编辑器和图片标注编辑器
  - [ ] 标注模式切换（实体模式/关系模式）
  - [ ] 版本历史显示和回滚功能
  - [ ] 保存和提交复核功能
  - [ ] 快捷键支持

#### 任务37: 批量标注功能实现
- [ ] **批量标注**
  - [ ] 批量标注触发按钮
  - [ ] 批量任务进度显示（实时更新）
  - [ ] 批量任务取消功能
  - [ ] 批量任务结果查看

#### 任务38: 复核页面实现
- [ ] **复核管理**
  - [ ] 复核任务列表组件（ReviewTaskList）
  - [ ] 标注结果查看器（只读模式）
  - [ ] 复核操作面板（批准/驳回/修改）
  - [ ] 复核意见输入
  - [ ] LLM纠正建议功能

#### 任务39: 数据导出功能实现
- [ ] **数据导出**
  - [ ] 导出配置对话框（状态筛选、格式选择）
  - [ ] 训练集/测试集划分配置
  - [ ] 按句子分类筛选
  - [ ] 导出进度显示
  - [ ] 文件下载功能

#### 任务40: Reward数据集生成功能实现
- [ ] **Reward数据集**
  - [ ] Reward数据集生成按钮
  - [ ] 修正统计显示
  - [ ] Reward数据预览
  - [ ] Reward数据导出

#### 任务41: 用户管理页面实现
- [ ] **用户管理**（管理员）
  - [ ] 用户列表组件
  - [ ] 用户创建对话框
  - [ ] 用户编辑和删除功能
  - [ ] 角色分配功能

#### 任务42: 登录和认证功能实现
- [ ] **认证系统**
  - [ ] 登录页面
  - [ ] JWT Token存储和管理
  - [ ] 路由守卫（权限检查）
  - [ ] 自动登出（Token过期）

#### 任务43: 前端UI优化和响应式设计
- [ ] **UI/UX优化**
  - [ ] 响应式布局（适配不同屏幕尺寸）
  - [ ] 加载状态和骨架屏
  - [ ] 错误提示和成功提示
  - [ ] 确认对话框（删除等危险操作）
  - [ ] 交互优化（防抖、节流）

### 通用组件

- [ ] **布局组件**
  - [ ] 顶部导航栏
  - [ ] 侧边菜单
  - [ ] 面包屑导航

- [ ] **业务组件**
  - [ ] 文件上传组件
  - [ ] 分页组件
  - [ ] 表格组件
  - [ ] 表单组件
  - [ ] 标注编辑器组件

- [ ] **工具组件**
  - [ ] Loading组件
  - [ ] 消息提示组件
  - [ ] 确认对话框组件

---

## 🔧 技术实现要点

### 1. 认证管理

```typescript
// 推荐实现
class AuthService {
  private token: string | null = null;
  
  async login(username: string, password: string) {
    const response = await api.post('/auth/login', { username, password });
    this.token = response.access_token;
    localStorage.setItem('token', this.token);
    return response;
  }
  
  getToken() {
    return this.token || localStorage.getItem('token');
  }
  
  isAuthenticated() {
    return !!this.getToken();
  }
  
  logout() {
    this.token = null;
    localStorage.removeItem('token');
  }
}
```

### 2. API封装

```typescript
// 推荐实现
class ApiService {
  private baseURL = 'http://localhost:8000/api/v1';
  
  async request(endpoint: string, options: RequestInit = {}) {
    const token = authService.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers
    };
    
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers
    });
    
    if (!response.ok) {
      if (response.status === 401) {
        authService.logout();
        router.push('/login');
      }
      throw new Error(await response.text());
    }
    
    return await response.json();
  }
}
```

### 3. 状态管理

```typescript
// 推荐状态结构
interface AppState {
  user: User | null;
  currentDataset: Dataset | null;
  labelSchema: {
    entityTypes: EntityType[];
    relationTypes: RelationType[];
  };
  annotationTask: AnnotationTask | null;
}
```

### 4. 路由守卫

```typescript
// 推荐实现
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = authService.isAuthenticated();
  
  if (requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});
```

---

## 📊 开发优先级

### 第一阶段：基础功能（1-2周）- 对应任务27-29

1. **前端项目初始化** ⭐⭐⭐ (任务27)
   - Vue3项目结构
   - Vue Router配置
   - Pinia状态管理
   - Axios封装
   - Element Plus配置
   - TypeScript类型定义

2. **API服务层和状态管理** ⭐⭐⭐ (任务28-29)
   - API封装（所有后端接口）
   - Pinia Store实现
   - 统一错误处理

3. **认证系统** ⭐⭐⭐ (任务42)
   - 登录页面
   - Token管理
   - 路由守卫
   - 权限检查

### 第二阶段：数据管理功能（1-2周）- 对应任务30-32

4. **Excel导入页面** ⭐⭐⭐ (任务30)
   - 文件上传组件
   - 处理进度显示
   - 语料预览列表
   - 按字段分类筛选
   - 图片缩略图显示

5. **数据集管理页面** ⭐⭐⭐ (任务31)
   - 数据集列表
   - 数据集卡片
   - 创建数据集对话框
   - 语料选择器
   - 数据集统计显示

6. **标签配置页面** ⭐⭐⭐ (任务32)
   - 实体类型配置（CRUD）
   - 关系类型配置（CRUD）
   - **标签定义生成功能**（LLM自动生成定义、示例、辨析）
   - **标签体系版本管理**（版本快照、切换、比较）
   - 标签导入导出
   - Agent Prompt预览

### 第三阶段：核心标注功能（2-3周）- 对应任务33-37

7. **文本标注编辑器** ⭐⭐⭐ (任务33-34)
   - 文本选择和高亮
   - 实体标注（创建、编辑、删除）
   - 实体列表面板
   - 偏移量计算和验证

8. **关系标注功能** ⭐⭐⭐ (任务34)
   - SVG关系箭头层
   - 关系创建交互
   - 关系列表面板
   - 箭头自动布局

9. **图片标注编辑器** ⭐⭐ (任务35)
   - 整图标注（点击选择标签）
   - 区域标注（拖拽绘制边界框）
   - 图片缩放和平移
   - 坐标变换保持

10. **标注编辑页面集成** ⭐⭐⭐ (任务36)
    - 文本和图片编辑器集成
    - 标注模式切换
    - 版本历史和回滚
    - 保存和提交复核
    - 快捷键支持

11. **批量标注功能** ⭐⭐ (任务37)
    - 批量标注触发
    - 实时进度显示
    - 任务取消
    - 结果查看

### 第四阶段：复核和导出功能（1-2周）- 对应任务38-40

12. **复核页面** ⭐⭐ (任务38)
    - 复核任务列表
    - 标注结果查看器（只读）
    - 复核操作面板
    - 复核意见输入
    - LLM纠正建议

13. **数据导出功能** ⭐⭐ (任务39)
    - 导出配置对话框
    - 状态筛选
    - 训练集/测试集划分
    - 按句子分类筛选
    - 导出进度显示

14. **Reward数据集生成** ⭐ (任务40)
    - 生成按钮
    - 修正统计显示
    - 数据预览
    - 数据导出

### 第五阶段：管理和优化（1周）- 对应任务41-45

15. **用户管理页面** ⭐ (任务41)
    - 用户列表
    - 用户CRUD
    - 角色分配

16. **UI优化和响应式设计** ⭐⭐ (任务43)
    - 响应式布局
    - 加载状态和骨架屏
    - 错误提示
    - 交互优化（防抖、节流）

17. **测试和文档** ⭐ (任务43.1, 44, 45)
    - 组件单元测试
    - 端到端测试
    - 用户手册
    - 部署文档

---

## 🎨 UI/UX建议

### 布局建议

```
+------------------+
|   顶部导航栏      |
+-----+------------+
| 侧  |            |
| 边  |   主内容区  |
| 菜  |            |
| 单  |            |
+-----+------------+
```

### 关键页面布局

1. **标注编辑器**（任务36）
   ```
   +----------------------------------+
   |  文本显示区（可选中标注）         |
   |  - 实体高亮显示                  |
   |  - 关系箭头层（SVG）             |
   +----------------------------------+
   |  图片显示区（如有关联图片）       |
   |  - 整图标注                      |
   |  - 区域标注（边界框）            |
   +----------------------------------+
   |  右侧面板                        |
   |  - 实体列表                      |
   |  - 关系列表                      |
   |  - 操作按钮                      |
   +----------------------------------+
   ```

2. **数据集管理**（任务31）
   - 卡片式展示
   - 快速操作按钮
   - 统计信息展示（总任务数、已标注数、已复核数）

3. **复核页面**（任务38）
   - 对比视图（原始标注 vs 当前标注）
   - 批注功能
   - 快速批准/驳回按钮

4. **标签配置页面**（任务32）
   - 左侧：实体类型列表
   - 右侧：关系类型列表
   - 底部：版本管理和导入导出
   - 弹窗：标签定义生成和审核

---

## 📚 参考资源

### 官方文档
- [前端对接指南](./FRONTEND_INTEGRATION_GUIDE.md) ⭐⭐⭐
- [原始需求文档](../../.kiro/specs/entity-relation-annotation-tool/requirements.md) ⭐⭐⭐
- [原始设计文档](../../.kiro/specs/entity-relation-annotation-tool/design.md) ⭐⭐⭐
- [原始任务列表](../../.kiro/specs/entity-relation-annotation-tool/tasks.md) ⭐⭐⭐
- [Swagger UI](http://localhost:8000/docs) ⭐⭐

### 示例代码
- 测试代码: `backend/tests/api/`
- API实现: `backend/api/`
- 参考项目: `参考项目代码/标注系统前端代码整理/`

### 工具推荐
- **API测试**: Postman, Insomnia
- **状态管理**: Pinia (Vue)
- **UI组件**: Element Plus
- **图表**: ECharts
- **图片标注**: Konva.js, Fabric.js

---

## ✅ 准备完成检查

在开始开发前，确认以下所有项目都已完成：

- [ ] 后端服务正常运行（`python main.py`）
- [ ] API文档已阅读（前端对接指南、原始需求文档、原始设计文档）
- [ ] 测试账号可以登录（admin/admin123）
- [ ] 核心API已测试通过（认证、语料、数据集、标注）
- [ ] 前端项目已初始化（Vue3 + Pinia + Element Plus）
- [ ] 开发环境已配置（环境变量、代理）
- [ ] 技术栈已选定（Vue3 + TypeScript + Element Plus）
- [ ] 功能模块已规划（按任务27-45组织）
- [ ] 已理解标签定义生成功能（LLM自动生成）
- [ ] 已理解标签体系版本管理功能（版本快照、切换、比较）
- [ ] 已理解图片标注的两种模式（整图标注 vs 区域标注）

**全部完成后，即可开始前端开发！** 🎉

---

## 🆘 遇到问题？

1. **后端问题**: 查看 [后端项目总览](./BACKEND_PROJECT_OVERVIEW.md)
2. **API问题**: 查看 [Swagger UI](http://localhost:8000/docs)
3. **数据模型**: 查看 [前端对接指南](./FRONTEND_INTEGRATION_GUIDE.md)
4. **需求理解**: 查看 [原始需求文档](../../.kiro/specs/entity-relation-annotation-tool/requirements.md)
5. **设计细节**: 查看 [原始设计文档](../../.kiro/specs/entity-relation-annotation-tool/design.md)
6. **任务规划**: 查看 [原始任务列表](../../.kiro/specs/entity-relation-annotation-tool/tasks.md)
7. **其他问题**: 提交Issue或查看测试代码

---

## 📝 重要提醒

### 与原始需求的关键对齐点

1. **标签定义生成功能**（任务32，需求3.1-3.6）
   - 用户创建标签时，可以调用LLM自动生成详细定义
   - 生成内容包括：标准定义、示例列表、类别辨析
   - 生成后需要人工审核确认
   - 只有已审核的标签才用于Agent的Prompt生成

2. **标签体系版本管理**（任务32，设计文档6.6节）
   - 支持创建版本快照（重大变更时）
   - 支持版本切换和激活
   - 支持版本比较（查看差异）
   - 每个数据集绑定到特定版本

3. **图片标注的两种模式**（任务35，需求12）
   - **整图标注**：将整张图片作为一个实体（bbox为null）
   - **区域标注**：在图片上框选特定区域（包含bbox坐标）
   - 需要在UI上明确区分这两种模式

4. **句子分类（text_type）**（需求1.6）
   - 每条语料记录都有字段来源分类
   - 包括：问题描述、原因分析、采取措施等
   - 导出时支持按分类筛选

5. **版本历史管理**（任务36，需求5.7-5.8）
   - 每次标注修改都创建版本记录
   - 支持查看版本历史
   - 支持回滚到指定版本

---

*最后更新: 2026-01-20*
*版本: 2.0 - 已对齐原始需求文档*
