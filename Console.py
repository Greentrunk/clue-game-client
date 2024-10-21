"""
Console Module

This module contains the Console class

Author: Christopher Pohl
Date: 2024-10-21
"""
from GameState import GameState
import queue


class Console:
    def __init__(self, ws, game_data_queue):
        self.game_state = GameState.GameStart
        self.ws = ws
        self.game_data_queue = game_data_queue
        self.is_running = True

    def run(self):
        curr_game_data = ""
        while self.is_running:
            # POLL FOR CURRENT GAME DATA IF MESSAGE
            try:
                while not self.game_data_queue.empty():
                    curr_game_data = self.game_data_queue.get_nowait()
                    print(f"Game data is {curr_game_data}")
            except queue.Empty:
                pass

            # RENDER/LOGIC HERE BASED ON GAME STATE
            if self.game_state == GameState.GameStart:
                pass
            elif self.game_state == GameState.CharacterSelection:
                pass
            elif self.game_state == GameState.GameBoard:
                self.__print_game_board()
            elif self.game_state == GameState.PlayerTurn:
                pass
            elif self.game_state == GameState.PlayerWin:
                pass
            elif self.game_state == GameState.PlayerLoss:
                pass
            else:
                print("ERROR: unknown game state")

    def __print_game_board(self):
        pass

    def __wait_for_input(self, instruction):
        message = input(instruction)
