# pi-codex-search

- **GitHub**: https://github.com/Leechael/pi-codex-search
- **npm**: `pi-codex-search`
- **主分类**: Tool 扩展
- **标签**: `typescript`、`third-party-api`、`web-search`、`production-oriented`、`requires-config`
- **一句话总结**: 注册一个 `codex_search` 工具，复用 Pi 已有的 `openai-codex`（ChatGPT Plus/Pro Codex 订阅）登录凭证为模型提供带引用来源的联网搜索，无需单独 token 或 API key。

## 功能说明
这是一个以工具能力为核心的 Pi 扩展。它不给模型 provider 本身加浏览能力，而是注册一个 `codex_search` 工具，由模型按需调用。核心卖点是**直接复用 Pi 已知的 `openai-codex` OAuth 凭证**：只要 Pi 能用你的 Codex 订阅，这个扩展就能用同一套鉴权走 ChatGPT 后端的搜索路径，无需 `ACCESS_TOKEN` 环境变量或单独登录流程。

工具支持单次调用 1–5 个查询并行执行、按 query 分组返回结果，可选 `live`/`cached` 新鲜度与 `low`/`medium`/`high` 搜索上下文规模；返回文本在有引用时附带 `Sources:` 段落，并提供包含 model、citations、search calls、response id、usage、逐 query 失败信息的结构化 `details`。TUI 中支持流式进度、折叠预览与展开查看全文与来源。

## 适用场景
- 已有 ChatGPT Plus/Pro（Codex 订阅）并在 Pi 中用 `openai-codex` 登录，想顺带获得联网搜索而不想再配额外的搜索 API。
- 需要查询训练截止后的最新文档 / release notes，并希望结果带来源引用。
- 需要一次性发起多个相关查询做对比（最多 5 个并行）。
- 希望按项目控制搜索工具的开关、命名与默认参数。

## 核心机制
- **是否注册 command**: 是，注册 `/codex-search-settings`（含 `status`、`reset` 子命令及交互式设置对话框，用于改名、禁用、固定模型、调默认值）。
- **是否注册 tool**: 是，注册 `codex_search` 工具（工具名可配置，须匹配 `[a-zA-Z_][a-zA-Z0-9_]{0,63}`）。
- **是否监听 event / hook**: 是，监听 `session_start`，按配置加载并在 `enabled` 时注册工具。
- **是否涉及 UI / notify**: 是，流式搜索进度、折叠预览、展开全文与来源、失败分类提示。
- **是否依赖第三方服务**: 是，依赖 ChatGPT/Codex 后端（`chatgpt.com/backend-api`）及用户的 Codex 订阅鉴权。

## 安装与使用
- **安装方式**:
  - npm：`pi install npm:pi-codex-search`
  - 本地试用：`pi -e /path/to/pi-codex-search`
  - GitHub Release tarball：下载 `pi-codex-search.tar.gz` 解压后 `pi install /tmp/pi-codex-search`
- **配置要求**: 必须先在 Pi 内 `/login openai-codex` 并选择 `ChatGPT Plus/Pro (Codex Subscription)`；无 token 或取不到 ChatGPT account id 时首次调用报 `auth` 错误。配置按「环境变量 > 项目 `<cwd>/.pi/pi-codex-search.json` > 家目录 `~/.pi/pi-codex-search.json`」三层合并，支持 `enabled`、`toolName`、`model`、`baseUrl`、`searchContextSize`、`freshness` 等字段及对应 `PI_CODEX_WEB_SEARCH_*` 环境变量。
- **基本使用方式**: 安装后工具默认注册，模型自行决定何时调用 `codex_search`；用户也可用 `/codex-search-settings` 调整。

## 值得关注的点
- 用「复用 Codex 订阅鉴权」解决联网搜索，省去单独申请/粘贴搜索 API key，对已经用 Codex 订阅的人接入成本极低。
- 搜索模型按「config > 当前 Codex 模型 > `/codex/models` 默认」顺序自动选择，多数用户无需手动设置。
- 错误分类细致（`auth` / `rate_limit` / `transport` / `timeout` / `schema` / `unknown`），并提供清晰的故障排查指引。
- 配置三层合并 + 非法值 fail-fast，避免静默以错误设置运行；改名/禁用可避免与其他搜索扩展工具名冲突。

## 限制与注意事项
- 强依赖有效的 Codex 订阅与 `openai-codex` OAuth 凭证；凭证过期或取不到 account id 时需重新 `/login openai-codex`。
- 走的是 ChatGPT 后端非公开接口（`backend-api`），稳定性与可用性受其策略影响。
- 受订阅本身的速率/额度限制，多查询并行会放大消耗。
- 当前版本 0.1.x；判断基于 README、`package.json`、`index.ts`，底层请求细节需进一步阅读 `src/codex.ts`、`src/config.ts` 确认。

## 适合谁
- 已用 ChatGPT Plus/Pro Codex 订阅、希望零额外配置就给 Pi 加联网搜索的用户。
- 需要带来源引用、可批量并行查询的检索能力的 coding agent 用户。
- 想研究如何在 Pi 扩展中复用 provider OAuth 凭证、调用 Codex 后端的开发者。

## 备注
- 与本仓库已收录的 [pi-web-search](./../pi-web-search/) 对比：pi-web-search 底层走 Gemini/Google provider 的搜索与 URL grounding，并额外提供 `url_context`；pi-codex-search 则专注复用 ChatGPT/Codex 订阅鉴权做 `codex_search`，定位更适合已有 Codex 订阅的用户。
- 仓库提到 release 流程与 `pi-provider-kimi-code` 同构，作者为 Leechael。
