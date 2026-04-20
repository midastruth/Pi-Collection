# pi-subagents

- **GitHub**: [https://github.com/nicobailon/pi-subagents](https://github.com/nicobailon/pi-subagents)
- **主分类**: Workflow / Automation 扩展
- **标签**: `typescript`, `local-only`, `production-oriented`
- **一句话总结**: 为 Pi 提供可复用的子代理编排层，支持单 agent 委派、链式流程、并行执行、异步后台运行、Agents Manager TUI，以及与 `pi-intercom` 的会话协调。

## 功能说明
这是一个以 **subagent 编排** 为核心的 Pi 扩展，不只是单一工具或命令集合。它提供 `subagent` / `subagent_status` 两个工具，也提供 `/run`、`/chain`、`/parallel`、`/agents`、`/subagents-status` 等用户入口，用来把任务分发给内置或自定义 agent，并在链式步骤、并行任务、后台执行、artifact、会话日志和状态追踪之间打通。仓库还内置 `scout`、`planner`、`worker`、`reviewer`、`researcher`、`delegate` 等 agent，并支持 `.chain.md` 链文件、技能注入、模型/工具/扩展隔离、git worktree 并行隔离和管理型 CRUD 操作，完成度很高。

## 适用场景
- 希望把复杂任务拆成“调研 → 规划 → 实施 → 评审”等多阶段流程
- 需要多个子代理并行执行，并且希望保留 async 状态、artifact、日志与运行历史
- 想在 Pi 中建立可复用的 agent / chain 体系，而不是每次临时手写 prompt

## 核心机制
- **是否注册 command**: 是；至少包含 `/run`、`/chain`、`/parallel`、`/agents`、`/subagents-status`，并注册 `Ctrl+Shift+A` 快捷键
- **是否注册 tool**: 是；注册 `subagent` 与 `subagent_status`
- **是否监听 event / hook**: 是；监听 `session_start`、`session_shutdown`、`tool_result` 以及 `subagent:started` / `subagent:complete` 等事件
- **是否涉及 UI / notify**: 是；包含 Agents Manager overlay、chain clarify TUI、async 状态 overlay、状态 widget、slash result 渲染与完成通知扩展
- **是否依赖第三方服务**: 否；核心能力主要依赖本地 Pi 运行环境与已配置模型 provider，但部分增强能力可选依赖 `pi-intercom`、`pi-web-access`、`pi-mcp-adapter`、`pi-prompt-template-model`

## 安装与使用
- **安装方式**: `pi install npm:pi-subagents`
- **配置要求**: 开箱可用，内置 agent 可直接使用；如需自定义 agent / chain，可在 `~/.pi/agent/agents/`、`~/.agents/`、项目 `.pi/agents/` 或旧版 `.agents/` 中写 markdown 定义；可选配置文件为 `~/.pi/agent/extensions/subagent/config.json`
- **基本使用方式**: 安装后可直接执行 `/run <agent> <task>`、`/chain ...`、`/parallel ...`，也可用 `Ctrl+Shift+A` 打开 Agents Manager；如果让主 agent 自动调用，则通过 `subagent` 工具传入 `agent`、`tasks` 或 `chain` 参数完成委派

## 值得关注的点
- 同时覆盖 **单次委派、链式流水线、并行 fan-out/fan-in、后台异步运行**，不是只做最小化 subagent demo
- Agent 定义能力很完整：支持 frontmatter 中的模型、fallbackModels、thinking、skills、tools、extensions、prompt 继承策略、递归深度等控制
- 除了执行外，还提供 agent / chain 的管理能力，LLM 可通过 `action: list|get|create|update|delete` 动态维护定义
- 对实际开发流程很友好：支持 chain artifacts、run history、session logs、output 截断、debug artifacts、git worktree 隔离并行
- 与 `pi-intercom` 联动后，可让子代理在运行中向 orchestrator 定向提问或回传完成摘要，适合更复杂的多代理协作

## 限制与注意事项
- 功能面很广，上手门槛高于简单命令型扩展，需要理解 agent frontmatter、chain、skills、async、worktree 等概念
- 一些高级能力是可选集成，不安装 `pi-intercom`、`pi-web-access`、`pi-mcp-adapter` 等扩展时，对应能力不会生效
- `worktree: true` 要求处于 git 仓库且工作区干净，否则无法安全启用并行隔离
- 当前设计明显偏本地工作站式编排，不是远程托管型多代理平台

## 适合谁
- 想把 Pi 升级成可复用多代理工作流系统的高级用户
- 需要长期维护 agent 角色库、链模板和异步执行流程的个人开发者或小团队
- 想研究 Pi 中 subagent orchestration、TUI 管理器、技能注入和本地会话协调实现方式的扩展作者

## 备注
当前判断基于 README、`package.json`、`index.ts`、`slash-commands.ts`、`agents.ts`、`skills.ts`、`intercom-bridge.ts` 与 `notify.ts`。虽然它同时具备 tool、command、UI 和 event 特征，但最核心的价值仍是“把多个专用 agent 组织成可复用的自动化流程”，因此优先归为 Workflow / Automation 扩展。
