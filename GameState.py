"""
GUI Module

This module contains the GameState class

Author: Christopher Pohl
Date: 2024-10-21
"""

from enum import Enum


class GameState(Enum):
    GameStart = 1
    CharacterSelection = 2
    GameBoard = 3
    PlayerTurn = 4
    PlayerWin = 5
    PlayerLoss = 6
