"""
GUI Module

This module contains the GameState class

Author: Christopher Pohl
Date: 2024-10-21
"""

from enum import Enum


class GameState(Enum):
    GameStart = "Game Start"
    CharacterSelection = "Character Selection"
    GameBoard = "Game Board"
    PlayerTurn = "Player Turn"
    PlayerWin = "Player Win"
    PlayerLoss = "Player Loss"



