# Workflow / Automation 扩展

这个目录收录偏流程编排、自动执行、多步骤串联的 Pi 扩展。

## 已收录
- [pi-interactive-subagents](./pi-interactive-subagents/) - 异步子代理编排扩展，支持多窗格并行执行、结果回灌与 artifact 共享
- [pi-subagents](./pi-subagents/) - 通用子代理编排扩展，支持 `/run`、`/chain`、`/parallel`、Agents Manager、async 状态追踪与 worktree 隔离并行
- [taskplane](./taskplane/) - 面向 pi 的多代理任务编排系统，支持分波执行、review、merge 与本地 dashboard
- [pi-autoresearch](./pi-autoresearch/) - 自动实验优化循环扩展，支持 benchmark 执行、自动提交/回滚、dashboard 导出与 finalize 收尾流程
- [pi-dynamic-workflows](./pi-dynamic-workflows/) - 注册 `workflow` 工具，让模型写确定性 JS 脚本，用 `agent`/`parallel`/`pipeline` 把任务 fan-out 到多个隔离子代理并汇总，对标 Claude Code dynamic workflows
