"""字符串工具：反转单词顺序、统计元音、判断回文。"""
from __future__ import annotations

VOWELS = frozenset("aeiouAEIOU")


def _require_str(s: object, func_name: str) -> str:
    if not isinstance(s, str):
        raise TypeError(f"{func_name} 的参数必须是 str，收到 {type(s).__name__}")
    return s


def reverse_words(s: str) -> str:
    """按空白分词后反转顺序，再用单个空格连接。"""
    s = _require_str(s, "reverse_words")
    parts = s.split()
    return " ".join(reversed(parts))


def count_vowels(s: str) -> int:
    """统计英文字母元音 a/e/i/o/u（大小写均计）。"""
    s = _require_str(s, "count_vowels")
    return sum(1 for ch in s if ch in VOWELS)


def is_palindrome(s: str) -> bool:
    """忽略非字母数字字符与大小写后，判断是否回文。"""
    s = _require_str(s, "is_palindrome")
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]
