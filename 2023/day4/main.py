import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Optional

CARD = re.compile(r"Card (?:\s*\d+)\:((?:\s+\d+)+) \|((?:\s+\d+)+)")


@dataclass(frozen=True)
class Card:
    winning: list[int]
    have: list[int]

    @classmethod
    def parse_card(cls, line: str) -> Optional["Card"]:
        m = CARD.match(line)
        if m is not None:
            winning = [int(num) for num in m.group(1).strip().split()]
            have = [int(num) for num in m.group(2).strip().split()]
            return cls(winning, have)


@dataclass(frozen=True)
class ScoredCard:
    count: int

    @classmethod
    def compute_score(cls, card: Card) -> "ScoredCard":
        return cls(len(set(card.winning) & set(card.have)))

    @property
    def score(self) -> int:
        if self.count == 0:
            return 0
        return 2 ** (self.count - 1)


def proliferate(cards: list[ScoredCard]) -> int:
    batch = {idx: 1 for idx, _ in enumerate(cards, start=1)}
    max_card_no = len(cards)

    def go(batch: dict[int, int], acc: int) -> int:
        batch_count = sum(batch.values())
        if batch_count == 0:
            return acc
        new_batch: dict[int, int] = {}
        for card_no, num_copies in batch.items():
            card_copies = (
                card_no + idx
                for idx in range(1, cards[card_no - 1].count + 1)
                if card_no + idx <= max_card_no
            )
            for copy_card_no in card_copies:
                new_batch[copy_card_no] = new_batch.get(copy_card_no, 0) + num_copies
        return go(new_batch, acc + batch_count)

    return go(batch, 0)


def proliferate_iterative(cards: list[ScoredCard]) -> int:
    batch = {idx: 1 for idx, _ in enumerate(cards, start=1)}
    max_card_no = len(cards)

    batch_count = sum(batch.values())
    acc = batch_count
    while batch_count > 0:
        new_batch: dict[int, int] = {}
        for card_no, num_copies in batch.items():
            card_copies = (
                card_no + idx
                for idx in range(1, cards[card_no - 1].count + 1)
                if card_no + idx <= max_card_no
            )
            for copy_card_no in card_copies:
                new_batch[copy_card_no] = new_batch.get(copy_card_no, 0) + num_copies
        batch = new_batch
        batch_count = sum(batch.values())
        acc += batch_count

    return acc


def filterOptional[A](iterable: Iterable[A | None]) -> list[A]:
    return [value for value in iterable if value is not None]


def parse_cards(lines: list[str]) -> list[Card]:
    return filterOptional(Card.parse_card(line.strip()) for line in lines)


if __name__ == "__main__":
    with open("sample.txt") as file:
        cards = parse_cards(file.readlines())
    scored_cards = [ScoredCard.compute_score(card) for card in cards]
    assert sum(card.score for card in scored_cards) == 13
    assert (total := proliferate_iterative(scored_cards)) == 30, total

    with open("input.txt") as file:
        cards = parse_cards(file.readlines())
    scored_cards = [ScoredCard.compute_score(card) for card in cards]
    print(sum(card.score for card in scored_cards))
    print(proliferate_iterative(scored_cards))
