"""
Pygame Module

This module contains the Pygame class

Author: John Fiorini
Date: 2024-11-10
"""
import pygame
from pygame.examples.go_over_there import screen, CIRCLE_RADIUS

from GameState import GameState
from Gameboard import spawnLocations, charColors
from Gameboard import Grid

import queue


CIRCLE_R = 15

class Pygame:

    def __init__(self, ws, game_data_queue):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.game_state = GameState.GameStart
        self.game_data_queue = game_data_queue
        self.ws = ws
        self.screen = pygame.display.set_mode((1245, 688))
        self.clock = pygame.time.Clock()
        self.is_running = True

    def setupGameboard(self):
        self.game_board_img = pygame.image.load("assets/textures/Map.png")
        self.game_board = self.game_board_img.get_rect()
        self.game_board.center = self.screen.get_rect().center

    def testGrid(selfself):
        # Create a Grid object
        grid = Grid(7, 7, 95, screen)
        grid.draw_circles()
        grid.draw_grid_lines()



    def placeCharacters(self):
        # Using draw.rect module of
        # pygame to draw the solid circle

        self.screen.blit(self.game_board_img, self.game_board)

        # Miss scarlet
        pygame.draw.circle(self.screen, charColors.SCARLET.value,
                           spawnLocations.spawnScarlet.value, CIRCLE_R, 0)
        # Col. Mustard
        pygame.draw.circle(self.screen,  charColors.MUSTARD.value,
                           spawnLocations.spawnMustard.value, CIRCLE_R, 0)
        # Professor Plum
        pygame.draw.circle(self.screen, charColors.PLUM.value,
                           spawnLocations.spawnPlum.value, CIRCLE_R, 0)
        # Miss Peacock
        pygame.draw.circle(self.screen, charColors.PEACOCK.value,
                           spawnLocations.spawnPeacock.value, CIRCLE_R, 0)
        # Mr Green
        pygame.draw.circle(self.screen, charColors.GREEN.value,
                           spawnLocations.spawnGreen.value, CIRCLE_R, 0)
        # Miss White
        pygame.draw.circle(self.screen, charColors.WHITE.value,
                           spawnLocations.spawnWhite.value, CIRCLE_R, 0)


        pygame.display.update()


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
            #self.screen.fill("black")

            self.game_state = curr_game_data


            # RENDER/LOGIC HERE BASED ON GAME STATE
            if self.game_state == GameState.GameStart.value:
                pass
            elif self.game_state == GameState.CharacterSelection.value:

                pass
            elif self.game_state == GameState.GameBoard.value:
                self.setupGameboard()
                # self.testGrid()
                self.placeCharacters()

                pass
            elif self.game_state == GameState.PlayerTurn.value:


                pass
            elif self.game_state == GameState.PlayerWin.value:
                pass
            elif self.game_state == GameState.PlayerLoss.value:
                pass
            else:
                print("ERROR: unknown game state")


            # DEBUG RENDER GAME STATE
            text_surface = self.font.render(curr_game_data, True, (0, 255, 255))
            self.screen.blit(text_surface, (0, 0))
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

    def __quit(self):
        pygame.quit()
        self.ws.close()

