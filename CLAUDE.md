# LinguaMaster 项目 Claude 配置

## 🚨 重要文件保护规则

以下文件是项目工作记录的核心文件，**绝对不能删除**：

| 文件 | 用途 |
|------|------|
| `task_plan.md` | 项目任务计划和进度追踪 |
| `findings.md` | 技术调研和问题解决记录 |
| `progress.md` | 工作日志和测试结果 |

### ⛔ 禁止操作

1. **不要删除**上述三个文件
2. **不要在清理操作中移除**这些文件
3. 这些文件已在 `.gitignore` 中排除，但**不代表可以删除**

### ✅ 正确做法

- 这些文件用于 `planning-with-files` 工作流
- 每次开始新任务时更新 `task_plan.md`
- 每次发现新知识时更新 `findings.md`
- 每次完成工作时更新 `progress.md`

---

## 项目结构

```
fluent-learner-v2/
├── backend/           # FastAPI 后端
│   ├── main.py
│   ├── routes/
│   └── ai/
├── electron/          # Electron 主进程
│   └── main.ts
├── src/               # React 前端
├── docs/              # 文档
│   ├── Project Daily Summary/
│   └── Plan-and-decision/
├── task_plan.md       # ⚠️ 不要删除
├── findings.md        # ⚠️ 不要删除
└── progress.md        # ⚠️ 不要删除
```

---

## 开发环境

### 启动开发服务器

```bash
# Windows (PowerShell)
cd /mnt/c/Users/hancao/.gemini/antigravity/scratch/language-learner/fluent-learner-v2
powershell.exe -Command "npm run dev"
```

### 构建安装包

```bash
powershell.exe -Command "npm run build:full"
```

---

## 版本信息

- 当前版本: v0.2.0
- GitHub: https://github.com/haanc/LinguaMaster
