# Implementation Plan - Epic 4: AI Intelligence Layer

本阶段的核心目标是将“被动观看”转化为“主动分析”。我们将实现一个完整的 AI 处理流水线：从视频中提取音频，利用 Whisper AI 生成精准的时间轴字幕，并最终在以库的形式展示给用户。

## 🏗️ 架构概览 (Architecture Overview)

我们将采用 **异步任务队列 (Asynchronous Pipeline)** 模式来处理耗时的 AI 任务，避免阻塞主界面。

```mermaid
graph TD
    A[Frontend (React)] -->|Import URL| B(Backend API)
    B -->|Start Background Task| C{Task Manager}
    C -->|1. Download| D[yt-dlp]
    D -->|2. Extract Audio| E[FFmpeg]
    E -->|3. Transcribe| F[Whisper AI API]
    F -->|4. Save Segments| G[(SQLite DB)]
    
    H[frontend Polling/WS] <-->|Check Status| I[Database Status]
```

## 🧩 组件拆解 (Component Breakdown)

### 1. 数据层 (Data Layer)
我们需要追踪每个视频的处理状态，以便在前端展示进度条或错误信息。

*   **[MODIFY] `MediaSource` Model**:
    *   新增 `status` 字段: `ENUM('pending', 'downloading', 'processing_audio', 'transcribing', 'ready', 'error')`
    *   新增 `error_message` 字段: 记录失败原因。
    *   新增 `cover_image` 字段: 存储本地封面路径（之前只存了 URL）。

### 2. 后端服务 (Backend Services)
后端将分为三个主要服务模块：

*   **[NEW] `AudioProcessor` (ffmpeg wrapper)**:
    *   **功能**: 将 `mp4` 视频转换为符合 Whisper API 要求的小体积 `mp3` 或 `m4a` 文件。
    *   **依赖**: 系统需安装 `ffmpeg`。
*   **[NEW] `AIService` (Whisper Client)**:
    *   **功能**: 调用 OpenAI (或 Groq/Deepgram) 接口。
    *   **输入**: 音频文件路径。
    *   **输出**: 结构化的 JSON 字幕数据 list[`start`, `end`, `text`]。
    *   **Prompt工程**: 优化 Prompt 以确保生成结果包含标点符号，并按句子切分。
*   **[MODIFY] `MediaService`**:
    *   串联 `Download` -> `AudioProcess` -> `Transcribe` -> `DB Save` 的完整业务逻辑。

### 3. 前端界面 (Frontend UI)
*   **[NEW] `LibraryView` (Resource Hub)**:
    *   **功能**: 网格化展示所有已导入的视频（显示封面、标题、状态标签）。
    *   **交互**: 
        *   点击 "Ready" 状态的视频 -> 进入播放器。
        *   点击 "Processing" 视频 -> 显示加载中。
        *   右键菜单 -> 删除/重新处理。
*   **[MODIFY] `App.tsx` (Router)**:
    *   引入 React Router，区分 `Home/Library` 和 `Player` 页面。

## 📋 实施步骤 (Implementation Steps)

### Step 4.1: Database Migration & Status Tracking
*   更新 `sqlmodel` 定义，添加状态字段。
*   在后端实现简单的状态流转逻辑。

### Step 4.2: Library UI (The Bookshelf)
*   实现 `LibraryGrid` 和 `VideoCard` 组件。
*   从 `GET /media` 获取数据并渲染。

### Step 4.3: Audio Extraction Pipeline
*   集成 `ffmpeg-python` 或直接子进程调用。
*   实现 `extract_audio(video_path) -> audio_path`。

### Step 4.4: Whisper AI Integration
*   接入 `openai` Python SDK。
*   实现 `transcribe_audio(audio_path) -> segments`。
*   **关键点**: 处理长音频（Whisper API 有 25MB 限制，可能需要切片，或者使用更高效的 `distil-whisper` 等服务）。

### Step 4.5: End-to-End Wiring
*   将 URL Import 的后台任务扩展为完整流水线。
*   前端自动轮询状态，直到视频变为 `Ready`。

## 🧪 验证计划 (Verification Plan)

### 自动化测试
*   **Unit Test**: 测试 `AudioProcessor` 能正确生成音频文件。
*   **Integration Test**: Mock OpenAI 响应，验证从“音频输入”到“数据库记录”的流程。

### 手动验证
1.  **导入流程**: 导入一个 YouTube 短视频。
2.  **观察状态**: 在 Library 页面看到卡片状态从 Downloading -> Processing -> Ready 变化。
3.  **最终效果**: 点击进入播放器，侧边栏显示 AI 生成的字幕，且与语音精确同步。
