"""
Pygame Module

This module contains the Pygame class

Author: John Fiorini
Date: 2024-11-10
"""
import pygame
from GameState import GameState
import queue


class Pygame:
    def __init__(self, ws, game_data_queue):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.game_state = GameState.GameStart
        self.game_data_queue = game_data_queue
        self.ws = ws
        self.screen = pygame.display.set_mode((1200, 720))
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.game_board_img = pygame.image.load("assets/textures/clue_board.jpg")
        self.game_board = self.game_board_img.get_rect()
        self.game_board.center = self.screen.get_rect().center

    def set_game_data_queue(self, queue):
        self.game_data_queue = queue

    def run(self):
        curr_game_data = ""
        while self.is_running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__quit()
                    self.is_running = False
                    return

            # POLL FOR CURRENT GAME DATA IF MESSAGE
            try:
                while not self.game_data_queue.empty():
                    curr_game_data = self.game_data_queue.get_nowait()
                    # print(f"Game data is {curr_game_data}")
            except queue.Empty:
                pass

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            # RENDER/LOGIC HERE BASED ON GAME STATE
            if self.game_state == GameState.GameStart:
                pass
            elif self.game_state == GameState.CharacterSelection:
                pass
            elif self.game_state == GameState.GameBoard:
                pass
            elif self.game_state == GameState.PlayerTurn:
                pass
            elif self.game_state == GameState.PlayerWin:
                pass
            elif self.game_state == GameState.PlayerLoss:
                pass
            else:
                print("ERROR: unknown game state")

            self.screen.blit(self.game_board_img, self.game_board)

            # DEBUG RENDER GAME STATE
            text_surface = self.font.render(curr_game_data, True, (255, 255, 255))
            self.screen.blit(text_surface, (0, 0))
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

    def __quit(self):
        pygame.quit()
        self.ws.close()
