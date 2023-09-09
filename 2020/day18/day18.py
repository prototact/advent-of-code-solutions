from typing import Optional
from collections.abc import Callable, Iterator
from itertools import chain
from operator import add, mul


BinaryOp = Callable[[int, int], int]
Expression = int | tuple["Expression", tuple["Expression", bool], BinaryOp]


def peek(itr: Iterator[str] ) -> tuple[Optional[str], Iterator[str]]:
    try:
        char = next(itr)
    except StopIteration:
        return None, itr
    if char == " ":
        return peek(itr)
    return char, chain([char], itr)


def parse_number(digit: str, itr: Iterator[str]) -> tuple[int, Optional[str]]:
    num = ""
    while digit.isdigit():
        num += digit
        try:
            digit = next(itr)
        except StopIteration:
            return int(num), None
    return int(num), digit

def parse_operation(op: str) -> BinaryOp:
    if op == "+":
        return add
    if op == "*":
        return mul
    raise ValueError("Uknown operation")

def break_down(expr: Expression) -> Expression:
    if isinstance(expr, int):
        return expr
    expr1, (expr2, _), op1 = expr
    if isinstance(expr2, int):
        return expr
    expr3, (expr4, enclosed2), op2 = expr2
    if enclosed2:
        return expr
    newexpr = ((expr1, (expr3, False), op1), (expr4, enclosed2), op2)
    return newexpr

# add a enclosed expression with a boolean?
def parse_expression(itr: Iterator[str], big_expr: None | tuple[Expression] | tuple[Expression, BinaryOp] | Expression) -> Optional[Expression]:
    try:
        char = next(itr)
    except StopIteration:
        match big_expr:
            case None:
                return None
            case (expr,):
                return expr
            case (_, _):
                raise ValueError("Bad ending")
            case (_, _, _):
                return big_expr
            case _:
                raise ValueError("Wrong input")
    if char.isdigit():
        expr, next_char = parse_number(char, itr)
        match big_expr:
            case None:
                if next_char is not None:
                    return parse_expression(chain([next_char], itr), (expr,))
                else:
                    return parse_expression(itr, (expr,))
            case (_,):
                raise ValueError("Bad expression")
            case (expr1, op):
                if next_char is not None:
                    return parse_expression(chain([next_char], itr), (expr1, (expr, False), op))
                else:
                    return (expr1, (expr, False), op)
            case (_ ,_ ,_):
                raise ValueError("Bad expression")
            case _:
                raise ValueError("Bad expression")
    elif char == "(":
        match big_expr:
            case None:
                return parse_expression(itr, None)
            case (_,):
                raise ValueError("Bad expression")
            case (expr, op):
                expr1 = parse_expression(itr, None)
                if expr1 is not None:
                    return parse_expression(itr, (expr, (expr1, True), op))
                else:
                    raise ValueError("Bad expression")
            case (_, _, _):
                raise ValueError("Bad epxression")
            case _:
                raise ValueError(f"Bad expression {big_expr}")
    elif char == ")":
        match big_expr:
            case (expr,):
                return parse_expression(itr, (expr,))
            case (_, _):
                raise ValueError("Bad expression")
            case (_, _, _):
                return parse_expression(itr, big_expr)
            case _:
                raise ValueError("Bad expression")
    elif char in {"+", "*"}:
        op = parse_operation(char)
        match big_expr:
            case (expr,):
                return parse_expression(itr, (expr, op))
            case (_, _):
                raise ValueError("Bad expression")
            case (expr, expr1, op1):
                expr2 = parse_expression(itr, None)
                if expr2 is not None:
                    # the problem is here, expr2 should break down if it is not enclosed in parentheses
                    # a, (b, c, op), op1 -> (a, b, op1) , c, op
                    if isinstance(expr2, int):
                        return parse_expression(itr, ((expr, expr1, op1), (expr2, False), op))
                    else:
                        expr3, (expr4, enclosed), op2 = expr2
                        if not enclosed:
                            return parse_expression(itr, (((expr, expr1, op1), (expr3, False), op), (expr4, enclosed), op2))
                        else:
                            return parse_expression(itr, ((expr, expr1, op1), (expr2, enclosed), op))
                else:
                    raise ValueError("Bad expression")
            case _:
                raise ValueError("Bad expression")
    elif char == " ":
        return parse_expression(itr, big_expr)
    raise ValueError(f"this should be unreachable {char}{str(itr)}")


def parse_expressions(lines: list[str]) -> list[Expression]:
    expressions: list[Expression] = []
    for line in lines:
        line = line.strip()
        expr = parse_expression(iter(line), None)
        if expr is not None:
           expressions.append(expr)
    return expressions

def eval_expression(expression: Expression) -> int:
    if isinstance(expression, int):
        return expression
    expr1, (expr2, _), op = expression
    return op(eval_expression(expr1), eval_expression(expr2))


if __name__ == "__main__":
    with open("sample.txt") as file:
        expressions = parse_expressions(file.readlines())
    for expr in expressions:
        print(expr)
    results = [eval_expression(expression) for expression in expressions]
    assert results == [71, 51, 26, 437, 12240, 13632], results