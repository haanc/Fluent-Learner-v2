# 用户认证与订阅方案 (Updated for WeChat & Email)

基于您的具体需求（邮箱 + 微信扫码）以及未来的多设备同步规划，我们采纳 **方案 A (Modern Auth)** 的变体。

---

## 🏗️ 核心架构: Supabase + WeChat Bridge

我们使用 **Supabase** 作为唯一的用户数据库，但由于 Supabase 原生不直接支持“微信扫码（PC端）”，我们需要构建一个轻量级的桥接层。

### 1. 认证方式 (Authentication Methods)

| 方式 | 体验 | 技术实现 |
| :--- | :--- | :--- |
| **邮箱登录** | 标准流程 | **Supabase Auth 原生支持**。直接调用 `supabase.auth.signUp()` 和 `signInWithPassword()`。 |
| **微信扫码** | 扫码即登录 | **Supabase Edge Functions** (无服务器函数) + 微信开放平台 API。 |

### 2. 微信扫码登录流程 (WeChat Scan Flow)

这是一个由于微信限制而必须要走的“标准复杂流程”。

1.  **前端请求**：用户点击“微信登录”，Electron 应用生成一个唯一的 `session_id`。
2.  **展示二维码**：应用内显示微信官方授权页 URL (嵌入 WebView 或 iframe)。
    *   `https://open.weixin.qq.com/connect/qrconnect?appid=...&redirect_uri=YOUR_CALLBACK_URL`
3.  **用户扫码**：用户手机扫码并确认。
4.  **回调处理 (Cloud)**：
    *   微信服务器回调我们的 **Supabase Edge Function**。
    *   Function 拿到 `code` -> 换取 `access_token` 和 `openid`。
    *   **关键步骤**：Function 在 Supabase `auth.users` 表中查找该 `openid`。
        *   **如果存在**：生成一个自定义 JWT Token。
        *   **如果不存在**：自动创建一个新用户 (Shadow User)，并生成 Token。
    *   Function 将 Token 存入 Redis 或 临时数据库表，关联到 `session_id`。
5.  **前端轮询**：Electron 应用轮询检查 `session_id` 的状态，一旦获取到 Token，标记登录成功。

---

## 💰 订阅与功能锁 (Subscription & Gating)

### 策略：Lazy Auth (延迟转化)
用户下载应用后，**默认进入游客模式**，无需登录即可使用基础功能。

| 功能 | 游客 (Guest) | 免费用户 (Free Tier) | 订阅用户 (Pro) |
| :--- | :--- | :--- | :--- |
| **本地播放** | ✅ 无限 | ✅ 无限 | ✅ 无限 |
| **基础查词** | ✅ 每日 10 次 | ✅ 每日 50 次 | ✅ 无限 |
| **AI 深度分析** | ❌ 锁定 | ❌ 锁定 | ✅ 无限 (合理上限) |
| **云端同步** | ❌ 不可用 | ❌ 不可用 (或仅同步部分) | ✅ 实时同步 |

### 支付集成
*   推荐使用 **LemonSqueezy** (支持支付宝/微信支付)。
*   **流程**：
    1.  应用内点击 "Upgrade"。
    2.  弹出 LemonSqueezy 支付链接。
    3.  支付成功 -> Webhook 通知 Supabase -> 更新 `users` 表 `is_pro = true`。
    4.  应用端通过 Supabase Realtime 监听到字段变化，瞬间解锁界面，撒花🎉。

---

## 📝 您的准备工作 (Prerequisites)

为了实现微信登录，您需要准备：
1.  **微信开放平台账号 (open.weixin.qq.com)**：注意不是公众平台。
2.  **企业认证**：微信扫码登录通常只对**已认证的企业**开放（个人开发者较难申请）。
    *   *如果暂时只有个人身份，建议先只做邮箱登录，微信登录作为 Phase 2。*

---

## ✅ 总结
我们现在的技术栈锁定为：
*   **App**: Electron + React
*   **Backend**: Supabase (Auth + DB + Edge Functions/Python API)
*   **Payment**: LemonSqueezy
