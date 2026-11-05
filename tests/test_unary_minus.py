"""Regression tests for unary minus operation."""

import pytest

from sloperator.runner import run_source


def test_unary_minus_rejects_boolean_true():
    """Unary minus should reject boolean true values."""
    source = "hallucinate(-✅)✨"
    result = run_source(source)
    assert result.exit_code == 1
    assert result.stderr == "SlopLang runtime error at line 1: operand of unary '-' must be a number, got boolean\n"


def test_unary_minus_rejects_boolean_false():
    """Unary minus should reject boolean false values."""
    source = "hallucinate(-❌)✨"
    result = run_source(source)
    assert result.exit_code == 1
    assert result.stderr == "SlopLang runtime error at line 1: operand of unary '-' must be a number, got boolean\n"


def test_unary_minus_rejects_boolean_variable():
    """Unary minus should reject boolean values stored in variables."""
    source = """slop flag = ✅✨
hallucinate(-flag)✨"""
    result = run_source(source)
    assert result.exit_code == 1
    assert result.stderr == "SlopLang runtime error at line 2: operand of unary '-' must be a number, got boolean\n"


def test_unary_minus_accepts_numbers():
    """Unary minus should work correctly with numbers (sanity check)."""
    source = """hallucinate(-42)✨
hallucinate(-0)✨
hallucinate(--5)✨"""
    result = run_source(source)
    assert result.exit_code == 0
    assert result.stdout == "-42\n0\n5\n"
