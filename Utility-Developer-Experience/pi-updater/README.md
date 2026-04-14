# pi-updater

- **GitHub**: [https://github.com/tonze/pi-updater](https://github.com/tonze/pi-updater)
- **主分类**: Utility / Developer Experience 扩展
- **标签**: `typescript`, `production-oriented`, `requires-config`, `third-party-api`
- **一句话总结**: 为 pi 提供类似 Codex 的自动更新体验，在启动时检查新版本、弹出更新提示，并在成功安装后尝试无缝重启当前会话。

## 功能说明
`pi-updater` 不是给 agent 增加业务能力的工具，而是给 **pi 本体** 增加更新检查与安装体验的辅助扩展。它会在 `session_start` / `session_switch` 时做缓存优先的版本检查：先读取本地缓存，必要时再后台访问 npm registry；如果发现新版本，就在 UI 中提供“立即更新 / 本次跳过 / 跳过此版本”的选择。用户也可以通过 `/update` 手动检查更新，扩展会调用 npm 安装新版 `@mariozechner/pi-coding-agent`，成功后再尝试用当前 session 自动重启 pi。

## 适用场景
- 希望在使用 pi 时及时知道官方新版本，而不是手动去 npm 或 GitHub 检查
- 想给本地安装的 pi 增加更顺手的升级流程，包括更新提示、忽略特定版本、升级后重启
- 需要一个轻量、尽量不拖慢启动速度的更新检查方案

## 核心机制
- **是否注册 command**: 是；注册 `/update`，支持手动检查更新，另外还提供 `/update --test` 用于测试整套交互流程
- **是否注册 tool**: 否；当前未见面向 agent 的 tool 注册
- **是否监听 event / hook**: 是；监听 `session_start` 与 `session_switch`，用于触发自动版本检查
- **是否涉及 UI / notify**: 是；依赖选择框、确认框、loader、通知提示来承载更新流程
- **是否依赖第三方服务**: 是；依赖 npm registry 获取最新版本信息，并通过 `npm install -g` 安装新版 pi

## 安装与使用
- **安装方式**: `pi install npm:pi-updater`，或 `pi install git:github.com/tonze/pi-updater`
- **配置要求**: 当前自动安装仅明确支持 **npm 安装的 pi**；需要本地具备 npm 全局安装权限与联网能力；可通过环境变量 `PI_SKIP_VERSION_CHECK=1` 或 `PI_OFFLINE=1` 禁用自动检查
- **基本使用方式**: 安装后正常启动 pi 即可在发现新版本时收到提示；也可以在会话中手动执行 `/update` 强制检查，若升级成功，扩展会询问是否立即重启当前会话

## 值得关注的点
- 启动检查采用“本地缓存优先 + 本次运行只做一次后台 live check”的策略，尽量减少对启动速度的影响
- 支持“Skip this version”，会把被忽略版本写入 `~/.pi/agent/update-cache.json`，避免同一版本反复打扰
- 更新成功后会尝试重新拉起 `pi` 并复用当前 session 文件，整体体验明显比纯命令行升级更顺滑
- 代码体量很小，结构清晰，适合作为研究 Pi UI 交互、session restart 与轻量系统辅助扩展的参考样例

## 限制与注意事项
- 自动安装路径目前只覆盖 npm 安装形态；如果用户的 pi 不是通过 npm 安装，实际升级流程可能不适用
- 强依赖 npm registry 和本机 npm 全局安装能力；离线环境下只会提示无法检查，且 `PI_OFFLINE` 会直接禁用自动检查
- 它更新的是 `@mariozechner/pi-coding-agent` 包，本质上更接近“pi 本体升级助手”，而不是项目级业务扩展
- 版本号比较逻辑较简单，当前主要基于标准三段式 semver 字符串；更复杂的 prerelease/build metadata 处理在源码中未见展开

## 适合谁
- 常用 pi、希望获得更顺手升级体验的终端用户
- 想给本地 agent 工具链加入轻量自更新能力的扩展开发者
- 想研究 Pi 扩展如何接入 UI、会话切换事件和本地命令执行的开发者

## 备注
虽然它也访问第三方 npm registry，但仓库的核心价值并不是“集成外部业务服务”，而是提升 **pi 本身的维护与使用体验**，因此更适合归入 Utility / Developer Experience 扩展。