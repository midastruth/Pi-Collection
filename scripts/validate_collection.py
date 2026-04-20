#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

CATEGORY_LABELS = {
    "Command": "Command 扩展",
    "Tool": "Tool 扩展",
    "Event-Hook": "Event / Hook 扩展",
    "UI-Notification": "UI / Notification 扩展",
    "Workflow-Automation": "Workflow / Automation 扩展",
    "Integration": "Integration 扩展",
    "Template-Example": "Template / Example 扩展",
    "Utility-Developer-Experience": "Utility / Developer Experience 扩展",
}

REQUIRED_FIELDS = ["GitHub", "主分类", "标签", "一句话总结"]
REQUIRED_SECTIONS = [
    "## 功能说明",
    "## 适用场景",
    "## 核心机制",
    "## 安装与使用",
    "## 值得关注的点",
    "## 限制与注意事项",
    "## 适合谁",
    "## 备注",
]
CORE_MECHANISM_FIELDS = [
    "是否注册 command",
    "是否注册 tool",
    "是否监听 event / hook",
    "是否涉及 UI / notify",
    "是否依赖第三方服务",
]
INSTALL_FIELDS = ["安装方式", "配置要求", "基本使用方式"]
PI_MARKERS = [
    "pi-coding-agent",
    "pi package",
    "pi install",
    "pi 扩展",
    "pi extension",
    "面向 pi",
    "用于 pi",
    "当前 pi",
    "pi 会话",
]


def normalize_text(value: str) -> str:
    value = value.strip()
    if value.startswith("[") and "](http" in value:
        match = re.search(r"\((https?://[^)]+)\)", value)
        if match:
            return match.group(1)
    return value.strip("` ")


def extract_field(text: str, field: str) -> str | None:
    pattern = rf"^- \*\*{re.escape(field)}\*\*:\s*(.+)$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return normalize_text(match.group(1)) if match else None


def parse_labels(raw: str | None) -> set[str]:
    if not raw:
        return set()
    cleaned = raw.replace("，", ",")
    parts = [part.strip().strip("`") for part in cleaned.split(",")]
    return {part for part in parts if part}


def is_repo_dir(path: Path) -> bool:
    return path.is_dir() and path.name != ".git" and not path.name.startswith(".")


def find_repo_dirs(root: Path) -> list[tuple[str, Path]]:
    repos: list[tuple[str, Path]] = []
    for category in CATEGORY_LABELS:
        category_dir = root / category
        if not category_dir.exists():
            continue
        for child in sorted(category_dir.iterdir()):
            if child.name == "README.md" or not is_repo_dir(child):
                continue
            repos.append((category, child))
    return repos


