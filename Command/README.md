# Command 扩展

这个目录收录以“注册命令 / 通过命令触发能力”为核心的 Pi 扩展。

## 已收录
- [pi-diff-review](./pi-diff-review/) - 原生 diff 审查窗口扩展，通过 `/diff-review` 收集评审意见并插回 pi 编辑器
- [pi-review](./pi-review/) - 命令式代码审查扩展，支持 review uncommitted changes、branch、commit、PR 与 folder，并可用 `/end-review` 返回总结
- [pi-rollback](./pi-rollback/) - 分支感知的检查点与回滚扩展，支持 `/checkpoint` 打标、`/rollback` 退回更早节点，并自动保留被放弃分支的摘要
- [pi-smart-btw](./pi-smart-btw/) - 注册 `/btw` 命令，在后台拉起无会话子 Pi 处理离题问题，结果可选择性注入主对话
