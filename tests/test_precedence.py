from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, Call, ExprStmt, Grouping, Literal
from sloperator.runner import run_source


def parse_expression(source: str):
    program = parse(tokenize(f"hallucinate({source})✨"))
    statement = program[0]
    assert isinstance(statement, ExprStmt)
    call = statement.expression
    assert isinstance(call, Call)
    (argument,) = call.arguments
    return argument


def test_multiplication_binds_tighter_than_addition():
    expression = parse_expression("1 + 2 * 3")

    assert isinstance(expression, Binary)
    assert expression.operator.type is TokenType.PLUS
    assert isinstance(expression.left, Literal)
    assert expression.left.value == 1

    assert isinstance(expression.right, Binary)
    assert expression.right.operator.type is TokenType.STAR
    assert isinstance(expression.right.left, Literal)
    assert expression.right.left.value == 2
    assert isinstance(expression.right.right, Literal)
    assert expression.right.right.value == 3


def test_parentheses_override_precedence():
    expression = parse_expression("(1 + 2) * 3")

    assert isinstance(expression, Binary)
    assert expression.operator.type is TokenType.STAR
    assert isinstance(expression.left, Grouping)
    assert isinstance(expression.right, Literal)
    assert expression.right.value == 3


def test_multiplication_is_evaluated_before_addition():
    result = run_source("hallucinate(1 + 2 * 3)✨")

    assert result.stderr == ""
    assert result.stdout == "7\n"
