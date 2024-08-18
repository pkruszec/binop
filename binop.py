from dataclasses import dataclass
from typing import Self, Union
from enum import Enum, auto

# Lexer

Token = Union[int | str]

# NOTE: This is a very simplified lexer.
# It does not support comments, floats, or operators longer than one character.
# It is here just to make writing tests faster.
def lexer_next(text: str) -> tuple[str, Token | None]:
    ops = ['(', ')', '+', '-', '*', '/']
    
    # Eliminate whitespace
    for i, c in enumerate(text):
        if not c.isspace():
            text = text[i:]
            break

    idx = None
    token_type = None
    token_value = []
    for i, c in enumerate(text):
        if token_type is None:
            if c in ops:
                return (text[i+1:], c)
            elif c.isdigit():
                token_type = int
                token_value.append(c)
                idx = i + 1
            else:
                raise ValueError
        elif token_type == int:
            if not c.isdigit():
                idx = i
                break
            token_value.append(c)
            
    if token_type == int:
        return (text[idx:], int("".join(token_value)))
            
    return (text[idx:], None)

def lexer_lex_text(text: str) -> list[Token]:
    tokens = []
    while True:
        text, token = lexer_next(text)
        if token is None:
            break
        tokens.append(token)
    return tokens
        
# Parser

class NodeKind(Enum):
    INT = 0
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    MINUS_UNARY = auto()

@dataclass
class Node:
    kind: NodeKind
    children: list[Self]

    # Just for testing
    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False
        return self.kind == other.kind and self.children == other.children
    
def next_token(tokens):
    return tokens.pop(0) if tokens else None

def peek_token(tokens):
    return tokens[0] if tokens else None

def parse_expr(tokens):
    return parse_plus(tokens)

def parse_plus(tokens):
    # Handling unary + and - operators
    token = peek_token(tokens)
    kind = None
    if isinstance(token, str):
        if token == '+':
            next_token(tokens)
        if token == '-':
            kind = NodeKind.MINUS_UNARY
            next_token(tokens)

    node = (
        parse_term(tokens)
        if kind is None else
        Node(kind, [parse_term(tokens)])
    )
    
    while True:
        token = peek_token(tokens)
        if not isinstance(token, str):
            break
        kind = None
        if token == '+':
            kind = NodeKind.PLUS
        elif token == '-':
            kind = NodeKind.MINUS
        else:
            break
        next_token(tokens)
        f1 = parse_term(tokens)

        node = Node(kind, [node, f1])

    return node

def parse_term(tokens):
    node = parse_factor(tokens)
    
    while True:    
        token = peek_token(tokens)
        if not isinstance(token, str):
            break
        kind = None
        if token == '*':
            kind = NodeKind.MUL
        elif token == '/':
            kind = NodeKind.DIV
        else:
            break
        next_token(tokens)
        f1 = parse_factor(tokens)

        node = Node(kind, [node, f1])

    return node

def parse_factor(tokens):
    token = next_token(tokens)
    if isinstance(token, int):
        return Node(NodeKind.INT, [token])
    if not isinstance(token, str):
        raise ValueError
    
    if token != '(':
        raise ValueError
    
    expr = parse_expr(tokens)

    token = next_token(tokens)
    if token != ')':
        raise ValueError

    return expr

def calculate_expr(expr: Node) -> int:
    if expr.kind == NodeKind.INT:
        return expr.children[0]
    elif expr.kind == NodeKind.PLUS:
        return calculate_expr(expr.children[0]) + calculate_expr(expr.children[1])
    elif expr.kind == NodeKind.MINUS:
        return calculate_expr(expr.children[0]) - calculate_expr(expr.children[1])
    elif expr.kind == NodeKind.MUL:
        return calculate_expr(expr.children[0]) * calculate_expr(expr.children[1])
    elif expr.kind == NodeKind.DIV:
        return calculate_expr(expr.children[0]) // calculate_expr(expr.children[1])
    elif expr.kind == NodeKind.MINUS_UNARY:
        return -1 * calculate_expr(expr.children[0])
    
    return 0
