import pytest
from binop import *

@pytest.mark.parametrize("text, expected", [
    ("1+2", [1, '+', 2]),
    ("(2)*3+2", ['(', 2, ')', '*', 3, '+', 2]),
])
def test_lexer(text, expected):
    assert lexer_lex_text(text) == expected

@pytest.mark.parametrize("text, expected", [
    ("32", Node(NodeKind.INT, [32])),
    ("(32)", Node(NodeKind.INT, [32])),
    (
        "32 * 8",
        Node(NodeKind.MUL, [
            Node(NodeKind.INT, [32]),
            Node(NodeKind.INT, [8]),
        ])
    ),
    (
        "5 / (4)",
        Node(NodeKind.DIV, [
            Node(NodeKind.INT, [5]),
            Node(NodeKind.INT, [4]),
        ])
    ),
    (
        "32 + 8",
        Node(NodeKind.PLUS, [
            Node(NodeKind.INT, [32]),
            Node(NodeKind.INT, [8]),
        ])
    ),
    (
        "2 + 2 + 2",
        Node(NodeKind.PLUS, [
            Node(NodeKind.PLUS, [
                Node(NodeKind.INT, [2]),
                Node(NodeKind.INT, [2]),
            ]),
            Node(NodeKind.INT, [2]),
        ])
    ),
    (
        "2 + 2 - 4",
        Node(NodeKind.MINUS, [
            Node(NodeKind.PLUS, [
                Node(NodeKind.INT, [2]),
                Node(NodeKind.INT, [2]),
            ]),
            Node(NodeKind.INT, [4]),
        ])
    ),
    (
        "2 + 2 - 4*3",
        Node(NodeKind.MINUS, [
            Node(NodeKind.PLUS, [
                Node(NodeKind.INT, [2]),
                Node(NodeKind.INT, [2]),
            ]),
            Node(NodeKind.MUL, [
                Node(NodeKind.INT, [4]),
                Node(NodeKind.INT, [3]),
            ]),
        ])
    ),
    (
        "2 * 2 * 2",
        Node(NodeKind.MUL, [
            Node(NodeKind.MUL, [
                Node(NodeKind.INT, [2]),
                Node(NodeKind.INT, [2]),
            ]),
            Node(NodeKind.INT, [2]),
        ])
    ),
    (
        "(32 + 8) * 3",
        Node(NodeKind.MUL, [
            Node(NodeKind.PLUS, [
                Node(NodeKind.INT, [32]),
                Node(NodeKind.INT, [8]),
            ]),
            Node(NodeKind.INT, [3]),
        ])
    ),
])
def test_ast(text, expected):
    tokens = lexer_lex_text(text)
    assert parse_expr(tokens) == expected

@pytest.mark.parametrize("text, result", [
    ("534", 534),
    ("2+2", 4),
    ("1+1+1+1+1+1+1", 7),
    ("2*3+2", 8),
    ("12 * 32 + 2", 386),
    ("54 - 2 + 2", 54),
    ("2 + 2 * 2", 6),
    ("(2 + 2) * 2", 8),
    ("(-2 + 2) * 2", 0),
    ("+(2 + (-2)) * 2", 0),
    ("-3 + 4", 1),
    ("-(3 + 4)", -7),
])
def test_calc(text, result):
    tokens = lexer_lex_text(text)
    expr = parse_expr(tokens)
    assert calculate_expr(expr) == result