def validate_repo_readme(category: str, repo_dir: Path, root_readme: str, category_readme: str, strict_suspicious: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    readme_path = repo_dir / "README.md"
    repo_name = repo_dir.name

    if not readme_path.exists():
        return ([f"{readme_path}: 缺少 README.md"], warnings)

    text = readme_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = next((line for line in lines if line.strip()), "")
    if title != f"# {repo_name}":
        warnings.append(f"{readme_path}: 标题建议与目录名一致，当前应为 '# {repo_name}'")

    for field in REQUIRED_FIELDS:
        value = extract_field(text, field)
        if not value:
            errors.append(f"{readme_path}: 缺少字段 “{field}”")
            continue
        if field == "GitHub" and "github.com/" not in value:
            errors.append(f"{readme_path}: GitHub 字段需要包含有效的 github.com 链接")
        if field == "主分类" and CATEGORY_LABELS[category] not in value:
            errors.append(
                f"{readme_path}: 主分类应包含 “{CATEGORY_LABELS[category]}”，当前为 “{value}”"
            )

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{readme_path}: 缺少章节 “{section}”")

    for field in CORE_MECHANISM_FIELDS:
        if not re.search(rf"^- \*\*{re.escape(field)}\*\*:\s*.+$", text, flags=re.MULTILINE):
            errors.append(f"{readme_path}: “核心机制”中缺少 “{field}”")

    for field in INSTALL_FIELDS:
        if not re.search(rf"^- \*\*{re.escape(field)}\*\*:\s*.+$", text, flags=re.MULTILINE):
            errors.append(f"{readme_path}: “安装与使用”中缺少 “{field}”")

    root_link = f"[{repo_name}](./{category}/{repo_name}/)"
    if root_link not in root_readme:
        errors.append(f"README.md: 缺少 {repo_name} 的导航链接 {root_link}")

    category_link = f"[{repo_name}](./{repo_name}/)"
    if category_link not in category_readme:
        errors.append(f"{category}/README.md: 缺少 {repo_name} 的导航链接 {category_link}")

    labels = parse_labels(extract_field(text, "标签"))
    lowered = text.lower()
    pi_related = any(marker in lowered for marker in PI_MARKERS)
    explicit_exception = any(tag in labels for tag in {"non-extension", "skill-collection"})
    if not repo_name.startswith("pi-") and not pi_related and not explicit_exception:
        message = (
            f"{readme_path}: 仓库名不以 pi- 开头，且正文未明显说明其与 Pi 的关系；"
            "如果是相关但非标准 Pi 扩展，请至少补充 Pi 关联描述，或添加 non-extension / skill-collection 标签"
        )
        if strict_suspicious:
            errors.append(message)
        else:
            warnings.append(message)

    return errors, warnings


def get_staged_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return [Path(line.strip()) for line in result.stdout.splitlines() if line.strip()]


def staged_repo_keys(staged_files: list[Path]) -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for path in staged_files:
        parts = path.parts
        if len(parts) < 2:
            continue
        category, repo_name = parts[0], parts[1]
        if category not in CATEGORY_LABELS or repo_name == "README.md":
            continue
        keys.add((category, repo_name))
    return keys


def validate_structure(root: Path, strict_suspicious: bool, staged_only: bool) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    root_readme_path = root / "README.md"
    if not root_readme_path.exists():
        print("ERROR: 根目录缺少 README.md", file=sys.stderr)
        return 1
    root_readme = root_readme_path.read_text(encoding="utf-8")

    repo_dirs = find_repo_dirs(root)
    seen_repo_names: dict[str, str] = {}
    staged_files: list[Path] = []
    selected_repo_keys: set[tuple[str, str]] = set()

    if staged_only:
        staged_files = get_staged_files(root)
        selected_repo_keys = staged_repo_keys(staged_files)

    for category in CATEGORY_LABELS:
        category_readme_path = root / category / "README.md"
        if not category_readme_path.exists():
            errors.append(f"{category_readme_path}: 缺少分类 README.md")

    for category, repo_dir in repo_dirs:
        if repo_dir.name in seen_repo_names:
            errors.append(
                f"仓库目录名重复: {repo_dir.name} 同时存在于 {seen_repo_names[repo_dir.name]} 和 {category}"
            )
        else:
            seen_repo_names[repo_dir.name] = category

    repo_dirs_to_validate = repo_dirs
    if staged_only:
        repo_dirs_to_validate = [
            (category, repo_dir)
            for category, repo_dir in repo_dirs
            if (category, repo_dir.name) in selected_repo_keys
        ]

    for category, repo_dir in repo_dirs_to_validate:
        category_readme_path = root / category / "README.md"
        if not category_readme_path.exists():
            continue
        category_readme = category_readme_path.read_text(encoding="utf-8")

        repo_errors, repo_warnings = validate_repo_readme(
            category=category,
            repo_dir=repo_dir,
            root_readme=root_readme,
            category_readme=category_readme,
            strict_suspicious=strict_suspicious,
        )
        errors.extend(repo_errors)
        warnings.extend(repo_warnings)

    if errors:
        print("❌ Collection 校验失败：")
        for item in errors:
            print(f"- {item}")
        if warnings:
            print("\n⚠️  另外还有这些提醒：")
            for item in warnings:
                print(f"- {item}")
        return 1

    scope_label = "（仅校验 staged 记录）" if staged_only else ""
    print(f"✅ Collection 校验通过{scope_label}")
    if staged_only and not repo_dirs_to_validate:
        if staged_files:
            print("ℹ️ 当前 staged 变更未涉及仓库详情目录，已跳过详细记录校验")
        else:
            print("ℹ️ 当前没有 staged 文件")
    if warnings:
        print("\n⚠️  提醒：")
        for item in warnings:
            print(f"- {item}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 Pi Collection 的目录结构和文档完整性")
    parser.add_argument(
        "--strict-suspicious",
        action="store_true",
        help="将“看起来不像 Pi 相关仓库”的提示升级为错误",
    )
    parser.add_argument(
        "--staged-only",
        action="store_true",
        help="仅校验本次 staged 涉及的仓库记录，同时仍检查全局分类 README 与重名目录",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    return validate_structure(
        root=root,
        strict_suspicious=args.strict_suspicious,
        staged_only=args.staged_only,
    )


if __name__ == "__main__":
    raise SystemExit(main())
