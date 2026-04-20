# 提交前质量校验

这个仓库提供了一个本地 `pre-commit` 质量门，目的是在 `git commit` 前尽量拦住这些问题：

- 新增仓库目录后忘记补 `README.md`
- 详细记录缺少关键字段或章节
- 仓库被放进了错误分类
- 根目录 `README.md` / 分类目录 `README.md` 忘记补导航链接
- 新增仓库名不以 `pi-` 开头，且文档里也没说明它为什么与 Pi 相关

## 启用方式

在仓库根目录执行：

```bash
bash scripts/install-hooks.sh
```

启用后，每次 `git commit` 都会自动运行：

```bash
python3 scripts/validate_collection.py --strict-suspicious --staged-only
```

也就是默认只检查**本次 staged 涉及的仓库记录**，避免每次提交都全量扫描整个资料库。

## 平时也可以手动跑

```bash
python3 scripts/validate_collection.py
```

如果你想把“可疑但不确定”的 Pi 相关性提示也当成阻断错误：

```bash
python3 scripts/validate_collection.py --strict-suspicious
```

如果你想模拟提交前的实际行为：

```bash
python3 scripts/validate_collection.py --strict-suspicious --staged-only
```

## 当前会检查什么

### 1. 目录结构
- 是否位于允许的分类目录下
- 仓库目录下是否有 `README.md`
- 是否出现同名仓库被放入多个分类

### 2. 详细记录完整性
每个仓库 `README.md` 至少要有这些字段：

- `GitHub`
- `主分类`
- `标签`
- `一句话总结`

以及这些章节：

- `功能说明`
- `适用场景`
- `核心机制`
- `安装与使用`
- `值得关注的点`
- `限制与注意事项`
- `适合谁`
- `备注`

并且会检查：

- `主分类` 是否和所在目录一致
- `核心机制` 的 5 个判断项是否都写了
- `安装与使用` 的 3 个字段是否都写了
- GitHub 链接是否看起来有效

### 3. 导航同步
- 根目录 `README.md` 是否有该仓库入口
- 对应分类目录 `README.md` 是否有该仓库入口

### 4. Pi 相关性提示
对于**目录名不以 `pi-` 开头**的仓库，脚本会额外检查：

- 文档里是否明确说明它和 Pi 的关系
- 或者是否显式加了 `non-extension` / `skill-collection` 标签

这样可以减少把“泛 AI 仓库”误放进资料库的情况。

## 如果你就是要收录“非标准 Pi 扩展”怎么办？

可以，不需要强行删掉。建议至少做到下面两点之一：

1. 在正文里明确写清它和 Pi 的关系
2. 在标签里补上 `non-extension` 或 `skill-collection`

这样校验器就不会把它当成“无说明的可疑仓库”。

## staged-only 的行为说明

- 如果本次提交涉及 `分类目录/仓库目录/...`，会校验该仓库的详细记录完整性
- 如果只改了普通文档、脚本或 hook，而没动仓库详情目录，会跳过“逐仓库内容检查”
- 即使是 `staged-only`，也仍会检查：
  - 分类 `README.md` 是否存在
  - 是否出现重名仓库目录
  - 被本次提交涉及的仓库是否已同步到根目录 / 分类目录导航

这能让提交更快，同时保留最关键的防误收录保护。

## 临时跳过

如果你非常确定这次提交要先绕过校验，可以这样执行：

```bash
SKIP_PI_COLLECTION_VALIDATE=1 git commit
```

不建议长期依赖这个方式。
