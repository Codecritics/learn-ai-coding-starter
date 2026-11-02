"""Regression tests for lexical errors that were previously untested."""

import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize


def test_generic_unexpected_character():
    """Test the generic unexpected character fallback error.
    
    This tests the error path at scanner.py line 115 that handles
    arbitrary unsupported characters not explicitly listed in
    UNSUPPORTED_CHARS dictionary.
    """
    with pytest.raises(LexicalError) as exc_info:
        tokenize("@")
    
    assert exc_info.value.line == 1
    assert exc_info.value.message == "unexpected character '@'"


@pytest.mark.parametrize(
    ("source", "expected_char"),
    [
        ("@", "@"),
        ("#", "#"),
        ("$", "$"),
        ("%", "%"),
        ("^", "^"),
        ("`", "`"),
        ("~", "~"),
        ("[", "["),
        ("]", "]"),
        ("\\", "\\"),
    ],
)
def test_various_unexpected_characters(source: str, expected_char: str):
    """Test that various unsupported characters produce appropriate errors."""
    with pytest.raises(LexicalError) as exc_info:
        tokenize(source)
    
    assert exc_info.value.line == 1
    assert exc_info.value.message == f"unexpected character '{expected_char}'"
