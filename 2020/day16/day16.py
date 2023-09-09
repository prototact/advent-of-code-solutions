from typing import Optional
from collections.abc import Iterator
from dataclasses import dataclass
import re


Rules = dict[str, tuple[range, range]]


RULE = re.compile(r"((?:\w+\s*)+)\: (\d+\-\d+) or (\d+\-\d+)")


@dataclass
class Ticket:
    field_values: list[int]


def parse_rules(lines: Iterator[str]) -> tuple[Rules, Iterator[str]]:
    rules: Rules = {}
    for line in lines:
        line = line.strip()
        if not line:
            break
        match = RULE.match(line)
        if match is not None:
            name, rng1, rng2 = match.groups()
            left1, right1 = [int(num) for num in rng1.split("-")]
            left2, right2 = [int(num) for num in rng2.split("-")]
            rules[name] = (range(left1, right1 + 1), range(left2, right2 + 1))
        else:
            raise ValueError(f"Unknown rule format {line}")
    return rules, lines


def parse_my_ticket(lines: Iterator[str]) -> tuple[Ticket, Iterator[str]]:
    ticket: Optional[Ticket] = None
    for line in lines:
        line = line.strip()
        if line == "your ticket:":
            continue
        if not line:
            break
        field_values = [int(value) for value in line.split(",")]
        ticket = Ticket(field_values)
    if ticket is not None:
        return ticket, lines
    raise ValueError("My ticket not found.")


def parse_other_tickets(lines: Iterator[str]) -> tuple[list[Ticket], Iterator[str]]:
    tickets: list[Ticket] = []
    for line in lines:
        line = line.strip()
        if line == "nearby tickets:":
            continue
        field_values = [int(value) for value in line.split(",")]
        ticket = Ticket(field_values)
        tickets.append(ticket)
    return tickets, lines


def find_ticket_invalid_values(ticket: Ticket, rules: Rules) -> list[int]:
    invalid_values: list[int] = []
    for value in ticket.field_values:
        if all((value not in rng1) and (value not in rng2) for rng1, rng2 in rules.values()):
            invalid_values.append(value)
    return invalid_values   


def find_all_tickets_invalid_values(tickets: list[Ticket], rules: Rules) -> tuple[list[int], list[Ticket]]:
    invalid_values: list[int] = []
    valid_tickets: list[Ticket] = []
    for ticket in tickets:
        invalid = find_ticket_invalid_values(ticket, rules)
        if invalid:
            invalid_values.extend(invalid)
        else:
            valid_tickets.append(ticket)
    return invalid_values, valid_tickets


if __name__ == "__main__":
    with open("sample.txt") as file:
        itr = iter(file.readlines())
    rules, itr = parse_rules(itr)
    my_ticket, itr = parse_my_ticket(itr)
    other_tickets, _ = parse_other_tickets(itr)
    
    invalid_values, _ = find_all_tickets_invalid_values(other_tickets, rules)
    assert (result := sum(invalid_values)) == 71, result

    with open("input.txt") as file:
        itr = iter(file.readlines())
    rules, itr = parse_rules(itr)
    my_ticket, itr = parse_my_ticket(itr)
    other_tickets, _ = parse_other_tickets(itr)
    
    invalid_values, valid_tickets = find_all_tickets_invalid_values(other_tickets, rules)
    print(sum(invalid_values))
