#!/usr/bin/env python3
"""CSV 学员数据分析器：统计人数、国家分布、对赌完成率，输出 report.json。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import pandas as pd
except ModuleNotFoundError:
    root = Path(__file__).resolve().parent
    print(
        "未安装 pandas。请在项目目录执行：\n"
        f"  cd {root}\n"
        "  python3 -m venv .venv\n"
        "  .venv/bin/pip install -r requirements.txt\n"
        "  .venv/bin/python csv_student_analyzer.py",
        file=sys.stderr,
    )
    sys.exit(1)

COMPLETED_STATUS = "已达成"
REQUIRED_COLUMNS = ("姓名", "邮箱", "加入日期", "所在国家", "对赌状态")


def analyze(csv_path: Path) -> dict:
    df = pd.read_csv(csv_path, dtype=str)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV 缺少必要列：{', '.join(missing)}")

    total = len(df)
    country_counts = df["所在国家"].value_counts().sort_index().to_dict()
    completed = int((df["对赌状态"] == COMPLETED_STATUS).sum())
    completion_rate = round(completed / total, 4) if total else 0.0

    return {
        "总人数": total,
        "各国家人数": country_counts,
        "对赌完成人数": completed,
        "对赌完成率": completion_rate,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="分析学员 CSV 并生成 report.json")
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path(__file__).resolve().parent / "users_sample.csv",
        help="学员 CSV 路径（默认：同目录 users_sample.csv）",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "report.json",
        help="统计结果输出路径（默认：同目录 report.json）",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"找不到输入文件：{args.input}")

    report = analyze(args.input)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"已分析 {args.input.name}，共 {report['总人数']} 人")
    print(f"对赌完成率：{report['对赌完成率']:.2%}（{report['对赌完成人数']}/{report['总人数']}）")
    print(f"报告已保存：{args.output}")


if __name__ == "__main__":
    main()
