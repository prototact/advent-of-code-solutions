from abc import ABC, abstractmethod
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass
from enum import IntEnum
from typing import Self, final


class Card(IntEnum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14


CARDMAP = dict(zip("23456789TJQKA", Card))


class JokeCard(IntEnum):
    Jack = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Queen = 11
    King = 12
    Ace = 13


JOKECARDMAP = dict(zip("J23456789TQKA", JokeCard))


class Hands(IntEnum):
    High_Card = 0
    Pair = 1
    Two_Pair = 2
    Three_of_a_Kind = 3
    Full_House = 4
    Four_of_a_Kind = 5
    Five_of_a_Kind = 6


@dataclass
class Hand[A: IntEnum](ABC):
    _hand: list[A]

    @classmethod
    @abstractmethod
    def parse_hand(cls, hand: str) -> Self:
        ...

    @final
    def __iter__(self) -> Iterator[A]:
        yield from self._hand

    @property
    @abstractmethod
    def _eval_hand(self) -> Hands:
        ...

    @property
    @final
    def by_hand(self) -> list[int]:
        return [int(self._eval_hand), *map(int, self)]


@dataclass
class NormalHand(Hand[Card]):
    @classmethod
    def parse_hand(cls, hand: str) -> Self:
        return cls([CARDMAP[card] for card in hand])

    @property
    def _eval_hand(self) -> Hands:
        count = Counter(self)
        match count.most_common(2):
            case [(_, 1), _]:
                return Hands.High_Card
            case [(_, 2), (_, 1)]:
                return Hands.Pair
            case [(_, 2), (_, 2)]:
                return Hands.Two_Pair
            case [(_, 3), (_, 1)]:
                return Hands.Three_of_a_Kind
            case [(_, 3), (_, 2)]:
                return Hands.Full_House
            case [(_, 4), _]:
                return Hands.Four_of_a_Kind
            case [(_, 5)]:
                return Hands.Five_of_a_Kind
            case _:
                raise ValueError(f"Unreachable {self._hand}!")


@dataclass
class JokeHand(Hand[JokeCard]):
    @classmethod
    def parse_hand(cls, hand: str) -> Self:
        return cls([JOKECARDMAP[card] for card in hand])

    @property
    def _eval_hand(self) -> Hands:
        count = Counter(self)
        jokers = count.get(JokeCard.Jack, 0)
        del count[JokeCard.Jack]
        match (count.most_common(2), jokers):
            case ([(_, 1), _], 0):
                return Hands.High_Card
            case ([(_, 1), _], 1):
                return Hands.Pair
            case ([(_, 1), _], 2):
                return Hands.Three_of_a_Kind
            case ([(_, 1), _], 3):
                return Hands.Four_of_a_Kind
            case ([(_, 1)], 4):
                return Hands.Five_of_a_Kind
            case ([(_, 2), (_, 1)], 0):
                return Hands.Pair
            case ([(_, 2), (_, 1)], 1):
                return Hands.Three_of_a_Kind
            case ([(_, 2), (_, 1)], 2):
                return Hands.Four_of_a_Kind
            case ([(_, 2)], 3):
                return Hands.Five_of_a_Kind
            case ([(_, 2), (_, 2)], 0):
                return Hands.Two_Pair
            case ([(_, 2), (_, 2)], 1):
                return Hands.Full_House
            case ([(_, 3), (_, 1)], 0):
                return Hands.Three_of_a_Kind
            case ([(_, 3), (_, 1)], 1):
                return Hands.Four_of_a_Kind
            case ([(_, 3), (_, 2)], 0):
                return Hands.Full_House
            case ([(_, 3)], 2):
                return Hands.Five_of_a_Kind
            case ([(_, 4), (_, 1)], 0):
                return Hands.Four_of_a_Kind
            case ([(_, 4)], 1):
                return Hands.Five_of_a_Kind
            case ([(_, 5)], 0):
                return Hands.Five_of_a_Kind
            case ([], 5):
                return Hands.Five_of_a_Kind
            case _:
                raise ValueError(f"Unreachable {self._hand}!")


def rank_hands[A: IntEnum](hands: list[tuple[Hand[A], int]]) -> int:
    sorted_hands = sorted(hands, key=lambda x: x[0].by_hand)
    return sum(rank * dip for rank, (_, dip) in enumerate(sorted_hands, start=1))


def parse_hands_and_dips[A: IntEnum](
    lines: list[str], type_: type[Hand[A]]
) -> list[tuple[Hand[A], int]]:
    return [
        (type_.parse_hand(hand), int(dip))
        for hand, dip in (line.strip().split() for line in lines)
    ]


if __name__ == "__main__":
    with open("sample.txt") as file:
        hands = parse_hands_and_dips(file.readlines(), NormalHand)
    total_returns = rank_hands(hands)
    assert total_returns == 6440

    with open("sample.txt") as file:
        hands = parse_hands_and_dips(file.readlines(), JokeHand)
    total_returns = rank_hands(hands)
    assert total_returns == 5905

    with open("input.txt") as file:
        hands = parse_hands_and_dips(file.readlines(), NormalHand)
    total_returns = rank_hands(hands)
    print(total_returns)

    with open("input.txt") as file:
        hands = parse_hands_and_dips(file.readlines(), JokeHand)
    total_returns = rank_hands(hands)
    print(total_returns)
