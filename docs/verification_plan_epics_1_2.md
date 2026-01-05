# Verification Plan: Epics 1 & 2 - Foundation & Data Core

本计划用于验证已完成的基础架构和数据层功能，确保后续开发建立在稳定的底座之上。

## 📍 验证目标
1.  **进程集成**: 验证 Electron 稳定控制 Python 后端生命周期。
2.  **数据持久化**: 验证 SQLite 数据库正确创建并支持 UUID。
3.  **API 健壮性**: 验证 CRUD 接口逻辑正确且响应及时。
4.  **前端连通性**: 验证 React 能正确消费后端数据。

---

## 🧪 测试项目

### 1. 进程与联通性测试 (Epic 1)
*   **1.1 Backend Health**:
    *   方法: 访问 `http://localhost:8000/health`。
    *   预期: 返回 `{"status": "ok"}`。
*   **1.2 Python Startup**:
    *   方法: 查看终端日志，确认 Uvicorn 已启动。
    *   预期: 无 `Address already in use` 报错。

### 2. 数据库与 API 测试 (Epic 2)
*   **2.1 DB Schema Verification**:
    *   方法: 检查 `backend/learning.db` 文件。
    *   预期: 文件存在且大小大于 0。
*   **2.2 Create Media Record**:
    *   方法: 运行以下 PowerShell 命令：
      ```powershell
      Invoke-RestMethod -Uri http://localhost:8000/media -Method Post -ContentType "application/json" -Body '{"title": "Test Video", "file_path": "C:/test.mp4", "language": "en"}'
      ```
    *   预期: 返回含生成的 UUID 的 JSON 对象。
*   **2.3 List Media**:
    *   方法: `Invoke-RestMethod -Uri http://localhost:8000/media -Method Get`。
    *   预期: 包含刚刚创建的记录。

### 3. 前端集成测试 (Epic 2)
*   **3.1 React Query State**:
    *   方法: 打开应用，查看控制台或界面底部的 `Total Media in Library`。
    *   预期: 数字应从 `0` 变为测试创建的数量。
*   **3.2 Local Protocol Verification**:
    *   方法: 输入/选择一个有效的本地视频路径。
    *   预期: 视频能够加载缩略图并正常播放。

---

## 🛠️ 执行脚本
我将依次执行上述测试并记录结果。
