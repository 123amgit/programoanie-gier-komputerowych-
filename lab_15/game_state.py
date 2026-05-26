# game_state.py
# Globalna maszyna stanów gry.

from enum import Enum, auto


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    WIN = auto()
