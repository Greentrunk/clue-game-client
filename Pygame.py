"""
Pygame Module

This module contains the Pygame class

Author: John Fiorini & Christopher Pohl
Date: 2024-11-10
"""
from xml.etree.ElementTree import tostring

import pygame
import thorpy as tp

from GameState import GameState
from Gameboard import spawnLocations, charColors, customGrid, xScale, yScale
from Gameboard import Grid

import json
import queue

CIRCLE_R = 15
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 1245
SCREEN_HEIGHT = 688

class Pygame:

    def __init__(self, ws, game_data_queue):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.game_state = GameState.GameStart
        self.game_data = {}
        self.game_data_queue = game_data_queue
        self.ws = ws
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.player_name = ""
        self.is_ready_button_shown = False


        self.start_screen_img = pygame.image.load("assets/textures/Start.jpg")
        self.start_screen = self.start_screen_img.get_rect()
        self.start_screen.center = self.screen.get_rect().center

        self.lobby_screen_img = pygame.image.load("assets/textures/Lobby.png")
        self.lobby_screen = self.lobby_screen_img.get_rect()
        self.lobby_screen.center = self.screen.get_rect().center

        self.game_board_img = pygame.image.load("assets/textures/Map.png")
        self.game_board = self.game_board_img.get_rect()
        self.game_board.center = self.screen.get_rect().center

        
        # User Interface object initialization
        tp.init(self.screen, tp.themes.theme_game1)


        # Player Name input UI object
        player_name_input = []
        self.enter_player_name = tp.TextInput("", placeholder="Enter Player Name")
        self.confirm_player_name = tp.Button("Confirm")

        def player_name_unclick():
            player_name = self.enter_player_name.value
            message = {"message_type": "player_join", "player_name": player_name}
            self.ws.send(json.dumps(message))
            self.player_name = player_name
            self.game_state = GameState.LobbyWaiting

            #This needs to change everytime we change states
            self.ui_current_updater = self.ui_lobby_waiting_updater

        self.confirm_player_name.at_unclick = player_name_unclick
        player_name_input.append(self.enter_player_name)
        player_name_input.append(self.confirm_player_name)

        # appending UI group from player_name_input array
        self.ui_player_name_input = tp.Group(player_name_input)
        self.ui_player_name_input_updater = self.ui_player_name_input.get_updater()

        # Lobby Waiting
        self.lobby_waiting = []

        self.ui_lobby_waiting = tp.Group(self.lobby_waiting)
        self.ui_lobby_waiting_updater = self.ui_lobby_waiting.get_updater()

        self.ui_current_updater = self.ui_player_name_input_updater

    def drawGameStart(self):
        self.screen.blit(self.start_screen_img, self.start_screen)

        welcome_message = self.font.render("Welcome to Blues Clue-less", True, WHITE)
        self.screen.blit(welcome_message, ((SCREEN_WIDTH/2) - 200, 20))

        name_prompt = self.font.render("Please type your name to start:", True, WHITE)
        self.screen.blit(name_prompt, ((SCREEN_WIDTH/2) - 200, 120))

        # DEBUG RENDER GAME STATE
        player_name = self.font.render(self.player_name, True, BLACK)
        self.screen.blit(player_name, (12, 5))


    def drawLobby(self):
        print(self.player_name)
        self.screen.blit(self.lobby_screen_img, self.lobby_screen)

        welcome_message = self.font.render("You are now in the Lobby", True, WHITE)
        self.screen.blit(welcome_message, ((SCREEN_WIDTH/2) - 200, 20))

        welcome_message = self.font.render("Your name is:", True, WHITE)
        self.screen.blit(welcome_message, ((SCREEN_WIDTH/2) - 200, 120))

        # DEBUG RENDER GAME STATE
        player_name = self.font.render(self.player_name, True, WHITE)
        self.screen.blit(player_name, ((SCREEN_WIDTH/2) +50, 120))

        welcome_message = self.font.render("IN LOBBY WAITING, PLAYER COUNT: ", True, WHITE)
        self.screen.blit(welcome_message, ((SCREEN_WIDTH/2 - 400), 575))

        player_count = str(len(self.game_data["players"]))
        player_count_temp = self.font.render(player_count, True, WHITE)
        self.screen.blit(player_count_temp, ((SCREEN_WIDTH / 2   + 300), 575))

        if self.is_ready_button_shown == False:
            self.ready_button = tp.Button("Press to ready up")
            self.ready_button.center_on(self.screen)
            self.lobby_waiting.append(self.ready_button)
            self.is_ready_button_shown = True

        def player_ready_unclick():
            print("Button clicked!")
            # self.is_ready_button_shown = False
            message = {"message_type": "player_ready", "player_name": self.player_name}
            self.ws.send(json.dumps(message))
        self.ready_button.at_unclick = player_ready_unclick

        # confirm_player_ready = self.player_ready_unclick()
        # player_name_input.append(self.enter_player_name)
        # player_name_input.append(self.confirm_player_name)
        #
        # button = tp.Button("Standard button")
        # button.set_draggable()  # set the element as draggable to demonstrate also at_drag method
        # button.center_on(self.screen)
        #
        # def my_function_at_unclick():  # dummy function for the test
        #     print("Clicked !")
        #
        # button.at_unclick = my_function_at_unclick  # defining standard 'click' function (though its technically not a click)
        #
        # def my_function_at_drag(dx, dy):  # dummy function for the test ; dx and dy are mandatory !
        #     print("Element dragged:", dx, dy, ("x- and y-axis movement."))
        #
        # button.at_drag = my_function_at_drag  # defining the function to call when we drag the element.
        #
        # def my_function_at_hover(a, b, c):  # dummy function for the test
        #     print("Testing events handling:", a, b, c)
        #
        # button.at_hover = my_function_at_hover  # defining the function to call when we start hovering the element.
        # button.at_hover_params = {"a": "(called at hover)", "b": 12, "c": 15}  # parameters to give at hover
        #
        # # at_unhover, at_cancel and _at_click are also redifinables (though the last one is discouraged - see the doc).
        #
        # def before_gui():  # add here the things to do each frame before blitting gui elements
        #     screen.fill((250,) * 3)
        #
        # tp.call_before_gui(before_gui)  # tells thorpy to call before_gui() before drawing gui.
        #
        # # For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
        # player = button.get_updater().launch()


    def setupGameboard(self):
        self.screen.blit(self.game_board_img, self.game_board)

        # DEBUG RENDER GAME STATE
        player_name = self.font.render(self.player_name, True, BLACK)
        self.screen.blit(player_name, (15, 5))

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

    def updateGameboard(self):
        # Using draw.rect module of
        # pygame to draw the solid circle

        self.setupGameboard()

        # self.screen.blit(self.game_board_img, self.game_board)

        for player in self.game_data["players"]:
            x = player["position"]["x"]
            y = player["position"]["y"]
            # char =
            if player["character"] == "Colonel Mustard":
                pygame.draw.circle(self.screen, charColors.MUSTARD.value,
                                   (xScale[x - 1].value, yScale[y - 1].value), CIRCLE_R, 0)
            elif player["character"] == "Miss Scarlet":
                pygame.draw.circle(self.screen, charColors.SCARLET.value,
                                   (xScale[x - 1].value, yScale[y - 1].value), CIRCLE_R, 0)
            elif player["character"] == "Professor Plum":
                pygame.draw.circle(self.screen, charColors.PLUM.value,
                                   (xScale[x - 1].value, yScale[y - 1].value), CIRCLE_R, 0)
            elif player["character"] == "Mrs. Peacock":
                pygame.draw.circle(self.screen, charColors.PEACOCK.value,
                                   (xScale[x - 1].value, yScale[y - 1].value), CIRCLE_R, 0)
            elif player["character"] == "Reverend Green":
                pygame.draw.circle(self.screen, charColors.GREEN.value,
                                   (xScale[x - 1].value, yScale[y - 1].value), CIRCLE_R, 0)
            elif player["character"] == "Mrs. White":
                pygame.draw.circle(self.screen, charColors.WHITE.value,
                                   (xScale[x - 1].value, yScale[y - 1].value), CIRCLE_R, 0)

    def set_game_data_queue(self, queue):
        self.game_data_queue = queue

    def run(self):
        curr_game_data = {}
        while self.is_running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            events = pygame.event.get()
            for event in events:
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

            self.screen.fill((255, 255, 255))

            # Check who's turn
            if self.game_data["player_turn"] == self.player_name:
                self.game_state = GameState.PlayerTurn

            # RENDER/LOGIC HERE BASED ON GAME STATE
            if self.game_state == GameState.GameStart:
                self.drawGameStart()
                self.ui_current_updater.update(events=events)
                # Temp for minimal

                # player_name = input("Enter player name: \n")
                # self.game_state = GameState.LobbyWaiting

            elif self.game_state == GameState.LobbyWaiting:
                self.drawLobby()
                self.ui_lobby_waiting_updater.update(events=events)

                # To replace with a game start message sent from the server
                print("PRE GAME STARTED")
                if self.game_data["game_start"] == "game_started":
                    print("GAME STARTED")
                    self.game_state = GameState.GameBoardInit


            elif self.game_state == GameState.GameBoardInit:
                self.setupGameboard()
                # self.testGrid()
                self.placeCharacters()
                print("GAMEBOARD INIT")
                self.game_state = GameState.PlayerTurn



            elif self.game_state == GameState.GameBoard:
                self.updateGameboard()
                #
                # self.game_state = GameState.PlayerTurn

                pass
            elif self.game_state == GameState.PlayerTurn:
                while True:
                    message = {}
                    move_type = input("User, enter 'move' to move, 'accuse' to accuse', or 'claim' to claim\n")
                    if move_type == "move":
                        x = input("Enter x coordinate: \n")
                        y = input("Enter y coordinate: \n")
                        message = {"message_type": "player_move", "x_coord": x, "y_coord": y,
                                   "player_name": self.player_name}
                        break
                    elif move_type == "accuse":
                        message = {"message_type": "skip_to_accuse", "player_name": self.player_name}
                        break
                    elif move_type == 'claim':
                        message = {"player_name": self.player_name}
                        message["message_type"] = "make_claim"
                        message["character"] = input("Enter character name to claim: \n")
                        message["weapon"] = input("Enter with what weapon: \n")
                        message["room"] = input("Enter in what room: \n")
                        break
                    else:
                        print("Invalid move!")

                self.ws.send(json.dumps(message))
                print("MOVING TO GAME STATE")
                self.updateGameboard()
                self.game_state = GameState.GameBoard

            elif self.game_state == GameState.PlayerWin:
                pass
            elif self.game_state == GameState.PlayerLoss:
                pass
            else:
                print("ERROR: unknown game state")

            # self.ui_current_updater.update(events=events)
            pygame.display.flip()
            self.clock.tick(60)  # limits FPS to 60

    def __quit(self):
        pygame.quit()
        self.ws.close()
