from dataclasses import dataclass
from typing import Optional
import re


GAME = re.compile(r"Game (\d+)")
RED = re.compile(r"(\d+) red")
GREEN = re.compile(r"(\d+) green")
BLUE = re.compile(r"(\d+) blue")


@dataclass(frozen=True)
class Turn:
    red: int
    green: int
    blue: int


MAX_CUBES = Turn(red=12, green=13, blue=14)


@dataclass(frozen=True)
class Game:
    id: int
    turns: list[Turn]


def parse_game(line: str) -> Game:
    gameid_text, turns_text = line.split(":")
    m = GAME.match(gameid_text)
    gameid: Optional[int] = None
    if m is not None:
        gameid = int(m.group(1))
    else:
        raise ValueError(f"Game has no id, bad input: {gameid}")

    turns: list[Turn] = []
    for turn_text in turns_text.split(";"):
        red = 0
        green = 0 
        blue = 0
        for color in (clr.strip() for clr in turn_text.split(",")):
            match (RED.match(color), GREEN.match(color), BLUE.match(color)):
                case (m, None, None) if m is not None:
                    red = int(m.group(1))
                case (None, m, None) if m is not None:
                    green = int(m.group(1))
                case (None, None, m) if m is not None:
                    blue = int(m.group(1))
                case _:
                    raise ValueError(f"Turn had no colors, bad input: {turn_text}")
        turn = Turn(red=red, green=green, blue=blue)
        turns.append(turn)
    return Game(id=gameid, turns=turns)


def parse_games(lines: list[str]) -> list[Game]:
    return [parse_game(line.strip()) for line in lines]


def validate_game(game: Game, max_turn: Turn = MAX_CUBES) -> bool:
    for turn in game.turns:
        if turn.red > max_turn.red or turn.green > max_turn.green or turn.blue > max_turn.blue:
            return False
    return True


def find_power_of_least_cubes(game: Game) -> int:
    red = max((turn.red for turn in game.turns), default=0) 
    green = max((turn.green for turn in game.turns), default=0) 
    blue = max((turn.blue for turn in game.turns), default=0) 
    return red * green * blue


if __name__ == "__main__":
    with open("input.txt") as file:
        lines = file.readlines()
    games = parse_games(lines)
    valid_games = [game for game in games if validate_game(game)]
    print(sum(game.id for game in valid_games))

    total_powers = sum(find_power_of_least_cubes(game) for game in games)
    print(total_powers)