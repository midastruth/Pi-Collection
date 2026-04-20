# pi-jarvis

- **GitHub**: [https://github.com/fluxgear/pi-jarvis](https://github.com/fluxgear/pi-jarvis)
- **主分类**: UI / Notification 扩展
- **标签**: `typescript`, `local-only`, `production-oriented`
- **一句话总结**: 为 Pi 增加一个 `/jarvis` 侧边对话 overlay，让用户能在不打断主会话的情况下开一个可持久化的辅助线程，并按权限把信息回传主会话。

## 功能说明
这个仓库的核心不是单纯新增一个命令，而是提供一个 **side conversation UI**：用户执行 `/jarvis` 后，会在当前 Pi 会话里打开一个悬浮 overlay，和独立的 side session 对话。该 side session 默认跟随主模型，也可以用 `/jarvis-model` 单独固定模型；同时可以按开关决定是否允许本地 `read` / `bash` / `edit` / `write` / `mcp` 能力，以及是否允许向主会话发送 note 或 redirect。扩展还会持续汇总主会话状态、当前焦点、最近变化与最近转录片段注入给 side session，让 `/jarvis` 更像“旁路助手”而不是另一个完全失联的窗口。

## 适用场景
- 想在主任务继续进行时，开一个独立小窗口做快速提问、排障、总结或 triage
- 需要一个不会直接污染主线程上下文的辅助助手，但又希望它知道主会话最近在做什么
- 想把某些建议先在 side session 里整理，再选择是否 note/redirect 回主会话

## 核心机制
- **是否注册 command**: 是；注册 `/jarvis` 与 `/jarvis-model`
- **是否注册 tool**: 是，但主要在 side session 内动态注册 `jarvis_send_follow_up_to_main` 与 `jarvis_send_steer_to_main` 两个桥接工具
- **是否监听 event / hook**: 是；监听 `session_start`、`agent_start`、`agent_end`、`message_start/update/end`、`tool_execution_start/end`、`model_select`、`session_shutdown`，并在 side session 中使用 `before_agent_start` 注入上下文与权限提示
- **是否涉及 UI / notify**: 是；核心能力就是 overlay UI、状态栏、通知、确认弹窗与侧会话展示
- **是否依赖第三方服务**: 否；主要依赖本地 Pi 运行环境，`mcp` 能力仅在安装 `pi-mcp-adapter` 时可用

## 安装与使用
- **安装方式**: README 写法是 `npm install pi-jarvis`，然后在 Pi 中注册扩展入口 `./dist/index.js`；`package.json` 也包含 `pi.extensions` 字段，说明它按 Pi package 形式发布，但当前仓库 README 主要展示的是手动注册流程
- **配置要求**: 默认即可运行；是否开放 repo tools、是否允许 note/redirect 主会话主要通过 overlay 中的开关控制
- **基本使用方式**: 执行 `/jarvis` 打开 overlay；也可以直接 `/jarvis <问题>` 发送首条消息；用 `/jarvis-model <provider/model>` 固定 side session 模型，或 `/jarvis-model follow-main` 恢复跟随主模型

## 值得关注的点
- 不是简单新开一个会话，而是把 **主会话摘要 + 最近变化 + recent transcript** 注入到 side session，使它能理解“主线程现在在干什么”
- 权限边界做得比较细：repo tools、note main、redirect 三个能力默认关闭，避免 side assistant 悄悄改文件或误导主线程
- side session 有独立持久化历史，关闭 overlay 后再次打开仍能续上之前的 `/jarvis` 对话
- 对主会话的 redirect 强制确认，交互安全性比“直接替主线程发消息”更稳妥
- 处理了模型跟随、模型固定、MCP 可用性、thinking 流渲染和 overlay 文本清洗等细节，成熟度不错

## 限制与注意事项
- 它更适合“辅助对话”和“旁路排障”，不是多代理自动编排框架
- side session 能否直接用本地工具，取决于用户是否在 overlay 中显式打开 `Repo tools`
- `mcp` 只在当前环境能解析到 `pi-mcp-adapter` 时可用，不是无条件内置
- README 安装说明偏手动注册路径；若要作为标准 Pi package 直接安装，建议在真实 Pi 环境再确认最佳安装方式

## 适合谁
- 希望在 Pi 里有一个不打断主线程的“第二思考通道”的用户
- 经常需要边做主任务边查上下文、看日志、总结下一步的开发者
- 想参考 Pi overlay、side session、主从会话桥接实现方式的扩展作者

## 备注
当前判断基于 README、`package.json`、`index.ts`、`overlay.ts`、`side-session.ts`、`main-context.ts`。它虽然注册了命令和桥接工具，但仓库最核心的价值是“提供一个可交互的 side-conversation overlay UI”，因此优先归为 UI / Notification 扩展，而不是 Command 或 Workflow / Automation。
