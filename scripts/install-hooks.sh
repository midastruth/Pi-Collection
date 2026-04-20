#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"

chmod +x .githooks/pre-commit scripts/install-hooks.sh scripts/validate_collection.py

git config core.hooksPath .githooks

echo "已启用 Git hooks: $repo_root/.githooks"
echo "以后 git commit 会自动执行 scripts/validate_collection.py --strict-suspicious --staged-only"
