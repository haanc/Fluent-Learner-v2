# Project Phase 1 Detailed Plan v1: The Interactive Player

这个文档将 Phase 1 拆解为可执行的微小步骤。每一步都是一个独立的commit点。

## 🏗️ Epic 1: Scaffold & Tech Spike (基础架构与技术探针) [DONE]
目标：搭建 Electron + React + Python 环境，并验证视频播放能力。

### Step 1.1: Project Init (Hello World)
*   **用途**: 建立纯净的项目骨架。
*   **技术**: `npm create electron-vite`, React, TypeScript.
*   **实现**: 创建 `fluent-learner-v2` 目录，清理默认模板代码，确保能 `npm run dev` 启动一个显示 "Hello World" 的窗口。
*   **验证**: 看到白色窗口，控制台无报错。

### Step 1.2: Python Backend Integration
*   **用途**: 验证 Electron 主进程能启动 Python 子进程。
*   **技术**: `python-shell` 或使用 Node `child_process.spawn`. FastAPI (Python).
*   **实现**: 创建 `backend/main.py` (FastAPI)，在 Electron 启动时在后台静默启动它。
*   **验证**: Electron 前端访问 `localhost:8000/health` 能收到 `{status: "ok"}`。

### Step 1.3: HTML5 Video Verification
*   **用途**: 验证不需要复杂的 native player，只需 `<video>` 标签即可播放本地文件。
*   **技术**: React `<video>`, Electron `protocol.registerFileProtocol` (解决本地文件安全策略问题)。
*   **实现**: 在界面放一个 `<video src="file:///C:/test.mp4">`，并确保它能播放。
*   **验证**: 视频成功加载和播放，声音正常。

### Step 1.4: Overlay Interaction Spike
*   **用途**: 验证核心体验——“视频上的文字”。
*   **技术**: CSS Absolute Positioning, `z-index`.
*   **实现**: 在视频上方覆盖一个半透明的 `div`，里面写一行字 "Click Me"。点击它弹出 `alert`，而不影响视频播放（不暂停）。
*   **验证**: 文字悬浮在视频上，点击文字视频继续播放，点击交互响应灵敏。

---

## 💾 Epic 2: Data Core (数据内核) [DONE]
目标：建立基于 UUID 的 SQLite 数据库，并打通前后端数据流。

### Step 2.1: Python SQLModel Setup
*   **用途**: 定义数据结构。
*   **技术**: SQLModel (Python), SQLite.
*   **实现**: 创建 `backend/database.py` 和 `backend/models.py`。定义 `MediaSource` 和 `SubtitleSegment` 类。
*   **验证**: 运行脚本能生成 `learning.db` 文件。

### Step 2.2: Python CRUD API
*   **用途**: 前端操作数据的接口。
*   **技术**: FastAPI Routes.
*   **实现**: 编写 `/api/media/list`, `/api/media/create` 等基础接口。
*   **验证**: 使用 Postman 或 Swagger UI 能成功插入和查询数据。

### Step 2.3: Frontend Data Hook
*   **用途**: 前端优雅地调用后端。
*   **技术**: React Query (TanStack Query), Axios.
*   **实现**: 封装 `useMediaList()` hook。
*   **验证**: React 组件能渲染出从 Python 后端读来的列表（即便是空列表）。

---

## 🌊 Epic 3: URL Intelligence & Import (智能导入)
目标：实现以 URL 为核心的资源获取流程。

### Step 3.1: URL Metadata Extraction
*   **用途**: 解析 YouTube/Bilibili 视频元数据。
*   **技术**: `yt-dlp` (Python).
*   **实现**: `/api/media/fetch-info` 接收 URL，返回标题、时长、缩略图。
*   **验证**: 输入 Bilibili 链接，后端成功返回对应的视频标题。

### Step 3.2: URL Input UI
*   **用途**: 提供直观的输入入口。
*   *技术**: React Header Input.
*   **实现**: 在 Header 增加输入框，点击后显示 Loading 状态并触发 Step 3.1。
*   **验证**: 粘贴链接点击导入，界面显示正确的视频预览。

### Step 3.3: Background Download & Processing
*   **用途**: 将流媒体转为可本地处理的文件。
*   **技术**: FastAPI BackgroundTasks, `yt-dlp`.
*   **实现**: 后台下载视频至 `cache/` 目录，并更新 `MediaSource` 的 `file_path`。
*   **验证**: 下载完成后，对应的资源在 Library 中可见且可播放。

---

## 🎬 Epic 4: The Immersive Player (核心播放器) [CURRENT]
目标：实现“视频 + 滚动字幕”的完整交互。
*(注意：此处已部分实现 UI，需对接 Step 3.3 后的真实文件)*
