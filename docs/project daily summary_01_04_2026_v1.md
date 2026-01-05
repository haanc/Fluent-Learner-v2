# 项目开发日报 (2026-01-04)

## 📅 今日概要
今天是项目功能爆发的一天。我们不仅构建了稳健的 **Sync 云端同步** 和 **多用户隔离** 基础设施，还重点攻克了应用的核心价值模块——**AI 智能辅导 (AI Tutor)** 与 **SRS 单词复习系统**。不仅实现了从“看视频”到“学单词”的完整闭环，还完成了复习算法的底层实现，解决了多个复杂的后端数据一致性与前端交互 Bug。

## ✨ 新增功能 (Features)

### 1. AI 智能辅导集成 (LangChain + LangGraph Architecture)
*   **架构升级**: 正式引入了 **LangChain** 和 **LangGraph** 作为 AI 服务的底层编排框架。
    *   **Workflow**: 在 `backend/ai/graph.py` 中实现了基于图 (Graph) 的状态机，用于管理 AI 导师的多轮对话上下文。
    *   **Chains**: 在 `backend/ai/chains.py` 中封装了特定的 Prompt Chains，分别用于 `Contextual Dictionary` (上下文查词) 和 `Grammar Explainer` (语法解析)。
*   **功能表现**:
    *   **上下文查词**: AI 提供翻译时会强制结合当前视频字幕语境。
    *   **语境解析**: `/ai/explain` 接口支持对长难句进行语法拆解。
    *   **AI 导师对话**: 实现了多轮对话接口，允许用户就视频内容提问。
*   **前端交互**: 实现了悬浮菜单 (Selection Menu)，用户划词即可唤起 AI 解释或保存到生词本。

### 2. SRS 间隔重复复习系统 (Review System)
*   **功能描述**: 在后端完整实现了 **SM-2 记忆算法**，为每个单词计算最佳复习时间。
*   **核心逻辑**:
    *   **Review API**: 开发了 `/vocab/{id}/review` 接口，接收用户打分 (0-5)。
    *   **算法实现**: 根据用户评分动态更新 `interval` (间隔天数)、`repetition` (重复次数) 和 `easiness_factor` (难度因子)。
    *   **自动调度**: 系统自动根据 `next_review_at` 字段，在生词本中筛选出 "Due" (到期) 的单词，提示用户 "Review (N)"。

### 3. 智能生词本 (Smart Vocabulary Notebook)
*   **功能描述**: 打造了一个集管理与复习于一体的单词中心。
*   **核心能力**:
    *   **复习模式**: 结合 SRS 算法，支持一键筛选 "Today's Review" 单词。
    *   **单词卡片**: 展示单词、翻译、例句，以及对应的视频来源跳转。
*   **交互实现**: 开发了 `NotebookView.tsx`，与后端 `/vocab` 接口对接，支持流畅的增删改查。

### 4. Supabase 云同步与多用户隔离
*   **双向同步**: 点击 "Sync" 按钮，一键同步本地生词和在线视频记录 (含 Payload 去重逻辑)。
*   **云端占位**: 视频仅同步元数据，节省本地空间。
*   **多用户隔离**: 通过后端 `owner_id` 字段与 API 拦截器，实现了完美的本地多用户/游客数据隔离。

## 🐛 修复的关键 Bug (Critical Fixes)

### 1. **SRS 复习功能崩溃 (AttributeError: 'easiness_factor')**
*   **现象**: 当用户尝试复习单词或加载生词本时，后端报错 `AttributeError`。
*   **原因**: 后端 Code 更新了算法字段，但 SQLite 数据库文件未迁移，缺少列。
*   **修复**: 编写 `migrate_db.py` 脚本，手动追加了 `interval`, `easiness_factor`, `repetitions`, `next_review_at` 等字段。

### 2. **保存单词崩溃 (IntegrityError / UUID)**
*   **现象**: AI 查词后保存时报错。
*   **修复**: 增加了后端对 `media_id` 字符串的手动 UUID 转换处理。

### 3. **Sync 重复键冲突 (ON CONFLICT)**
*   **现象**: 同步时报错 `command cannot affect row a second time`。
*   **修复**: 在前端同步服务中实现了严格的数据去重逻辑 (Deduplication)。

### 4. **Login 后 Sync 网络错误**
*   **修复**: 修复了 API Client 的 Header 注入逻辑，确保 `owner_id` 正确传递。

### 5. **启动白屏**
*   **修复**: 补全了丢失的 `handleLogout` 函数及 Import。

## 🚀 下一步计划 (Next Steps)
1.  **AI Graph 深度应用**: 利用 LangGraph 实现更复杂的“情景模拟对话”功能。
2.  **UI 实装**: 开发互动式的 Flashcard 复习界面。
3.  **移动端适配**: 优化小屏体验。
