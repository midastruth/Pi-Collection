# pi-vent

- **GitHub**: [https://github.com/IgorWarzocha/pi-vent](https://github.com/IgorWarzocha/pi-vent)
- **主分类**: Tool 扩展
- **标签**: `typescript`, `local-only`, `minimal`, `beginner-friendly`
- **一句话总结**: 为 pi 注册一个 `vent` 工具，让 agent 在遇到重大摩擦时把反馈追加到当前工作区的 `VENT.md`。

## 功能说明
pi-vent 是一个很小的 Pi tool 扩展，核心作用是让 agent 把“值得记住的问题反馈”写入项目根目录的 `VENT.md`。它不是普通日志工具，而是通过工具说明约束 agent：只在重复工具失败、文档误导、指令混乱、命令不稳定等明显影响任务推进的场景使用。每条记录会带本地时间戳和可选 trigger 标签，便于后续复盘开发环境、文档或扩展本身的问题。

## 适用场景
- 希望收集 agent 在实际使用 pi 时遇到的严重摩擦点
- 想为项目保留一个轻量的 AI 反馈 / 事后复盘日志
- 开发 Pi 扩展或工作流时，需要观察哪些说明、命令或工具调用容易让 agent 卡住

## 核心机制
- **是否注册 command**: 否，暂未发现
- **是否注册 tool**: 是；注册 `vent` 工具，参数为 `thought` 和可选 `trigger`
- **是否监听 event / hook**: 否，暂未发现
- **是否涉及 UI / notify**: 轻度涉及；实现了工具调用与结果的 TUI 渲染，但不属于通知类扩展
- **是否依赖第三方服务**: 否；只写入当前工作区本地文件 `VENT.md`

## 安装与使用
- **安装方式**: 全局安装 `pi install npm:@howaboua/pi-vent`；当前项目安装 `pi install -l npm:@howaboua/pi-vent`；单次运行可用 `pi -e npm:@howaboua/pi-vent`
- **配置要求**: README 未说明额外配置；安装后依赖 pi 扩展机制加载 `extensions/vent.ts`
- **基本使用方式**: agent 在遇到重大问题时调用 `vent({ thought, trigger? })`，扩展会在当前工作区创建或追加 `VENT.md`

## 值得关注的点
- 用非常小的实现解决“agent 遇到问题但反馈不被沉淀”的问题
- 工具 prompt 明确要求只记录重大问题，并建议在回合末尾批量写入，减少噪音
- 使用 `withFileMutationQueue` 包裹文件写入，降低并发写同一文件时的冲突风险
- 返回结构化 details，包含路径、时间戳、trigger 和原始反馈内容，便于 UI 展示或后续处理

## 限制与注意事项
- 记录质量取决于 agent 是否主动、克制且准确地调用该工具
- 它只追加本地 `VENT.md`，不提供搜索、汇总、上传或去重能力
- 如果项目不希望生成额外反馈文件，需要在使用前明确约束或不要安装
- Pi 扩展以本机权限运行，安装第三方 npm 包前仍需确认来源可信

## 适合谁
- 想持续改进 pi 使用说明、开发文档或本地工作流的用户
- 正在开发 Pi 扩展，希望收集 agent 端真实摩擦反馈的作者
- 喜欢轻量、本地优先、低配置工具的团队或个人

## 备注
当前判断基于 README、`package.json` 与 `extensions/vent.ts`。虽然它包含少量 TUI 渲染逻辑，但核心价值是向 agent 提供一个可调用的本地反馈写入工具，因此归为 Tool 扩展。
