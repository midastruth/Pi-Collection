# pi-rollback

- **GitHub**: [https://github.com/uriafranko/pi-rollback](https://github.com/uriafranko/pi-rollback)
- **主分类**: Command 扩展
- **标签**: `typescript`, `local-only`, `production-oriented`
- **一句话总结**: 为 pi 会话提供分支感知的检查点与回滚能力，走错路时可退回到更早的节点，同时保留被放弃分支的摘要。

## 功能说明
pi-rollback 解决的问题是：当 agent 探索了一条无效路径后，上下文被无用历史占满，继续对话代价高、质量差。该扩展通过 `/checkpoint` 在任意节点打标签，在需要时用 `/rollback` 回到更早的历史分支，同时自动生成一段"摘要"来保留被放弃分支的有效信息，避免完全遗忘。原始分支在 pi 的会话树中仍然保留，回滚本身是可逆的。

## 适用场景
- agent 走错方向、需要从某个决策点重来
- 长对话中上下文积累了大量无关历史，想"清场"但保留关键信息
- 想在多个探索路径之间做对比，利用 pi 会话树管理实验状态

## 核心机制
- **是否注册 command**: 是；注册了 `/checkpoint [label]` 和 `/rollback`
- **是否注册 tool**: 是；注册了 `rollback` 工具，允许 agent 自主触发回滚
- **是否监听 event / hook**: 未明确说明
- **是否涉及 UI / notify**: 是；回滚失败时会返回用户友好的通知
- **是否依赖第三方服务**: 否；纯本地，依赖 pi 自身的会话树与标签机制

## 安装与使用
- **安装方式**: `pi install npm:pi-rollback`
- **配置要求**: 无需额外配置
- **基本使用方式**:
  1. 在重要节点执行 `/checkpoint` 或 `/checkpoint my-label` 打标签
  2. 走错路后执行 `/rollback` 选择目标节点返回
  3. agent 也可以通过 `rollback` 工具自主触发回滚（指定 `dropMessages`、`targetEntryId` 或 `targetLabel`）

## 值得关注的点
- 利用 pi 原生分支模型：回滚不是删历史，而是移动当前分支指针，被放弃的路径仍可访问
- 回滚前会自动生成摘要（`buildSummaryInstructions`），将废弃分支的有价值发现注入下一段上下文
- 支持三种定位方式：按消息数回退（`dropMessages`）、按条目 ID（`targetEntryId`）、按标签名（`targetLabel`），灵活性高
- `rollback` 工具对 agent 开放，意味着 agent 可以自主决定"这条路走不通，我要回滚"，实现更自主的自我纠错
- 支持回滚后自动附带一段 continuation prompt，避免回到检查点后还要手动重新指令

## 限制与注意事项
- 依赖 pi 会话树机制（`pi.setLabel`、分支导航），不适用于不支持此能力的 pi 版本
- 当前版本（0.1.0）仍处于早期阶段，API 和行为可能随版本更新变化
- 对话历史中缺少足够的 checkpoint 时，`dropMessages` 计数回退可能报错（无足够历史可回溯）

## 适合谁
- 在 pi 会话中做长流程探索、需要管理多个实验路径的开发者
- 希望让 agent 具备自我纠错与路径管理能力的用户
- 想减少无效上下文积累、降低 token 浪费的用户

## 备注
核心逻辑集中在单文件 `extensions/pi-rollback/index.ts`。同时注册了 command 与 tool，但以 `/checkpoint` + `/rollback` 用户命令为主要交互入口，`rollback` tool 为 agent 侧附加能力，因此主分类归为 Command 扩展。
