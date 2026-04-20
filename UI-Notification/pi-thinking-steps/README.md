# pi-thinking-steps

- **GitHub**: [https://github.com/fluxgear/pi-thinking-steps](https://github.com/fluxgear/pi-thinking-steps)
- **主分类**: UI / Notification 扩展
- **标签**: `typescript`, `local-only`, `experimental`
- **一句话总结**: 重写 Pi 的 thinking 显示层，把原始 provider reasoning 渲染成 `collapsed` / `summary` / `expanded` 三种更易读的终端视图。

## 功能说明
这个仓库的核心目标是改善 **Pi TUI 中的 thinking 可读性**，而不是增加新的 agent 能力。它提供 `/thinking-steps` 命令和 `Alt+T` 快捷键，让用户在三种 thinking 显示模式之间切换，并在底部状态栏持续显示当前模式。实现上它会跟踪 assistant thinking 的开始、增量与结束状态，然后通过运行时 patch Pi 内部 `AssistantMessageComponent`，把默认 thinking 渲染替换成自定义结构化终端视图，支持摘要行、完整步骤展开、活动 pulse、列表/标题/代码片段的终端友好渲染。

## 适用场景
- 想在 Pi 中更清楚地查看模型 thinking，而不是看原始噪声较大的 reasoning 文本
- 需要快速扫读一长段推理过程，判断模型当前在检查、比较、规划还是验证什么
- 希望在真实终端环境里保留较紧凑的 UI，同时在需要时再展开完整 thinking 步骤

## 核心机制
- **是否注册 command**: 是；注册 `/thinking-steps`
- **是否注册 tool**: 否；未注册给 agent 调用的业务工具
- **是否监听 event / hook**: 是；监听 `session_start`、`message_start`、`message_update`、`message_end`、`agent_end`、`session_shutdown` 等事件维护 thinking 状态与 patch 生命周期
- **是否涉及 UI / notify**: 是；核心就是 thinking 区域的自定义渲染、状态栏模式提示与切换通知
- **是否依赖第三方服务**: 否；不依赖外部 API，但依赖 Pi 当前内部 TUI 实现细节

## 安装与使用
- **安装方式**: README 示例为 `pi -e ./index.ts` 直接加载仓库入口；`package.json` 也带有 `pi.extensions`，说明可作为 Pi 扩展包加载
- **配置要求**: 无明显额外配置；运行在 Pi 终端 UI 中即可
- **基本使用方式**: 安装后执行 `/thinking-steps` 交互选择模式，或直接 `/thinking-steps collapsed|summary|expanded`；也可用 `Alt+T` 快速轮换模式

## 值得关注的点
- 价值非常聚焦：只解决 **thinking 呈现质量**，不试图扩展 workflow 或工具层能力
- 提供三种模式，兼顾“低噪音监看”和“完整推理复查”两类需求
- 对 markdown-like thinking 内容做了终端友好的二次渲染，包括标题、列表、代码 span、强调文本和 ANSI/控制序列清洗
- patch 层单独隔离在 `internal-patch.ts`，并做了可逆、引用计数和兼容性校验，工程实现相对克制

## 限制与注意事项
- 这是明显依赖 **Pi 内部实现** 的扩展，而不是只基于稳定公开 API；Pi 内部组件一变，扩展可能就需要跟着更新
- 核心实现是 monkey patch 内部 `AssistantMessageComponent`，维护风险高于普通 command / tool 扩展
- 它改善的是“显示方式”，不会改变模型 thinking 的实际内容和质量
- 当前更适合在真实终端 TUI 中使用；如果 Pi 后续渲染体系变化，效果和兼容性都可能受影响

## 适合谁
- 经常查看模型 thinking，并希望 reasoning 更清晰可扫读的重度 Pi 用户
- 对终端可读性、推理轨迹展示质量比较敏感的开发者
- 想参考 Pi 内部渲染 patch、状态驱动 thinking UI 实现方式的扩展作者

## 备注
当前判断基于 README、`package.json`、`index.ts`、`render.ts`、`internal-patch.ts`、`state.ts`。虽然它也注册了命令和快捷键，但仓库最核心的价值是“重新渲染 thinking 的终端显示层”，因此优先归为 UI / Notification 扩展，而不是 Command 或 Event / Hook 扩展。
