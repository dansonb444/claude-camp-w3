#!/usr/bin/env bash
# 使用项目虚拟环境运行分析器（自动创建 venv 并安装依赖）
set -euo pipefail
cd "$(dirname "$0")"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
fi
exec .venv/bin/python csv_student_analyzer.py "$@"
