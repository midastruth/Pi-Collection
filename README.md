# Pi Extensions Collection

这是一个按分类整理的 Pi 扩展 / Skills 资料库。

- 根目录 `README.md` 只用作导航目录
- **详细记录放在各分类文件夹中**
- 每个仓库使用单独文件夹保存，便于后续继续补充截图、源码笔记、安装说明等内容

## 分类目录
- [Command 扩展](./Command/)
- [Tool 扩展](./Tool/)
- [Event / Hook 扩展](./Event-Hook/)
- [UI / Notification 扩展](./UI-Notification/)
- [Workflow / Automation 扩展](./Workflow-Automation/)
- [Integration 扩展](./Integration/)
- [Template / Example 扩展](./Template-Example/)
- [Utility / Developer Experience 扩展](./Utility-Developer-Experience/)

## 当前已收录
- [pi-skills](./Utility-Developer-Experience/pi-skills/) - 跨多种 agent 生态的 skills 集合仓库，包含搜索、浏览器自动化、转录、VS Code diff、Google CLI 等能力
- [pi-telegram](./Integration/pi-telegram/) - Telegram 私聊桥接扩展，可把当前 pi 会话接到 Telegram Bot 上
- [pi-intercom](./Integration/pi-intercom/) - 本地会话间 1:1 通信扩展，支持定向发消息、等待回复与 overlay UI
- [pi-diff-review](./Command/pi-diff-review/) - 原生 diff 审查窗口扩展，通过 `/diff-review` 收集评审意见并插回 pi 编辑器
- [pi-review](./Command/pi-review/) - 命令式代码审查扩展，支持 review uncommitted changes、branch、commit、PR 与 folder，并可用 `/end-review` 返回总结
- [pi-model-switch](./Tool/pi-model-switch/) - 为 agent 提供 `switch_model` 工具，可列出、搜索并切换当前会话模型
- [pi-web-search](./Tool/pi-web-search/) - 提供 `web_search` 与 `url_context` 工具，支持联网搜索与 URL 内容分析
- [pi-interactive-subagents](./Workflow-Automation/pi-interactive-subagents/) - 异步子代理编排扩展，支持多窗格并行执行与结果异步回灌
- [taskplane](./Workflow-Automation/taskplane/) - 面向 pi 的多代理任务编排系统，支持分波执行、review、merge 与本地 dashboard
- [pi-autoresearch](./Workflow-Automation/pi-autoresearch/) - 自动实验优化循环扩展，支持 benchmark 执行、结果保留/回滚、dashboard 与 finalize skill
- [pi-updater](./Utility-Developer-Experience/pi-updater/) - pi 本体自动更新扩展，支持启动检查、npm 安装升级与会话重启
- [pi-rollback](./Command/pi-rollback/) - 分支感知的检查点与回滚扩展，支持 `/checkpoint` 打标、`/rollback` 退回更早节点，并自动保留被放弃分支的摘要

## 说明
如果后续新增仓库：
1. 先判断主分类
2. 在对应分类目录下创建仓库文件夹
3. 将详细分析写入该仓库文件夹下的 `README.md`
4. 再回到根目录 `README.md` 补充导航链接
