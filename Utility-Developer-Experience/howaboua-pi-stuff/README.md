# howaboua-pi-stuff

- **GitHub**: https://github.com/IgorWarzocha/howaboua-pi-stuff
- **npm scope**: `@howaboua/*`（bun workspaces monorepo）
- **主分类**: Utility / Developer Experience 扩展
- **标签**: `skill-collection`、`monorepo`、`typescript`、`production-oriented`、`requires-config`
- **一句话总结**: 作者 IgorWarzocha 的 Pi 工具箱 monorepo，把自己日常使用的一整套 Pi 扩展与 skills 拆成独立 npm 包，并提供 `pi-stuff` / `pi-extensions` / `pi-skills` 三个聚合 bundle 一键安装。

## 功能说明
这是一个 bun workspaces monorepo，集中维护作者围绕"raw Pi 会话 + 清晰上下文边界 + review pass"工作流所用的全部扩展与 skill。每个能力都是独立发布的 npm 包，既可单独安装，也可通过三个聚合包整套拉取。仓库本身不是单一扩展，而是这套工具集的发布源与统一入口（含 changeset 发布、聚合包同步等脚本）。

该仓库的价值在于：它代表一种"不造一整套假操作系统、只用少量扩展把长会话维持下去"的实战工作流，并把这套工作流对应的工具逐一拆解成可单独取用的包。

## 收录的包

### 聚合 Bundle
- `@howaboua/pi-stuff` — extensions + 可共享 skills 的完整套装（不含 codex-conversion、omarchy）。
- `@howaboua/pi-extensions` — 全部扩展（不含 pi-codex-conversion）。
- `@howaboua/pi-skills` — 全部可共享 skills（不含 omarchy-help）。

### Extensions
- `pi-codex-conversion` — Codex 风格工具面（`exec_command` / `write_stdin` / `apply_patch`、图片工具、Codex web search、prompt/tool 适配）。**已单独收录于 [Tool/pi-codex-conversion](../../Tool/pi-codex-conversion/)**。
- `pi-auto-reasoning-tool` — 提供 `change_reasoning` 工具，agent 可按任务形态自行调高/调低 reasoning level，运行结束后自动恢复到会话初始级别。
- `pi-auto-trees` — `/marker` 标记返回点、`/end` 总结自上次 marker 以来的工作并跳回检查点、把结果压缩成分支摘要后推进 marker，专为长会话设计。
- `pi-subagent-review` — `/review` 隔离评审子代理，自动判断 base 分支与改动范围、生成评审上下文摘要、把 findings 作为咨询性意见回灌主会话，仿照 Codex CLI 的 `/review`。
- `pi-semantic-grep` — `semantic_grep` 语义检索工具，基于本地 SQLite 索引 + OpenAI 兼容 embeddings，按"含义"而非字面查代码/文档，会话启动时增量刷新索引。
- `pi-vent` — `vent` 工具，把反复出现的工作流摩擦记录到 `VENT.md`。**已单独收录于 [Tool/pi-vent](../../Tool/pi-vent/)**。
- `pi-explore-subagents` — `explore_subagent` 工具，启动 discovery-only（不改文件）的浅/深探索子代理，把陌生代码库的侦察工作隔离在主会话之外。
- `pi-markdown-workflows` — `/skills`、`/workflows` 统一 GUI，支持 workflow 捕获、`/learn`、嵌套 `AGENTS.md` 上下文加载；UI primitives 已抽成独立 npm SDK。
- `pi-smart-btw` — 副会话提问，结果需显式注入主会话，避免离题跑偏主线程。**已单独收录于 [Command/pi-smart-btw](../../Command/pi-smart-btw/)**。
- `pi-memories` — 极简本地记忆：在 `session_shutdown` 时跑一个无 tools/skills 的临时 Pi 会话，提炼值得长期记住的内容并追加到全局 `AGENTS.md` 收件箱，由人工审阅决定取舍。

