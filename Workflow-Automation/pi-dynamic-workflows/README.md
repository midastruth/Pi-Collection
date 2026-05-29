# pi-dynamic-workflows

- **GitHub**: https://github.com/Michaelliv/pi-dynamic-workflows
- **npm**: `pi-dynamic-workflows`
- **主分类**: Workflow / Automation 扩展
- **标签**: `typescript`、`subagent`、`fan-out`、`experimental`、`local-only`
- **一句话总结**: 注册一个 `workflow` 工具，让模型自己写一段确定性 JavaScript 脚本，把任务 fan-out 到多个隔离子代理并行/流水执行，再汇总结果，对标 Claude Code 的 dynamic workflows。

## 功能说明
这是一个 Pi 扩展，灵感来自 Anthropic 在 Claude Code 中引入的 dynamic workflows。它给模型提供一个 `workflow` 工具：不再让单个 assistant 顺序做完所有事，而是由模型现写一小段 JS 脚本，通过 `agent()` / `parallel()` / `pipeline()` 把工作分散给多个隔离的 in-memory Pi 子代理，最后把结构化结果汇总回主 assistant。

脚本运行在 Node `vm` 沙箱中，并通过 acorn 做 AST 校验以保证确定性（禁用 `Date.now()`、`Math.random()`、`require`/`import`、网络/文件 API，以及 `meta` 中的模板插值、函数调用等），让 `meta` 可静态解析、运行可复现、攻击面更小。适合代码库审计、多视角评审、大型重构和 fan-out 研究类任务。

## 适用场景
- 代码库审计 / 多视角并行评审，需要把工作切成多个独立子任务。
- 大型重构前的 fan-out 调研（多个模块并行扫描后汇总）。
- 需要把多步骤、可并行的研究流程交给模型自行编排。
- 想要每个子任务在独立、干净的上下文中执行，避免主会话被噪声淹没。

## 核心机制
- **是否注册 command**: 否，无 slash 命令；通过自然语言请求触发模型调用工具。
- **是否注册 tool**: 是，注册 `workflow` 工具（内部还有一个 terminating 的 `structured_output` 工具支撑子代理结构化返回）。
- **是否监听 event / hook**: 是，监听 `session_start`，在会话启动时把 `workflow` 工具加入 active tools。
- **是否涉及 UI / notify**: 是，提供内联 live 进度视图（按 phase 分组显示子代理状态），`Esc` 可取消运行中的 workflow，活跃子代理被中止并标记 skipped。
- **是否依赖第三方服务**: 否，子代理为 in-memory Pi 会话，使用标准 coding 工具在本地运行；仅依赖 `acorn`，peer 依赖 `@mariozechner/pi-coding-agent`、`pi-tui`、`typebox`。

## 工作流脚本能力
- `agent(prompt, opts)`：拉起隔离子代理，返回最终文本；传 `opts.schema`（JSON Schema）则返回校验后的结构化对象。
- `parallel(thunks)`：并发执行一组 `() => agent(...)`，按输入顺序返回结果。
- `pipeline(items, ...stages)`：让每个 item 在 fan-out 的同时依次经过多个 stage，stage 接收 `(prev, original, index)`。
- `phase(title)`、`log(message)`、`args`、`cwd`、`budget`（token 预算追踪）等全局对象。
- 脚本第一条语句必须 `export const meta = {...}`（含 `name` snake_case、`description`、`phases`）。

## 安装与使用
- **安装方式**: `pi install npm:pi-dynamic-workflows`，或本地 `pi install /path/to/pi-dynamic-workflows`；安装后在 Pi 内执行 `/reload`。
- **配置要求**: 无额外配置，会话启动自动激活 `workflow` 工具。
- **基本使用方式**: 用自然语言请求，例如「Run a workflow to inspect this repository and summarize the main modules.」，模型会自行写脚本并调用 `workflow` 工具。

## 值得关注的点
- 用「模型写确定性 JS 脚本」而非固定命令来表达编排逻辑，灵活度高且天然支持并行/流水线。
- 通过 AST 校验 + vm 沙箱强约束确定性，是这类「让 LLM 写可执行脚本」方案中较克制、安全的做法。
- 子代理为 in-memory Pi 会话，具备完整 coding 工具，能读文件、跑 shell、做结构化输出。
- `structured_output` 工具带 `terminate: true`，子代理在该调用上直接结束，省掉一次多余 assistant 轮次。

## 限制与注意事项
- 作者明确标注为 **prototype**：尚未实现持久化/可恢复运行，也没有 `/workflows` 管理器。
- 由模型现写脚本执行，编排质量取决于模型对脚本约定的遵守程度。
- 多子代理并行会放大 token 消耗，虽有 `budget` 追踪但需自行关注成本。
- 当前判断基于 README、`package.json`、`extensions/workflow.ts` 与 `src/` 入口；脚本运行时细节需进一步阅读 `src/workflow.ts`、`src/agent.ts` 确认。

## 适合谁
- 需要把审计/评审/重构等任务拆成多子代理并行执行的 Pi 用户。
- 喜欢 Claude Code dynamic workflows 思路、想在 Pi 中获得类似能力的人。
- 想研究「LLM 写确定性脚本 + vm 沙箱 + in-memory 子代理」编排写法的开发者。

## 备注
- 与本仓库已收录的子代理类项目对比：`pi-subagents` / `pi-interactive-subagents` / `taskplane` 多以命令（`/run`、`/chain`、`/parallel`）或 dashboard 驱动多代理编排；pi-dynamic-workflows 则把编排逻辑交给模型现写的 JS 脚本表达，靠 `agent/parallel/pipeline` 原语 fan-out，定位更偏「可编程的一次性工作流」。
