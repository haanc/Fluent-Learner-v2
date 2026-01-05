# Implementation Plan: URL Import Flow (YouTube & Bilibili)

本计划旨在将 YouTube 和 Bilibili URL 导入设为应用的首选视频获取方式。

## 🎯 目标
*   [x] **即时流媒体 (Instant Streaming)**: 允许用户输入链接后立即在播放器中观看，无需等待下载完成。
*   [x] **元数据提取**: 解析 YouTube/Bilibili 视频标题、封面及时长。
*   [x] **背景处理**: 下载仅用于 AI 字幕生成的音频流，或者在用户要求时下载完整视频以供离线使用。

## 🛠️ 拟进行的更改

### Backend (Python + FastAPI) [COMPLETED]
*   **[MODIFY] [media_service.py](file:///c:/Users/hancao/.gemini/antigravity/scratch/language-learner/fluent-learner-v2/backend/media_service.py)**:
    *   [x] 更新 `fetch_metadata` 以提取 `url` (直接流地址)。 
    *   [x] **关键修复**: 强制 `yt-dlp` 仅选择 Progressive MP4，避免 HLS (.m3u8) 导致 Windows 播放失败。
*   **[MODIFY] [main.py](file:///c:/Users/hancao/.gemini/antigravity/scratch/language-learner/fluent-learner-v2/backend/main.py)**:
    *   [x] `POST /media/fetch-info` 返回包含 `stream_url` 的元数据。
    *   [x] **新增代理**: `/media/proxy` 处理跨域 (CORS) 和 Referer 防盗链，支持 Range Header 拖动。

### Frontend (React + Electron) [COMPLETED]
*   **[MODIFY] [App.tsx](file:///c:/Users/hancao/.gemini/antigravity/scratch/language-learner/fluent-learner-v2/src/App.tsx)**:
    *   [x] 获取元数据后，立即将 `videoPath` 设置为本地代理地址 (`http://127.0.0.1:8000/media/proxy...`)。
    *   [x] 实现“边看边下”逻辑。

## ✅ 验证计划

### 自动化/后端测试
*   **Metadata Extraction**: 传入一个 YouTube URL，验证是否能正确获取 Title。
    ```powershell
    Invoke-RestMethod -Uri http://localhost:8000/media/fetch-info -Method Post -Body '{"url": "https://www.youtube.com/watch?v=..."}'
    ```

### 手动验证
1.  在输入框粘贴 YouTube 链接，点击 Import。
2.  观察界面是否显示“正在提取信息...”。
3.  验证视频信息（时长、标题）是否正确存入数据库。
4.  视频下载完成后，验证播放器是否能正常播放通过 URL 导入的视频。