### Skills
- `pi-skill-agent-native-hardening` — 对 agent 生成代码做加固/审计：减少 godfile、明确所有权、降重、提升可遍历性。
- `pi-skill-anti-ai-copy` — 改写文案使其更具体、更像真人，去掉 SaaS 宣传腔。
- `pi-skill-chrome-cdp` — 基于 Chrome DevTools Protocol 的浏览器检查/控制（移植自 `pasky/chrome-cdp-skill`）。
- `pi-skill-gh-issue-pr-flow` — 基于 `gh` 的通用 GitHub issue/PR 工作流（分支、校验、PR body、review triage）。
- `pi-skill-project-reference-research` — 把外部/本地仓库作为参考上下文查阅，返回带证据的结论。
- `pi-skill-skill-creator` — 帮助设计、撰写、打包并收紧可复用的 agent skill。
- `pi-skill-omarchy-help`（不入 bundle）— Arch + Omarchy 工作站维护，建议单独安装并按自己机器定制。

## 适用场景
- 想整套采用作者的长会话工作流（探索→marker→实现→review→PR→hardening→end）。
- 只想取其中某个能力（如 `semantic_grep`、`/review`、`explore_subagent`、`change_reasoning`）单独安装。
- 作为"如何用少量扩展把 raw Pi 会话维持得可控"的参考样板。
- 学习一个多包 Pi 扩展 monorepo 的组织、发布与聚合方式。

## 核心机制
- **是否注册 command**: 是（如 `/marker`、`/end`、`/review`、`/skills`、`/workflows`、`/btw` 等，分散在各子包）。
- **是否注册 tool**: 是（`change_reasoning`、`semantic_grep`、`explore_subagent`、`vent`、Codex 风格工具等）。
- **是否监听 event / hook**: 是（如 pi-memories 监听 `session_shutdown`、pi-auto-reasoning-tool 在 agent run 后恢复 reasoning level、pi-semantic-grep 会话启动时刷新索引）。
- **是否涉及 UI / notify**: 是（pi-markdown-workflows 统一 GUI、pi-subagent-review 编辑器上方 widget 等）。
- **是否依赖第三方服务**: 部分依赖（pi-semantic-grep 需 OpenAI 兼容 embeddings 端点；pi-codex-conversion 面向 Codex/GPT provider；chrome-cdp 需本地 Chrome）。

## 安装与使用
- **安装方式**:
  - 完整套装：`pi install npm:@howaboua/pi-stuff`
  - 仅扩展：`pi install npm:@howaboua/pi-extensions`
  - 仅 skills：`pi install npm:@howaboua/pi-skills`
  - 单个包：`pi install npm:@howaboua/pi-<name>`（如 `pi-semantic-grep`、`pi-subagent-review`）
- **配置要求**: 视具体包而定；semantic-grep 需配置 embeddings 端点，codex-conversion 需对应 provider。其余多数为零配置或本地运行。
- **基本使用方式**: 安装后按各子包说明使用命令/工具；作者在 README 给出了一条完整的端到端会话工作流参考。

## 值得关注的点
- 一处仓库即可看到作者完整的"扩展 + skill"组合拳，且每个能力都拆成可单独取用的包，取舍自由度高。
- 三个聚合 bundle 的设计（全套 / 仅扩展 / 仅 skills）方便按需安装。
- 其中 pi-vent、pi-smart-btw、pi-codex-conversion 此前已作为独立仓库单独收录，本仓库是它们的 monorepo 发布源。
- README 中给出的工作流（marker/review/hardening）本身是有参考价值的方法论，而非单纯功能罗列。
- 作者额外推荐了若干非本仓库 skill（impeccable、make-interfaces-feel-better、design.md、agent-pages、React Grab）。

## 限制与注意事项
- Pi 包以本地权限运行，安装前应自行审阅源码（作者本人也在 README 中提醒这一点）。
- monorepo 整体处于活跃迭代，各子包版本独立，能力与命令面可能随版本变化。
- 部分包有外部依赖（embeddings 端点、Chrome、特定 provider），并非全部开箱即用。
- 本记录基于 README、package.json 与各子包 README 整理，个别命令/参数细节需进一步阅读源码确认。

## 适合谁
- 想要一套经过实战打磨、可整套或拆件取用的 Pi 工具集的用户。
- 偏好"少量扩展 + 清晰上下文边界 + review pass"而非重型 agent 编排的人。
- 想参考多包 Pi 扩展 monorepo 工程化（changeset 发布、聚合包同步）的开发者。

## 备注
- 仓库内 `pi-vent`、`pi-smart-btw`、`pi-codex-conversion` 已分别单独收录，本条目作为其聚合发布源与整套工具箱的总入口，不重复展开这三个包。
