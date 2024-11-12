"""
Pygame Module

This module contains the Pygame class

Author: John Fiorini & Christopher Pohl
Date: 2024-11-10
"""
import pygame

from GameState import GameState
from Gameboard import spawnLocations, charColors
from Gameboard import Grid

import json
import queue

CIRCLE_R = 15


class Pygame:

    def __init__(self, ws, game_data_queue):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.game_state = GameState.GameStart
        self.game_data = {}
        self.game_data_queue = game_data_queue
        self.ws = ws
        self.screen = pygame.display.set_mode((1245, 688))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.player_name = ""

    def setupGameboard(self):
        self.game_board_img = pygame.image.load("assets/textures/Map.png")
        self.game_board = self.game_board_img.get_rect()
        self.game_board.center = self.screen.get_rect().center

    def testGrid(self):
        # Create a Grid object
        grid = Grid(7, 7, 95, self.screen)
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
        pygame.draw.circle(self.screen, charColors.MUSTARD.value,
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
        curr_game_data = {}
        while self.is_running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__quit()
                    self.is_running = False
                    self.ws.close()
                    return

            # POLL FOR CURRENT GAME DATA IF MESSAGE
            try:
                while not self.game_data_queue.empty():
                    curr_game_data = self.game_data_queue.get_nowait()
                    # print(f"Game data is {curr_game_data}")
            except queue.Empty:
                pass

            # fill the screen with a color to wipe away anything from last frame
            # self.screen.fill("black")

            self.game_data = curr_game_data

            # Check who's turn
            if self.game_data["player_turn"] == self.player_name:
                self.game_state = GameState.PlayerTurn


            # RENDER/LOGIC HERE BASED ON GAME STATE
            if self.game_state == GameState.GameStart:
                # Temp for minimal
                self.game_state = GameState.CharacterSelection

            elif self.game_state == GameState.CharacterSelection:
                player_name = input("Enter player name: \n")
                message = {"message_type": "player_join", "player_name": player_name}
                self.ws.send(json.dumps(message))
                self.player_name = player_name
                self.game_state = GameState.GameBoard

            elif self.game_state == GameState.GameBoard:
                self.setupGameboard()
                # self.testGrid()
                self.placeCharacters()

                pass
            elif self.game_state == GameState.PlayerTurn:
                while True:
                    message = {}
                    move_type = input("User, enter 'move' to move, 'accuse' to accuse', or 'claim' to claim\n")
                    if move_type == "move":
                        x = input("Enter x coordinate: \n")
                        y = input("Enter y coordinate: \n")
                        message = {"message_type": "player_move", "x_coord": x, "y_coord": y}
                        break
                    elif move_type == "accuse":
                        message = {"message_type": "skip_to_accuse"}
                        break
                    elif move_type == 'claim':
                        message["message_type"] = "make_claim"
                        message["character"] = input("Enter character name to claim: \n")
                        message["weapon"] = input("Enter with what weapon: \n")
                        message["room"] = input("Enter in what room: \n")
                        break
                    else:
                        print("Invalid move!")

                self.ws.send(json.dumps(message))

            elif self.game_state == GameState.PlayerWin:
                pass
            elif self.game_state == GameState.PlayerLoss:
                pass
            else:
                print("ERROR: unknown game state")

            # DEBUG RENDER GAME STATE
            # text_surface = self.font.render(curr_game_data, True, (0, 255, 255))
            # self.screen.blit(text_surface, (0, 0))
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

    def __quit(self):
        pygame.quit()
        self.ws.close()
