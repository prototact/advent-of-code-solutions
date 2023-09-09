from typing import Optional
from collections.abc import Iterator, Callable
from itertools import chain
from dataclasses import dataclass
from operator import add, mul


BinaryOp = Callable[[int, int], int]


@dataclass(frozen=True)
class Expression:
    ...


@dataclass(frozen=True)
class Number(Expression):
    value: int


@dataclass(frozen=True)
class Enclosed(Expression):
    value: Expression

@dataclass(frozen=True)
class Node(Expression):
    start: Number | Enclosed
    values: list[tuple[Expression, BinaryOp]]
    next_op: Optional[BinaryOp]


def peek(itr: Iterator[str]) -> tuple[Iterator[str], Optional[str]]:
    try: 
        char = next(itr)
    except StopIteration:
        return itr, None
    return chain([char], itr), char


def parse_number(itr: Iterator[str]) -> tuple[int, Iterator[str]]: 
    num = ""
    itr, char = peek(itr)
    while char is not None and char.isdigit():
        num += next(itr)
        itr, char = peek(itr)
    return int(num), itr

def parse_operation(char: str) -> BinaryOp:
    if char == "+":
        return add
    if char == "*":
        return mul
    raise ValueError(f"Unknown Operation {char}")


def parse_expression(itr: Iterator[str], expr: Optional[Expression] = None) -> Optional[Expression]:
    itr, char = peek(itr)
    if char is None:
        return expr
    if char.isdigit():
        number, itr = parse_number(itr)
        expr1 = Number(value=number)
        match expr:
            case None:
                node = Node(start=expr1, values=[], next_op=None)
                return parse_expression(itr, node)
            case Number(value=number):
                raise ValueError(f"Cannot combine two leaves without operation {number} {expr1.value}, remaining: {''.join(itr)}")
            case Enclosed(value=expr2):
                raise ValueError(f"Cannot combine a number to an enclosed value without operation {expr2} {expr1.value}, remaining: {''.join(itr)}")
            case Node(start=sexpr, values=exprs, next_op=op):
                # here the context should include an operation, in order to add to values
                if op is None:
                    raise ValueError("A Node should parse the next operator to expect an Enclosed or Number Expression")
                exprs.append((expr1, op))
                new_node = Node(start=sexpr, values=exprs, next_op=None)
                return parse_expression(itr, new_node)
            case _:
                raise ValueError(f"Unexpected parsing {expr}, remaining: {''.join(itr)}")
    if char == "(":
        next(itr)
        enclosed = parse_expression(itr, None)
        if enclosed is not None:
            match expr:
                case None:
                    assert isinstance(enclosed, Enclosed)
                    node = Node(start=enclosed, values=[], next_op=None)
                    return parse_expression(itr, node)
                case Number(value=_):
                    raise ValueError(f"Cannot combine number with enclosed value")
                case Enclosed(value=_):
                    raise ValueError(f"Cannot combine enclosed values")
                case Node(start=start, values=values, next_op=op):
                    if op is None:
                        raise ValueError(f"Cannot combine node {expr} with {enclosed} without next operation")
                    values.append((enclosed, op))
                    node = Node(start=start, values=values, next_op=None)
                    return parse_expression(itr, node)
                case _:
                    raise ValueError(f"Unknown expression {expr}")
        raise ValueError(f"Parentheses {enclosed} should be followed by something {''.join(c for c in itr)}")
    if char == ")":
        next(itr)
        match expr:
            case Node(start=start, values=values, next_op=op):
                if op is not None:
                    raise ValueError(f"Closing parentheses cannot be preceded by operation {op}, remaining {str(''.join(itr))}")
                return Enclosed(value=expr)
            case _:
                raise ValueError(f"Closing parentheses should be preceded by some expression {expr}, remaining {str(''.join(itr))}") 
    if char in {"+", "*"}:
        if expr is None:
            raise ValueError(f"Bad expression {''.join(itr)}")
        try:
            op = parse_operation(next(itr))
        except ValueError:
            raise
        match expr:
            case Node(start=start, values=values, next_op=op1):
                if op1 is not None:
                    raise ValueError(f"Two operators followed each other {op1} {op}, remaining {''.join(itr)}")
                node = Node(start=start, values=values, next_op=op)
                return parse_expression(itr, node)
            case Number(value=value):
                node = Node(start=Number(value), values=[], next_op=op)
                return parse_expression(itr, node)
            case Enclosed(value=value):
                node = Node(start=Enclosed(value=value), values=[], next_op=op)
                return parse_expression(itr, node)
            case _:
                raise ValueError(f"Operation {op} must be preceded by some value {expr} , remaining {''.join(itr)}")
    if char == " ":
        next(itr)
        return parse_expression(itr, expr)
    raise ValueError(f"Unreachable state {expr}, remaining: {''.join(itr)}")


def parse_expressions(lines: list[str]) -> list[Expression]:
    exprs: list[Expression] = []
    for line in lines:
        line = line.strip()
        expr = parse_expression(iter(line))
        if expr is not None:
            exprs.append(expr)
    return exprs


def eval_expression(expr: Expression) -> int:
    match expr:
        case Number(value=number):
            return number
        case Enclosed(value=value):
            return eval_expression(value)
        case Node(start=start, values=values, next_op=_):
            number = eval_expression(start)
            for value, op in values:
                number = op(number, eval_expression(value))
            return number
        case _:
            raise ValueError(f"Unknown expression: {expr}")


def eval_expression_order(expr: Expression) -> int:
    match expr:
        case Number(value=number):
            return number
        case Enclosed(value=value):
            return eval_expression_order(value)
        case Node(start=start, values=values, next_op=_):
            number = eval_expression_order(start)
            terms: list[tuple[int, BinaryOp]] = []
            current = number
            for expr, op in values:
                if op == add:
                    current = op(current, eval_expression_order(expr))
                else:
                    terms.append((current, op))
                    current = eval_expression_order(expr)
            for value, op in terms[::-1]:
                current = op(value, current)
            return current
        case _:
            raise ValueError(f"Unknown expression: {expr}")


if __name__ == "__main__":
    with open("sample.txt") as file:
        lines = file.readlines()
    exprs = parse_expressions(lines)

    results = [eval_expression(expr) for expr in exprs]
    assert results == [71, 51, 26, 437, 12240, 13632], results

    results_ord = [eval_expression_order(expr) for expr in exprs]
    assert results_ord == [231, 51, 46, 1445, 669060, 23340], results_ord

    with open("input.txt") as file:
        lines = file.readlines()
    exprs = parse_expressions(lines)

    results = [eval_expression(expr) for expr in exprs]
    print(sum(results))

    results_ord = [eval_expression_order(expr) for expr in exprs]
    print(sum(results_ord))
