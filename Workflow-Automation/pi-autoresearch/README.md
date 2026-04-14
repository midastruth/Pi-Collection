# pi-autoresearch

- **GitHub**: [https://github.com/davebcn87/pi-autoresearch](https://github.com/davebcn87/pi-autoresearch)
- **主分类**: Workflow / Automation 扩展
- **标签**: `typescript`, `production-oriented`, `local-only`, `requires-config`
- **一句话总结**: 给 pi 增加“自动做实验→跑基准→记录结果→保留收益/回滚退化→继续下一轮”的持续优化循环，并配套 dashboard 与收尾 skill。

## 功能说明
`pi-autoresearch` 的核心不是单个工具，而是一套围绕“自动优化实验”设计的工作流扩展。它给 agent 注册 `init_experiment`、`run_experiment`、`log_experiment` 三个工具，配合 `/autoresearch` 命令、状态 widget、全屏 dashboard、浏览器导出页面，以及 `autoresearch-create` / `autoresearch-finalize` 两个 skill，把“建立基线、连续试错、自动提交、失败回滚、结果沉淀、最终拆分 review 分支”串成完整闭环。源码里还实现了 `autoresearch.jsonl`、`autoresearch.md`、`autoresearch.ideas.md` 等持久化文件机制，用于在 context reset、重启或长时间运行后继续接力。

## 适用场景
- 想让 pi 持续优化某个可量化指标，如测试耗时、构建速度、bundle 体积、训练指标、Lighthouse 分数
- 需要把“试一个思路、跑 benchmark、看收益、保留或撤销”做成可长期运行的自动循环
- 希望把实验过程沉淀为结构化日志，并在最后整理成可审查、可独立合并的分支

## 核心机制
- **是否注册 command**: 是；注册 `/autoresearch`，支持启动、停止、清空状态、导出 dashboard
- **是否注册 tool**: 是；注册 `init_experiment`、`run_experiment`、`log_experiment`
- **是否监听 event / hook**: 是；源码可见 `session_start`、`session_tree`、`session_before_switch`、`session_shutdown`、`agent_start`、`agent_end`、`before_agent_start` 等生命周期处理，用于恢复状态、自动续跑、补充系统提示与清理 UI
- **是否涉及 UI / notify**: 是；包含常驻状态 widget、展开表格、全屏 overlay、浏览器导出 dashboard、提示通知
- **是否依赖第三方服务**: 不强依赖特定业务 API；主要依赖本地 pi、Git、Node.js、Shell 环境，以及你在 pi 中已配置的模型 provider

## 安装与使用
- **安装方式**: `pi install https://github.com/davebcn87/pi-autoresearch`
- **配置要求**: 至少需要可运行 benchmark 的本地项目、Git 仓库、pi 环境；可选创建 `autoresearch.config.json` 配置 `workingDir` 与 `maxIterations`；如需正确性回压检查，可额外编写 `autoresearch.checks.sh`
- **基本使用方式**: 先执行 `/skill:autoresearch-create` 让 agent 生成 `autoresearch.md` 与 `autoresearch.sh` 并建立 baseline，之后扩展会通过工具驱动连续实验；完成后可运行 `/skill:autoresearch-finalize`，把保留下来的实验整理成多个独立 review 分支；平时也可直接用 `/autoresearch <目标描述>` 进入或恢复该模式

## 值得关注的点
- 不是只“跑命令计时”，而是把实验日志、自动提交/回滚、上下文恢复、结果展示、最终分支整理一起打包成完整优化工作流
- `run_experiment` 会解析 `METRIC name=value` 结构化输出，`log_experiment` 会持久化 primary/secondary metrics 与 ASI（结构化诊断信息），适合长期迭代
- 内置噪声感知的 confidence score，用 MAD 估计 benchmark 抖动，帮助判断收益是否可能只是噪声
- `agent_end` 与 `before_agent_start` 逻辑让它具备明显的“长时运行 / 上下文切换后继续”的设计取向，而不只是一次性脚本
- 同时提供 `autoresearch-finalize` skill 和 `finalize.sh`，把 noisy experiment branch 拆成多个可 review、可独立合并的分支，这一点很有工程价值

## 限制与注意事项
- 强依赖本地 Git 工作流与可脚本化 benchmark；如果目标无法被命令行稳定衡量，这套机制价值会明显下降
- 需要用户或 skill 先把指标、方向、benchmark 脚本、scope 定义清楚，否则很容易出现“自动化很强，但优化目标不稳定”的问题
- 自动循环会持续消耗 token；README 明确建议结合 provider 预算和 `maxIterations` 控制成本
- 当前仓库同时包含 extension 与 skills；README 的手动安装示例只复制了 `autoresearch-create`，但仓库中实际上还有 `autoresearch-finalize`，手动安装时需要自行核对是否一并复制

## 适合谁
- 想把 pi 用作“自动性能/指标优化代理”的高级用户
- 需要在本地项目里持续试错、可恢复执行、并保留完整实验轨迹的开发者
- 想研究 Pi 长时工作流、实验日志、dashboard 与自动回滚机制如何组合实现的扩展开发者

## 备注
这个仓库同时具备 Tool、Command、UI、Skill 等特征，但从实际使用方式看，用户真正安装它是为了获得一套 **持续运行的自动实验优化流程**，因此主分类优先归入 Workflow / Automation 扩展。