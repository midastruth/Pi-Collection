---
name: publish-extension
description: 当用户想把自己的 Pi 扩展、插件、Skill 或增强 Pi 能力的项目发布/提交/收录/投稿到 pi-agora 收藏库时使用。会分析其 GitHub 仓库或本地项目，判断分类，并准备收录记录或 PR 步骤。
---

# 把项目发布 / 收录到 pi-agora

当用户想把自己的 Pi 扩展 / Skill / 能力增强项目收录进 pi-agora 时，按下面流程帮助用户。注意区分：用户是想**收录自己的项目**，而不是安装已有项目。

## 工作流程

1. **确认意图与语言**
   - 用用户当前使用的语言交流；用户切换语言时跟随切换。
   - 确认用户是想把自己的项目收录进 pi-agora。

2. **分析项目**
   - **有 GitHub 链接**：阅读 README、package.json、`src/`、扩展入口、command / tool / event / UI 相关代码、安装与配置说明。
   - **没有 GitHub，但当前工作区就是要发布的项目**：只做只读检查 —— package.json 的 `pi.extensions`、`extensions/`、`skills/`、`SKILL.md`、`src/`、README、安装脚本与配置示例。**不要修改用户项目，除非用户明确要求整理发布材料。**
   - 必要时可调用 `pi_agora_publish_guide` 工具获取结构化的发布流程提示。

3. **判断分类与标签**
   - 判断它是否与 Pi 扩展 / Skills / agent 能力扩展相关。
   - 按功能选择主分类：Command、Tool、Event-Hook、UI-Notification、Workflow-Automation、Integration、Template-Example、Utility-Developer-Experience。
   - 提炼实际价值，不要照抄 README；信息不足写"未明确说明 / 需进一步确认"。

4. **准备发布材料**
   - 整理发布前清单：README、license、package metadata、安装命令、配置项、示例、风险说明、截图/演示。
   - 生成可复制的 pi-agora 收录记录草稿（遵循仓库模板）。
   - 公共收录通常需要一个可访问来源；用户没有 GitHub 时，建议创建仓库、请维护者代提交，或先保留本地 submission draft —— **不要声称已经公开发布**。

5. **写入仓库（仅当当前工作区就是 pi-agora 仓库且用户确认收录时）**
   - 在 `<分类>/<repo-name>/README.md` 创建/更新记录。
   - 更新根 `README.md` 与对应分类 `README.md` 的导航。
   - 运行 `python3 scripts/validate_collection.py` 校验。
   - 只有用户明确要求时才提交 / push / 协助创建 PR。

6. **当前工作区不是 pi-agora 仓库时**
   - 不要默认修改用户项目。
   - 指导用户 fork/clone `https://github.com/midastruth/pi-agora`，或生成可复制到 PR 的结构化收录记录。

## 原则

- 区分"收录用户自己的项目"与"安装已有项目"。
- 只读优先，未经同意不修改用户项目。
- 不编造功能、安装步骤或配置；信息不足时明确说明。
