# Sloperator Agent Guide

## Quick Reference

```bash
# Run program
uv run sloperator.py path/to/file.slop

# Syntax check only
uv run sloperator.py --check path/to/file.slop

# Run all validation
uv run ruff format --check
uv run ruff check
uv run ty check
uv run pytest

# Run single test file
uv run pytest tests/test_name.py -v

# Playground dev server
uv run playground/server.py  # http://localhost:8080
```

## Architecture

```
sloperator.py           # CLI entrypoint
sloperator/
  lexer/                # UTF-8 source → tokens
    tokens.py           # Token types and definitions
    scanner.py          # Lexer implementation
  parser/               # Tokens → AST
    ast.py              # Node definitions (dataclasses)
    parser.py           # Recursive descent parser
  evaluator/            # AST → execution
    values.py           # Runtime value types
    environment.py      # Variable scoping
    interpreter.py      # Tree-walking interpreter
  runner.py             # Orchestrates lexer → parser → evaluator
  errors.py             # Error types and formatting
docs/spec.md            # Complete language specification
examples/               # Reference programs
playground/             # Web REPL (POST /run endpoint)
tests/                  # Pytest suite
```

## SlopLang Essentials

- **Emoji tokens matter**: `✨` (statement terminator), `✅`/`❌` (booleans), `—` (comments)
- **No truthiness**: conditions must be booleans, not numbers or other types
- **Curly quotes for strings**: `"hello"` not `"hello"` (lexer rejects straight quotes)
- **No implicit conversions**: operations reject mismatched types at runtime
- **Scoping**: blocks create lexical scopes, assignment searches up, inner `slop` can shadow outer `loadbearing`

## Testing Quirks

- Use `from sloperator.runner import run_source` for end-to-end tests
- Result has `.stdout`, `.stderr`, `.exit_code`
- Error format: `SlopLang {kind} error at line {n}: {message}\n`
- See `tests/test_errors.py` for error message regression patterns
- Parametrized tests use source snippets and expected output

## Python Requirements

- **Requires Python ≥3.13** (enforced in `pyproject.toml`)
- All code uses standard library only (no runtime dependencies)
- Dev tools: pytest, ruff (lint+format), ty (type check)
- Type hints required for all functions

## Common Pitfalls

1. **Emoji token variants**: Some input methods add U+FE0F variation selector after `✨`/`✅`/`❌`. The lexer accepts both with and without the selector.
2. **Error line numbers are 1-indexed** in error messages but the implementation tracks them as 0-indexed internally.
3. **Recursion limit is 500 calls** to prevent infinite recursion (`MAX_CALL_DEPTH` in `interpreter.py`). Python's recursion limit is raised to 20,000 in `runner.py`.
4. **Playground logs to `logs/`** which is git-ignored and watcher-ignored per `opencode.jsonc`.

## Language Specification

Full spec in `docs/spec.md`. It is the source of truth. When in doubt, check there or run test cases from `examples/`.
