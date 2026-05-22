#!/usr/bin/env python3
"""JSON 配置文件读写器：读取/修改用户偏好并写回 config.json。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

CONFIG_KEYS = ("主题", "语言", "字体大小")

DEFAULT_CONFIG: dict[str, Any] = {
    "主题": "light",
    "语言": "zh-CN",
    "字体大小": 14,
}

THEMES = frozenset({"light", "dark", "auto"})
LANGUAGES = frozenset({"zh-CN", "zh-TW", "en-US", "ja-JP", "ko-KR"})
FONT_MIN, FONT_MAX = 8, 32


def _validate_theme(value: str) -> str:
    v = value.strip().lower()
    if v not in THEMES:
        raise ValueError(f"主题必须是以下之一：{', '.join(sorted(THEMES))}")
    return v


def _validate_language(value: str) -> str:
    v = value.strip()
    if v not in LANGUAGES:
        raise ValueError(f"语言必须是以下之一：{', '.join(sorted(LANGUAGES))}")
    return v


def _validate_font_size(value: str) -> int:
    try:
        n = int(value.strip())
    except ValueError as e:
        raise ValueError(f"字体大小必须是 {FONT_MIN}～{FONT_MAX} 之间的整数。") from e
    if not FONT_MIN <= n <= FONT_MAX:
        raise ValueError(f"字体大小必须在 {FONT_MIN}～{FONT_MAX} 之间，当前为 {n}。")
    return n


VALIDATORS: dict[str, Callable[[str], Any]] = {
    "主题": _validate_theme,
    "语言": _validate_language,
    "字体大小": _validate_font_size,
}


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        save_config(path, dict(DEFAULT_CONFIG))
        print(f"已创建默认配置文件：{path}")
        return dict(DEFAULT_CONFIG)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"配置文件 JSON 格式无效：{e}") from e
    if not isinstance(data, dict):
        raise ValueError("配置文件根节点必须是 JSON 对象。")
    return data


def save_config(path: Path, config: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def validate_config(config: dict[str, Any]) -> dict[str, Any]:
    """校验完整配置；缺失键用默认值补全。"""
    out: dict[str, Any] = {}
    for key in CONFIG_KEYS:
        raw = config.get(key, DEFAULT_CONFIG[key])
        if key == "字体大小":
            if isinstance(raw, bool) or not isinstance(raw, int):
                raise ValueError("字体大小必须是整数。")
            out[key] = _validate_font_size(str(raw))
        else:
            if not isinstance(raw, str):
                raise ValueError(f"「{key}」必须是字符串。")
            out[key] = VALIDATORS[key](raw)
    return out


def show_config(config: dict[str, Any]) -> None:
    print("当前用户偏好：")
    for key in CONFIG_KEYS:
        print(f"  {key}：{config[key]}")


def edit_setting(config: dict[str, Any], path: Path) -> None:
    print()
    print("可修改的设置：")
    for i, key in enumerate(CONFIG_KEYS, 1):
        hint = ""
        if key == "主题":
            hint = f"（可选：{', '.join(sorted(THEMES))}）"
        elif key == "语言":
            hint = f"（可选：{', '.join(sorted(LANGUAGES))}）"
        elif key == "字体大小":
            hint = f"（整数 {FONT_MIN}～{FONT_MAX}）"
        print(f"  {i} — {key}{hint}  当前：{config[key]}")
    choice = input("请输入要修改的编号（直接回车取消）：").strip()
    if not choice:
        print("已取消修改。")
        return
    try:
        idx = int(choice)
        if not 1 <= idx <= len(CONFIG_KEYS):
            raise ValueError
    except ValueError:
        print("提示：请输入有效的选项编号。")
        return
    key = CONFIG_KEYS[idx - 1]
    new_raw = input(f"请输入新的「{key}」：").strip()
    if not new_raw:
        print("提示：新值不能为空。")
        return
    try:
        config[key] = VALIDATORS[key](new_raw)
    except ValueError as e:
        print(f"提示：{e}")
        return
    save_config(path, config)
    print(f"已更新「{key}」并保存到 {path.name}。")
    show_config(config)


def main() -> None:
    parser = argparse.ArgumentParser(description="JSON 用户偏好配置读写器")
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=Path(__file__).resolve().parent / "config.json",
        help="配置文件路径（默认：同目录 config.json）",
    )
    args = parser.parse_args()
    path = args.config.resolve()

    try:
        raw = load_config(path)
        config = validate_config(raw)
        if raw != config:
            save_config(path, config)
    except ValueError as e:
        print(f"提示：{e}")
        sys.exit(1)

    print("JSON 配置文件读写器")
    while True:
        print()
        print("请选择操作：")
        print("  1 — 查看当前配置")
        print("  2 — 修改某项设置")
        print("  0 — 退出")
        choice = input("请输入选项编号：").strip()
        try:
            if choice == "0":
                print("再见。")
                sys.exit(0)
            if choice == "1":
                show_config(config)
            elif choice == "2":
                edit_setting(config, path)
            else:
                print("提示：请输入 0～2 之间的数字。")
        except (EOFError, KeyboardInterrupt):
            print("\n已中断，退出程序。")
            sys.exit(0)
        except Exception as e:
            print(f"发生意外错误：{e}")
            print("请重试；程序将继续运行。")


if __name__ == "__main__":
    main()
