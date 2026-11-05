"""Tests for nested function calls."""

import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    """Run source and return stdout, asserting no errors."""
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def test_call_result_as_argument():
    """A call's result can be used directly as an argument to another call."""
    source = """clanker double(x) {
    ship x * 2✨
}

clanker add(a, b) {
    ship a + b✨
}

hallucinate(add(double(3), double(5)))✨"""
    assert run(source) == "16\n"


def test_multiple_nested_calls():
    """Multiple nested calls work correctly."""
    source = """clanker increment(n) {
    ship n + 1✨
}

hallucinate(increment(increment(increment(0))))✨"""
    assert run(source) == "3\n"


def test_deeply_nested_calls():
    """Deeply nested calls work correctly."""
    source = """clanker square(n) {
    ship n * n✨
}

hallucinate(square(square(2)))✨"""
    assert run(source) == "16\n"


def test_nil_returning_function_as_argument():
    """A function returning nil can be used as an argument."""
    source = """clanker returns_nil() {
}

clanker identity(x) {
    ship x✨
}

hallucinate(identity(returns_nil()))✨"""
    assert run(source) == "nil\n"
