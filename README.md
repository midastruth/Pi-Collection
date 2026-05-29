# pi-agora

这是一个按分类整理的 Pi 扩展 / Skills 资料库，也是一个名为 `pi-agora` 的 Pi package。

- 根目录 `README.md` 只用作导航目录
- **详细记录放在各分类文件夹中**
- 每个仓库使用单独文件夹保存，便于后续继续补充截图、源码笔记、安装说明等内容

## 作为 Pi 扩展安装
本仓库可以作为 Pi package 使用，扩展名为 `pi-agora`。它采用 **Skill 驱动** 的方式工作：

- 随包提供两个 Pi Skill（`SKILL.md`），通过 `package.json` 的 `pi.skills` 注册，也在运行时通过 `resources_discover` 事件暴露 `skills/` 目录：
  - `recommend-tools`：根据需求在本地收藏库检索并推荐合适的 Pi 扩展，确认后协助安装
  - `publish-extension`：帮助用户把自己的 Pi 扩展 / Skill / 能力增强项目收录到 pi-agora
- 提供底层工具供 Skill 调用：`pi_agora_search`（检索）、`pi_agora_install`（安装）、`pi_agora_publish_guide`（发布流程提示）
- 提供命令作为 Skill 的快捷入口：`/pi-agora`、`/pi-agora-publish`、`/pi-publish`

这两个 Skill 是 model-invocable 的：用户描述需求时模型会自动触发，也可以用 `/skill:recommend-tools`、`/skill:publish-extension` 显式调用，或用 `/pi-agora <需求>` 启动。首次加载会提示已加载的 Skill；如需关闭首次提示，可设置 `PI_AGORA_AUTO_ONBOARD=0`。

```bash
pi install https://github.com/midastruth/pi-agora
# 或临时安装
pi -e https://github.com/midastruth/pi-agora
# 或本地测试
pi -e /path/to/pi-agora
```

安装后可输入：

```text
/pi-agora 我想给 pi 增加联网搜索能力      # 触发 recommend-tools Skill
/skill:recommend-tools                   # 显式调用推荐 Skill
/pi-agora-publish https://github.com/you/your-pi-extension
/skill:publish-extension                 # 显式调用发布 Skill
/pi-publish  # 没有 GitHub 时，为当前本地 Pi 扩展 / Skill 项目准备发布材料
```

> 也可以直接用自然语言描述需求（例如“我想要个代码审查工具”），pi-agora 的 Skill 会被模型自动触发。

## 分类目录
- [Command 扩展](./Command/)
- [Tool 扩展](./Tool/)
- [Event / Hook 扩展](./Event-Hook/)
- [UI / Notification 扩展](./UI-Notification/)
- [Workflow / Automation 扩展](./Workflow-Automation/)
- [Integration 扩展](./Integration/)
- [Template / Example 扩展](./Template-Example/)
- [Utility / Developer Experience 扩展](./Utility-Developer-Experience/)

