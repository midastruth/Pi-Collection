# pi-design-deck

- **GitHub**: https://github.com/nicobailon/pi-design-deck
- **主分类**: Tool 扩展
- **标签**: `typescript` `production-oriented` `requires-config` `skill-collection`
- **一句话总结**: 为 agent 提供 `design_deck` 工具，以多幻灯片可视化决策面板呈现多个方案选项，用户选择后将结果返回给 agent 继续执行。

## 功能说明

agent 调用 `design_deck()` 工具，将架构方案、UI 设计、代码对比等以幻灯片形式展示给用户，每张幻灯片对应一个决策点，每个选项包含代码高亮、Mermaid 流程图、原始 HTML 或图片预览。用户在浏览器（或 macOS 原生 WKWebView 窗口）中逐张选择，提交后 agent 收到干净的 `{ slideId: "选项标签" }` 映射，直接进入实现阶段。内置"生成更多选项"循环——用户点击后 agent 通过 SSE 推送新选项，无需刷新页面。

## 适用场景

- agent 需要呈现多个架构方案让用户做决策（如 auth 方案、API 设计、数据库选型）
- 向用户展示 UI 方向对比，以高保真 HTML 预览代替文字描述
- 读取 PRD / 计划文档后，自动识别决策点并生成逐一确认的幻灯片
- 结合 interview 工具：interview 收集需求，design deck 展示结果方案

## 核心机制

- **是否注册 command**: 是，`/deck`（通用）、`/deck-plan <file>`（读 PRD 生成幻灯片）、`/deck-discover`（先访谈再建幻灯片）
- **是否注册 tool**: 是，`design_deck()`，6 种调用模式（新建 / add-options / add-option / replace-options / list / open & export）
- **是否监听 event / hook**: 未明确说明
- **是否涉及 UI / notify**: 是，本地 HTTP 服务器 + SSE 实时推送；macOS 使用 Glimpse（WKWebView 原生窗口），其他平台回退到浏览器标签
- **是否依赖第三方服务**: Mermaid.js 图表从 CDN 加载（首次需联网）；macOS 原生窗口依赖可选扩展 `npm:glimpseui`

## 安装与使用

- **安装方式**:
  ```bash
  pi install npm:pi-design-deck
  # macOS 原生窗口（可选）
  pi install npm:glimpseui
  ```
  安装后重启 pi 以加载扩展和内置 `design-deck` skill。

- **配置要求**: 可选配置，写入 `~/.pi/agent/settings.json` 的 `designDeck` 键下：
  - `port`：固定端口（默认随机）
  - `browser`：指定浏览器（如 `"chrome"`）
  - `snapshotDir`：快照保存目录
  - `autoSaveOnSubmit`：提交后自动保存（默认 true）
  - `generateModel`：生成更多选项时使用的默认模型
  - `theme.mode`：`"dark"` / `"light"` / `"auto"`

- **基本使用方式**:
  - 直接对话："帮我展示后端架构的 3 个方案" → agent 自动调用 `design_deck()`
  - `/deck` — 通用入口，可带话题也可裸运行
  - `/deck-plan docs/plan.md` — 读计划文档，按决策点建幻灯片
  - `/deck-discover` — 先访谈收集需求，再建幻灯片

## 值得关注的点

- **Generate-more 循环**：用户点击"生成更多选项"后，agent 通过 `add-options` 动作将新选项以 SSE 推入已打开的面板，面板保持状态不刷新；推送前显示 shimmer 骨架屏占位
- **服务器跨调用持久化**：HTTP 服务在工具多次调用间保持运行，无需每次重启；generate-more 调用会阻塞直到用户下一次操作
- **60 个 UI 组件参考库 + 词汇查找表**：内置 skill 包含组件库索引（含别名映射：collapse = accordion = disclosure）和设计系统特征描述，减少 agent 在 UI 设计时的歧义
- **快照系统完善**：提交/取消时自动保存快照（含所选选项和摘要备注），支持按 deckId 重新打开，支持导出自包含 HTML
- **模型选择器**：面板内可切换生成新选项时使用的模型，并支持设为默认值

## 限制与注意事项

- 同一时刻只能有一个 deck 处于活跃状态，需完成或取消后才能新建
- 图片预览块只支持磁盘绝对路径，不支持 URL
- 幻灯片 ID `"summary"` 为系统保留，不可用于自定义幻灯片
- Mermaid 图表依赖 CDN，离线环境首次加载会失败
- 主要在 macOS 上测试，Linux / Windows 属于尽力支持
- 需要 pi-agent v0.35.0 或更高版本（扩展 API）

## 适合谁

- 需要在决策节点给用户展示方案对比，而不是用文字描述的 agent 工作流
- 希望在架构设计、UI 方案选型等阶段引入人工确认环节的团队
- 想要记录与保存每次方案决策过程（快照 + 导出）的用户

## 备注

项目活跃（截至 2026-04-17：187 stars，13 forks），更新频繁。捆绑的 `design-deck` skill 通过 `package.json` 的 `pi.skills` 字段自动发现，无需手动复制。
