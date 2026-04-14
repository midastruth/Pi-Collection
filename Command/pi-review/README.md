# pi-review

- **GitHub**: [https://github.com/earendil-works/pi-review](https://github.com/earendil-works/pi-review)
- **主分类**: Command 扩展
- **标签**: `typescript`, `local-only`, `production-oriented`, `requires-config`
- **一句话总结**: 通过 `/review` 和 `/end-review` 为 pi 增加一套可落地的代码审查流程，支持审查未提交改动、分支、提交、PR 或指定目录，并可把审查结果总结后带回主会话。

## 功能说明
`pi-review` 的核心是把“让 agent 做 code review”变成一个明确的命令式工作流，而不是只给一段 prompt。它提供 `/review` 与 `/end-review` 两个命令，支持审查未提交改动、相对基线分支的改动、某个 commit、GitHub PR，以及指定文件夹/文件快照；同时内置了较完整的 review rubric、优先级规则、人类 reviewer callouts 要求，以及返回原会话后的总结/修复衔接逻辑。源码里还实现了 review branch 状态持久化、会话 widget、自定义 review 指令和项目级 `REVIEW_GUIDELINES.md` 读取机制。

## 适用场景
- 想在 pi 里建立更标准化的代码审查流程，而不是临时手写“帮我 review 一下”
- 需要针对 uncommitted changes、feature branch、单个 commit 或 GitHub PR 做审查
- 希望把 review 放到独立会话/分支中执行，结束后再把审查结论总结或排队修复回主分支

## 核心机制
- **是否注册 command**: 是；注册 `/review` 与 `/end-review`
- **是否注册 tool**: 否；当前未见面向 agent 的 tool 注册
- **是否监听 event / hook**: 是；监听 `session_start` 与 `session_tree`，用于恢复 review 状态、设置 widget 和共享自定义指令
- **是否涉及 UI / notify**: 是；包含 selector、editor、loader、widget、通知，以及交互式选择 review 目标/结束方式
- **是否依赖第三方服务**: 可选依赖 GitHub CLI `gh`；仅在 review PR 时需要，用于读取 PR 信息并 checkout 到本地

## 安装与使用
- **安装方式**: `pi install git:github.com/earendil-works/pi-review`
- **配置要求**: 基本要求是在 Git 仓库中运行；如需 review GitHub PR，需要本机安装并登录 `gh`；可选在项目 `.pi` 同级目录放置 `REVIEW_GUIDELINES.md` 作为共享审查规则
- **基本使用方式**: 可直接执行 `/review` 打开交互式目标选择器，也可使用 `/review uncommitted`、`/review branch main`、`/review commit abc123`、`/review pr 123`、`/review folder src docs` 等直接进入；结束时执行 `/end-review`，可选择仅返回、返回并总结，或返回并排队修复发现的问题

## 值得关注的点
- 不只是发起一次 review prompt，而是把“选择审查对象 → 在独立 review branch 中执行 → 回到原位置 → 总结或推进修复”做成闭环
- 内置较完整的 review rubric，包含优先级、fail-fast error handling、human reviewer callouts 等规则，输出约束比较强
- 支持共享自定义 review instructions，并且会自动读取项目级 `REVIEW_GUIDELINES.md`，适合团队统一审查偏好
- `/end-review` 能把 review 分支总结成结构化 handoff，甚至直接发送 follow-up 让 agent 修复 findings，这点很适合作为实际工作流使用

## 限制与注意事项
- 这是以命令与会话导航为核心的本地 Git 工作流扩展，不适合脱离仓库上下文的普通聊天场景
- PR review 依赖本地 `gh` 可用且已登录，且 checkout PR 前要求工作树没有会阻碍切换分支的已跟踪改动
- 仓库当前是单文件实现，功能集中但也意味着后续扩展或定制时需要自行读懂较长的 `review.ts`
- `REVIEW_GUIDELINES.md` 不是强制配置，但如果团队有固定审查规则，最好配合使用，否则主要依赖扩展内置 rubric

## 适合谁
- 想在 pi 中常态化执行 code review 的个人开发者或团队
- 需要把“审查”和“编码”会话分离，同时保留回跳与总结能力的用户
- 想参考 Pi 命令扩展如何结合 session tree、交互式 UI 和 GitHub CLI 的开发者

## 备注
虽然它也带有 UI、session state 和可选 GitHub PR 集成，但用户最直接的使用入口与核心价值仍然是 `/review` / `/end-review` 这组命令，因此主分类优先归入 Command 扩展。