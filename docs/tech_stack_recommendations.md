# 技术栈选型建议：Language Learning Assistant

为了实现 **“交互式播放器 + 即时查词”** 的核心目标，UI 的渲染能力（特别是富文本和媒体叠加）将成为最大的技术挑战。

以下提供三个方向的架构建议，从 **“体验上限”** 到 **“开发效率”** 依次排列。

---

## 方案 A: 现代混合架构 (Modern Hybrid) - 🥇 推荐
**核心理念**：用 Web 技术做 UI（最擅长处理文字排版和媒体），用 Python 做逻辑。这是目前开发“漂亮桌面应用”的主流方式（如 VS Code, Obsidian）。

| 维度 | 技术选型 | 理由 |
| :--- | :--- | :--- |
| **前端 (Frontend)** | **Electron + React (Vite)** | • **UI 能力无敌**：实现“视频上悬浮可点击字幕”非常简单（绝对定位+CSS）。<br>• **生态丰富**：拥有现成的 Video Player 组件、Markdown 渲染器。<br>• **TailwindCSS**：快速实现现代、响应式的设计（符合你对美观的要求）。 |
| **后端 (Backend)** | **FastAPI (Local Server)** | • Python 依然是核心。Electron 启动时在后台静默启动一个 FastAPI 服务。<br>• 前后端通过 HTTP/WebSocket 通信。<br>• **模块化**：强制分离 UI 和 业务逻辑。 |
| **数据库 (DB)** | **SQLite + SQLModel** | • **SQLModel**：基于 Pydantic，既是 ORM 又是数据验证，非常适合 FastAPI。<br>• 轻量、单文件、无需安装服务器。 |
| **优点** | **体验最好**。能轻松实现极为复杂的交互（如划词高亮、动效）。 |
| **缺点** | **架构复杂**。需要维护 JS/TS 和 Python 两套环境；打包体积较大。 |

---

## 方案 B: 专业原生架构 (Professional Native) - 🥈 稳健
**核心理念**：保持纯 Python 栈，但升级 GUI 框架以获得更强的媒体支持。

| 维度 | 技术选型 | 理由 |
| :--- | :--- | :--- |
| **前端 (Frontend)** | **PySide6 (Qt for Python)** | • **工业级标准**：Qt 是最强大的桌面 GUI 库。<br>• **多媒体强**：`QMediaPlayer` 原生支持视频播放和叠加层。<br>• **QWebEngine**：如果需要复杂排版，甚至可以嵌入迷你浏览器视窗。 |
| **后端 (Backend)** | **Python Services (Modular)** | • 传统的 MVC 模式。<br>• Controller 层直接调用 Service 层函数（无需 HTTP 开销）。 |
| **数据库 (DB)** | **SQLite + Peewee** | • **Peewee**：比 SQLModel 更轻量，可以说是 Python 中最简单的 ORM。<br>• 非常适合桌面单机应用。 |
| **优点** | **纯 Python**。性能优异，分发方便（打包体积小于 Electron）。 |
| **缺点** | **学习曲线陡峭**。Qt 的 API 庞大且复杂，自定义精美 UI（尤其是非标准控件）比 Web 难得多。 |

---

## 方案 C: 快速迭代架构 (Iterative MVP) - 🥉 现状延伸
**核心理念**：不换框架，硬啃 CustomTkinter 的能力边界。

| 维度 | 技术选型 | 理由 |
| :--- | :--- | :--- |
| **前端 (Frontend)** | **CustomTkinter + python-vlc** | • **现状延续**：无需重写现有界面。<br>• **vlc 集成**：将 VLC 窗口嵌入 Tkinter Frame（技术上有坑，但可行）。<br>• **交互限制**：在视频上做“可点击字幕”非常非常难，可能需要另辟蹊径（如字幕显示在视频下方而非浮层）。 |
| **后端 (Backend)** | **Python Services (Modular)** | • 沿用现有代码。 |
| **数据库 (DB)** | **SQLite (Raw/Native)** | • 直接写 SQL，或者用标准库 `sqlite3`。 |
| **优点** | **启动最快**。如果你只想尽快验证“播放视频”这个功能。 |
| **缺点** | **体验上限低**。Tkinter 难以实现现代化的动态交互效果；VLC 嵌入往往会有窗口遮挡/焦点抢占问题。 |

---

## 💡 我的建议

考虑到您的目标是 **“桌面级”** 且 **“交互式”** (Interactive)，以及您提到的“不要 Redux”、“模块化”：

**我强烈建议选择【方案 A (Electron + FastAPI)】的变体，或者【方案 B (PySide6)】。**

但如果您希望 **完全保留 Python** 且 **不引入 JS/Web 复杂度**，请选择 **方案 B (PySide6)**。

**如果您想先试试“深水”：**
我们可以先尝试 **方案 C (当前架构)** 的 **"Tech Spike" (技术探针)**：
> *挑战：在现在的 CustomTkinter 窗口里嵌入一个 VLC 播放器，看看能不能接受它的效果。*

如果效果不好，我们再果断切换到 Electron 或 PySide6。

您倾向于哪种路径？
1. **拥抱 Web 技术** (Electron) -> 最佳交互上限。
2. **坚守 Python 原生** (PySide6) -> 最佳性能/一致性。
3. **试试看现有架构** (CustomTkinter) -> 最低成本验证。
