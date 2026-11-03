# Sloperator

A tree-walking interpreter for [SlopLang](docs/spec.md), written in Python.

## Quick Start

```bash
# Run a program
uv run sloperator.py path/to/program.slop

# Check syntax without executing
uv run sloperator.py --check path/to/program.slop

# Validation
uv run pytest              # tests
uv run ruff format --check # formatting
uv run ruff check          # linting
uv run ty check            # type checking
```

## Example

```slop
clanker describe(count) {
    vibe count > 1 {
        ship "big slop"✨
    } nah {
        ship "small slop"✨
    }
}

loadbearing MAX = 3✨
slop count = 0✨

ralph count < MAX {
    hallucinate(describe(count))✨
    count = count + 1✨
}
```

Prints `small slop` twice, then `big slop`.

See [docs/spec.md](docs/spec.md) for the complete language specification.
