# 部署指南

## 架构概览

```
用户浏览器
    │
    ├─→ 前端（Vercel）
    │       Vue 3 + Vite 静态资源
    │       域名：https://your-app.vercel.app
    │
    └─→ 后端（阿里云服务器）
            FastAPI + SQLite
            域名：http://your-server-ip:18080
            或绑定域名：https://api.your-domain.com
```

前后端分离部署：前端托管在 Vercel（免费），后端运行在阿里云服务器（持久化存储）。

---

## 一、前端部署（Vercel）

### 前置条件

- GitHub 仓库已推送最新代码
- Vercel 账号已注册并绑定 GitHub

### 部署步骤

**1. 导入仓库**

打开 [vercel.com/new](https://vercel.com/new)，选择 `multimodal-excel-system` 仓库。

**2. 配置 Root Directory**

在 "Configure Project" 页面，将 **Root Directory** 改为 `frontend`（默认是根目录，必须修改）。

Vercel 会自动识别 Vite 框架，构建命令和输出目录无需手动填写（已由 `frontend/vercel.json` 定义）。

**3. 配置环境变量**

在 **Environment Variables** 中添加：

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `VITE_BACKEND_ORIGIN` | 后端服务完整 URL（**必填**） | `http://your-server-ip:18080` |

> 如果后端绑定了域名并配置了 HTTPS，填 `https://api.your-domain.com`。

**4. 点击 Deploy**

部署完成后，记录 Vercel 分配的域名（如 `https://multimodal-excel-system.vercel.app`），后端 CORS 配置需要用到。

### 后续更新前端

每次 `git push` 到 `main` 分支，Vercel 自动触发重新部署，无需手动操作。

---

## 二、后端部署（阿里云服务器）

> 当前阶段项目尚在开发中，本节为**预期部署方案**，待项目稳定后执行。

### 前置条件

- 阿里云 ECS 服务器（Linux，推荐 Ubuntu 22.04）
- 已安装：Python 3.10+、Git
- 服务器安全组已开放 18080 端口

### 1. 拉取代码

```bash
cd ~
git clone git@github.com:Bpig-C/multimodal-excel-system.git app
cd app
```

### 2. 创建 Python 虚拟环境并安装依赖

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
vim .env
```

必填项：

```env
# 数据库路径（绝对路径）
DATABASE_URL=sqlite:////home/your_user/app/data/database/annotation.db

# DashScope API Key（LLM 功能必填）
DASHSCOPE_API_KEY=sk-your-key

# 前端 Vercel 域名（CORS，必填）
CORS_ORIGINS=https://multimodal-excel-system.vercel.app
```

### 4. 初始化数据库

```bash
python init_db.py
```

### 5. 验证启动

```bash
uvicorn main:app --host 0.0.0.0 --port 18080
```

访问 `http://your-server-ip:18080/docs` 确认 API 正常。确认无误后 Ctrl+C 停止，继续配置守护进程。

### 6. 配置 systemd 守护进程（开机自启 + 崩溃自动重启）

创建服务文件：

```bash
sudo vim /etc/systemd/system/multimodal-backend.service
```

填入以下内容（替换 `your_user` 为实际用户名）：

```ini
[Unit]
Description=Multimodal Excel System Backend
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/home/your_user/app/backend
Environment="PATH=/home/your_user/app/backend/venv/bin"
EnvironmentFile=/home/your_user/app/backend/.env
ExecStart=/home/your_user/app/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 18080
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启用并启动：

```bash
sudo systemctl daemon-reload
sudo systemctl enable multimodal-backend
sudo systemctl start multimodal-backend
sudo systemctl status multimodal-backend
```

### 7. 配置 Vercel 环境变量

后端启动后，回到 Vercel 控制台：

**Settings → Environment Variables → 编辑 `VITE_BACKEND_ORIGIN`**

填入服务器地址（如 `http://your-server-ip:18080`），然后在 **Deployments** 页手动触发一次 Redeploy。

---

## 三、常用运维命令

### 后端服务管理

```bash
# 查看运行状态
sudo systemctl status multimodal-backend

# 查看实时日志
sudo journalctl -u multimodal-backend -f

# 重启服务
sudo systemctl restart multimodal-backend

# 停止服务
sudo systemctl stop multimodal-backend
```

### 更新后端代码

```bash
cd ~/app
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt   # 依赖有变化时执行
sudo systemctl restart multimodal-backend
```

### 数据备份

```bash
# 备份数据库
cp ~/app/data/database/annotation.db ~/backup/annotation_$(date +%Y%m%d).db

# 备份上传文件
tar -czf ~/backup/uploads_$(date +%Y%m%d).tar.gz ~/app/data/uploads/
```

---

## 四、环境变量汇总

### 前端（Vercel Environment Variables）

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `VITE_BACKEND_ORIGIN` | ✅ | 后端服务完整 URL |
| `VITE_API_BASE_URL` | 可选 | API 路径前缀，默认 `/api/v1` |

### 后端（服务器 `.env` 文件）

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `DATABASE_URL` | ✅ | SQLite 数据库路径 |
| `DASHSCOPE_API_KEY` | ✅ | 阿里云 DashScope API Key |
| `CORS_ORIGINS` | ✅ | 前端 Vercel 域名，多个用逗号分隔 |
| `HOST` | 可选 | 监听地址，默认 `0.0.0.0` |
| `PORT` | 可选 | 监听端口，默认 `18080` |
| `STORAGE_TYPE` | 可选 | 存储类型，默认 `local` |
| `LLM_TIMEOUT_SECONDS` | 可选 | LLM 超时，默认 `120` |

---

## 五、当前进度

| 步骤 | 状态 |
|------|------|
| 前端 Vercel 配置（`vercel.json`、`build` 脚本）| ✅ 已完成 |
| 后端 CORS 环境变量化 | ✅ 已完成 |
| `backend/.env.example` | ✅ 已完成 |
| GitHub 仓库推送 | ✅ 已完成 |
| Vercel 实际部署 | ⏳ 待执行（项目功能稳定后）|
| 阿里云后端部署 | ⏳ 待执行（项目功能稳定后）|
