"""string_utils 的 pytest 测试。"""
import pytest

from string_utils import count_vowels, is_palindrome, reverse_words


# --- reverse_words ---


def test_reverse_words_normal_multiple():
    assert reverse_words("hello world") == "world hello"


def test_reverse_words_boundary_single_word():
    assert reverse_words("hello") == "hello"


def test_reverse_words_boundary_empty():
    assert reverse_words("") == ""


def test_reverse_words_edge_extra_whitespace():
    assert reverse_words("  hello   world  ") == "world hello"


def test_reverse_words_exception_not_string():
    with pytest.raises(TypeError, match="reverse_words"):
        reverse_words(None)  # type: ignore[arg-type]


# --- count_vowels ---


def test_count_vowels_normal_mixed_case():
    assert count_vowels("Hello World") == 3


def test_count_vowels_boundary_empty():
    assert count_vowels("") == 0


def test_count_vowels_edge_no_vowels():
    assert count_vowels("xyz123") == 0


def test_count_vowels_edge_all_vowels():
    assert count_vowels("aeiouAEIOU") == 10


def test_count_vowels_exception_not_string():
    with pytest.raises(TypeError, match="count_vowels"):
        count_vowels(42)  # type: ignore[arg-type]


# --- is_palindrome ---


def test_is_palindrome_normal_simple():
    assert is_palindrome("aba") is True


def test_is_palindrome_boundary_empty():
    assert is_palindrome("") is True


def test_is_palindrome_boundary_single_char():
    assert is_palindrome("x") is True


def test_is_palindrome_edge_ignore_spaces_and_case():
    assert is_palindrome("A man a plan a canal Panama") is True


def test_is_palindrome_edge_not_palindrome():
    assert is_palindrome("hello") is False


def test_is_palindrome_exception_not_string():
    with pytest.raises(TypeError, match="is_palindrome"):
        is_palindrome(["a"])  # type: ignore[arg-type]