## 当前已收录
- [pi-skills](./Utility-Developer-Experience/pi-skills/) - 跨多种 agent 生态的 skills 集合仓库，包含搜索、浏览器自动化、转录、VS Code diff、Google CLI 等能力
- [pi-telegram](./Integration/pi-telegram/) - Telegram 私聊桥接扩展，可把当前 pi 会话接到 Telegram Bot 上
- [pi-intercom](./Integration/pi-intercom/) - 本地会话间 1:1 通信扩展，支持定向发消息、等待回复与 overlay UI
- [pi-brain](./Integration/pi-brain/) - 多来源 AI coding 会话导出与脱敏扩展，支持 Pi 内命令、CLI、Hugging Face 上传与多种训练格式
- [pi-diff-review](./Command/pi-diff-review/) - 原生 diff 审查窗口扩展，通过 `/diff-review` 收集评审意见并插回 pi 编辑器
- [pi-review](./Command/pi-review/) - 命令式代码审查扩展，支持 review uncommitted changes、branch、commit、PR 与 folder，并可用 `/end-review` 返回总结
- [pi-model-switch](./Tool/pi-model-switch/) - 为 agent 提供 `switch_model` 工具，可列出、搜索并切换当前会话模型
- [pi-web-search](./Tool/pi-web-search/) - 提供 `web_search` 与 `url_context` 工具，支持联网搜索与 URL 内容分析
- [pi-interactive-subagents](./Workflow-Automation/pi-interactive-subagents/) - 异步子代理编排扩展，支持多窗格并行执行与结果异步回灌
- [pi-subagents](./Workflow-Automation/pi-subagents/) - 通用子代理编排扩展，支持 `/run`、`/chain`、`/parallel`、Agents Manager、async 状态追踪与 worktree 隔离并行
- [taskplane](./Workflow-Automation/taskplane/) - 面向 pi 的多代理任务编排系统，支持分波执行、review、merge 与本地 dashboard
- [pi-autoresearch](./Workflow-Automation/pi-autoresearch/) - 自动实验优化循环扩展，支持 benchmark 执行、结果保留/回滚、dashboard 与 finalize skill
- [pi-dynamic-workflows](./Workflow-Automation/pi-dynamic-workflows/) - 注册 `workflow` 工具，让模型写确定性 JS 脚本，用 `agent`/`parallel`/`pipeline` 把任务 fan-out 到多个隔离子代理并汇总，对标 Claude Code dynamic workflows
- [pi-updater](./Utility-Developer-Experience/pi-updater/) - pi 本体自动更新扩展，支持启动检查、npm 安装升级与会话重启
- [pi-rollback](./Command/pi-rollback/) - 分支感知的检查点与回滚扩展，支持 `/checkpoint` 打标、`/rollback` 退回更早节点，并自动保留被放弃分支的摘要
- [pi-smart-btw](./Command/pi-smart-btw/) - `/btw <question>` 拉起无会话子 Pi 异步回答离题问题，默认仅显示于 transcript，需要时手动注入主会话
- [pi-design-deck](./Tool/pi-design-deck/) - 为 agent 提供 `design_deck` 工具，以多幻灯片可视化决策面板呈现多方案对比，用户选择后结果直接返回 agent
- [pi-vent](./Tool/pi-vent/) - 注册 `vent` 工具，把 agent 遇到的重大摩擦与复盘反馈追加到本地 `VENT.md`
- [pi-live-terminal](./Tool/pi-live-terminal/) - 提供 `live_terminal_run` / `live_terminal_close` 工具，把长任务或交互式命令放进 tmux 并在 Pi 中实时显示
- [pi-codex-conversion](./Tool/pi-codex-conversion/) - Codex-oriented 工具与 provider adapter，把 Codex-like 模型的工具面切换为 `exec_command` / `write_stdin` / `apply_patch` 等 Codex 风格工具
- [pi-codex-search](./Tool/pi-codex-search/) - 注册 `codex_search` 工具，复用 `openai-codex`（ChatGPT Codex 订阅）鉴权提供带引用来源的联网搜索，支持 1–5 查询并行与 `/codex-search-settings` 配置
- [pi-caveman](./Event-Hook/pi-caveman/) - 通过 `before_agent_start` 注入压缩型回答规则，并配合 `/caveman` 命令、状态恢复与底部状态栏降低输出冗长度
- [pi-jarvis](./UI-Notification/pi-jarvis/) - `/jarvis` 侧边对话 overlay，为主会话提供独立辅助线程、权限开关与 note/redirect 回传能力
- [pi-thinking-steps](./UI-Notification/pi-thinking-steps/) - thinking 显示增强扩展，提供 collapsed / summary / expanded 三种终端推理视图
- [pi-draw](./UI-Notification/pi-draw/) - 通过 `/draw` 或快捷键打开 tldraw 画布，将绘图导出为 PNG 并附加到当前 prompt
- [howaboua-pi-stuff](./Utility-Developer-Experience/howaboua-pi-stuff/) - 作者 IgorWarzocha 的 Pi 工具箱 monorepo，聚合 ~11 扩展 + 6 skills，提供 pi-stuff/pi-extensions/pi-skills 三个一键安装 bundle（pi-vent/pi-smart-btw/pi-codex-conversion 的发布源）
## 说明
如果后续新增仓库：
1. 先判断主分类
2. 在对应分类目录下创建仓库文件夹
3. 将详细分析写入该仓库文件夹下的 `README.md`
4. 再回到根目录 `README.md` 补充导航链接

## 提交前校验
- 手动执行：`python3 scripts/validate_collection.py`
- 模拟提交前范围：`python3 scripts/validate_collection.py --strict-suspicious --staged-only`
- 安装 Git Hook：`bash scripts/install-hooks.sh`
- 说明文档：[`docs/commit-quality-gate.md`](./docs/commit-quality-gate.md)
