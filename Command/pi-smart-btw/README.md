# pi-smart-btw

- **GitHub**: https://github.com/IgorWarzocha/pi-smart-btw （已迁移，跳转占位）
- **当前源码**: [howaboua-pi-stuff/packages/pi-smart-btw](https://github.com/IgorWarzocha/howaboua-pi-stuff/tree/main/packages/pi-smart-btw)（见 [Utility-Developer-Experience/howaboua-pi-stuff](../../Utility-Developer-Experience/howaboua-pi-stuff/)）
- **npm**: `@howaboua/pi-smart-btw`
- **主分类**: Command 扩展
- **标签**: `side-session`、`async`、`subagent`、`requires-config`、`typescript`
- **一句话总结**: 注册 `/btw <question>` 命令，在后台拉起一个全新的无会话 Pi RPC 子进程作为"临时副会话"回答问题，结果默认只显示在 transcript，需要时再一键注入回主对话。

## 功能说明
为主会话提供一个"顺便问一下"的旁路通道：使用 `/btw` 提出与当前任务无关的问题，扩展会用 `pi --mode rpc --no-session` 拉起一个干净上下文的子进程异步处理，主会话立即返回继续工作。答案以自定义 transcript 消息渲染（通过 `context` hook 从 LLM 上下文中过滤掉），用户用快捷键决定是否把 Q/A 注入回主线、是否丢弃；可在同一副会话里继续 `/btw` 追问，多轮 Q/A 在注入时按顺序合并成一段提示。

## 适用场景
- 主任务执行中突然想到一个不相关问题，又不想污染当前上下文
- 想用一个"干净的 Pi"快速验证某个事实、命令、报错含义
- 需要把一组离题问答整理后再有选择地塞进主线 prompt
- 想保留主会话上下文窗口，把杂项探索放到独立子进程

## 核心机制
- **是否注册 command**: 是，仅 `/btw`
- **是否注册 tool**: 否
- **是否监听 event / hook**: 是，注册 `context` hook 过滤掉副会话消息以免污染主 LLM 上下文；监听 `session_shutdown` 停止子进程
- **是否涉及 UI / notify**: 是，使用 `pi.ui.setWidget` 在编辑器上方渲染状态块（运行中 / 已就绪 / 失败），并注册自定义 message renderer 显示 Q/A 卡片；注册 `alt+z` 预填、`alt+c` 注入、`alt+x` 关闭三个全局快捷键
- **是否依赖第三方服务**: 否，完全本地；依赖 `pi` 二进制的 `--mode rpc --no-session` 能力
- **子进程通信**: 通过 stdin/stdout 行式 JSON-RPC 与子进程交互（`get_state`、`set_auto_compaction`、`set_auto_retry`、`prompt`），通过 `agent_end` + idle + 静默窗口判断回答完成
- **防嵌套**: 子进程设置环境变量 `PI_SMART_BTW_CHILD=1`，扩展入口检测到后直接跳过注册，避免无限递归

## 安装与使用
- **安装方式**:
  - 永久安装：`pi install npm:@howaboua/pi-smart-btw`
  - 单次试用：`pi -e npm:@howaboua/pi-smart-btw`
- **配置要求**: 首次加载会在 `~/.pi/agent/pi-smart-btw.json` 写出默认配置，可改 `model`（默认 `openai-codex/gpt-5.4-mini`）、`provider`、`thinking`、`command`（默认 `pi`），以及三个快捷键
- **基本使用方式**:
  - `/btw <question>` 发起或追问
  - `alt+z` 在编辑器中预填 `/btw `
  - `alt+c` 把所有已完成的 Q/A 注入主会话（idle 时直接发送，否则按 `followUp` 投递）
  - `alt+x` 关闭副会话并清空状态

## 值得关注的点
- 子进程加载用户已安装的扩展和 skills（**不**带 `--no-skills`），所以副会话也具备完整工具能力
- 副会话答案默认与主 LLM 上下文物理隔离，用 `context` hook 过滤自定义消息类型，避免"假装独立但其实污染上下文"的常见反模式
- 多轮注入时使用编号 Q/A 列表，prompt 结构稳定可被主 agent 直接消化
- 单文件入口 + 三个 src 文件，代码极简，可作为"用 RPC 起子 Pi"的参考样板

## 限制与注意事项
- 同时只支持一个活跃的副会话（一组 Q/A），重新 `/btw` 复用同一个子进程
- 子进程使用固定的 RPC 超时（ready 10s、单次响应 30s）和"静默 500ms 判定完成"的启发式，重负载或慢模型场景可能误判
- 默认模型写死为 `openai-codex/gpt-5.4-mini`，需要在 JSON 配置中自行调整
- 仅在 pi CLI 上下文里有意义，对没有 RPC 模式的运行环境不可用

## 适合谁
- 喜欢用 Pi 跑长任务但常被临时问题打断的用户
- 想要"干净上下文 + 完整工具"的人，作为 `pi-subagents`/`pi-jarvis` 之外更轻量的旁路问答
- 想学习如何用 `pi --mode rpc` 包子进程并把结果回灌主会话的开发者

## 备注
- 与本仓库已收录的相近项目对比：
  - 与 `pi-jarvis` 相比：jarvis 是侧边 overlay 持续对话，pi-smart-btw 偏单次/少量轮次的离题问答，且显式区分"显示"与"注入"
  - 与 `pi-subagents`/`pi-interactive-subagents` 相比：那些偏多代理编排和并行流水线，pi-smart-btw 仅服务用户自己的临时问题，不做工作流串联
- 当前版本代码量很小，行为可一眼读完。
- 该包已迁入作者的 monorepo `howaboua-pi-stuff`，原独立仓库现仅保留跳转指引（旧文档存于 `README.legacy.md`），npm 安装方式不变（`@howaboua/pi-smart-btw`）。
