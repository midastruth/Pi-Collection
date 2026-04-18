# pi-caveman

- **GitHub**: https://github.com/jonjonrankin/pi-caveman
- **主分类**: Event / Hook 扩展
- **标签**: typescript, local-only
- **一句话总结**: 通过 `before_agent_start` 注入“caveman mode”提示词，并配合 `/caveman` 命令、会话状态恢复与底部状态栏，让 pi 用更短的话输出同样的技术内容。

## 功能说明
这个扩展的核心目标是压缩 agent 的自然语言输出，尽量减少废话和说明性填充词，从而节省 token。它提供 `lite`、`full`、`ultra`、`wenyan` 系列和 `micro` 等多种压缩级别，既可以临时切换，也可以设为新会话默认模式。除了提示词注入，它还会保存会话级别状态、恢复历史会话设置，并在底部状态栏显示当前模式。

## 适用场景
- 希望长期降低回答冗长度和 token 消耗
- 更喜欢直接、压缩、偏命令式的技术说明风格
- 需要在不同会话间保留默认输出风格

## 核心机制
- **是否注册 command**: 是，注册 `/caveman` 命令，可切换模式、关闭模式、打开配置界面
- **是否注册 tool**: 否，未发现注册给 AI 调用的工具
- **是否监听 event / hook**: 是，监听 `session_start`、`agent_start`、`agent_end`、`session_shutdown`，并在 `before_agent_start` 中追加系统提示词
- **是否涉及 UI / notify**: 是，提供设置面板、通知提示和底部动态状态栏
- **是否依赖第三方服务**: 否，主要依赖本地 pi 扩展 API 与本地配置文件

## 安装与使用
- **安装方式**: `pi install git:github.com/jonjonrankin/pi-caveman`
- **配置要求**: 可选配置保存在 `~/.pi/agent/caveman.json`，支持设置默认级别与是否显示状态栏
- **基本使用方式**: 使用 `/caveman` 开关模式，或 `/caveman lite|full|ultra|wenyan-lite|wenyan|wenyan-ultra|micro|off` 指定级别；`/caveman config` 打开设置界面

## 值得关注的点
- 不是简单注册命令，而是通过 `before_agent_start` 在模型启动前修改系统提示词，真正影响后续回答风格
- 对会话恢复做了处理：当前模式会写入 session custom entry，恢复会话时可延续原来的压缩级别
- 对危险提示、不可逆操作确认等情况预留“自动恢复正常表达”的 safety 规则，避免一味压缩导致误解

## 限制与注意事项
- 它改变的是回答风格，不会减少代码块本身的长度，也不会替代模型能力优化
- `micro` 模式在 README 中明确标为 experimental，实际效果可能随模型不同而波动
- 主要价值是“更省字”和“更直接”，如果用户偏好完整解释或教学式表达，体验可能不如默认模式

## 适合谁
- 想降低日常交互 token 消耗的 pi 用户
- 偏好简短、直接技术回答的开发者
- 想研究 pi 生命周期 hook、状态持久化和 TUI 设置面板写法的扩展开发者

## 备注
当前判断主要基于 README、`package.json` 与 `extensions/caveman.ts`。该仓库同时具备 command、UI 和 event 特征，但其核心能力是通过生命周期 hook 注入提示词并维持状态，因此归入 **Event / Hook 扩展**。
