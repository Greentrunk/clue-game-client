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
        self.is_turn_ui_shown = False


        self.start_screen_img = pygame.image.load("assets/textures/Start.jpg")
        self.start_screen = self.start_screen_img.get_rect()
        self.start_screen.center = self.screen.get_rect().center

        self.lobby_screen_img = pygame.image.load("assets/textures/Lobby.png")
        self.lobby_screen = self.lobby_screen_img.get_rect()
        self.lobby_screen.center = self.screen.get_rect().center

        self.game_board_img = pygame.image.load("assets/textures/Map.png")
        self.game_board = self.game_board_img.get_rect()
        self.game_board.center = self.screen.get_rect().center


        self.scarlett_card_img = pygame.image.load("assets/cards/Scarlett.png")
        self.mustard_card_img = pygame.image.load("assets/cards/Mustard.png")
        self.plum_card_img = pygame.image.load("assets/cards/Plum.png")
        self.peacock_card_img = pygame.image.load("assets/cards/Peacock.png")
        self.green_card_img = pygame.image.load("assets/cards/Green.png")
        self.white_card_img = pygame.image.load("assets/cards/White.png")

        self.candle_card_img = pygame.image.load("assets/cards/CandleStick.png")
        self.knife_card_img = pygame.image.load("assets/cards/Knife.png")
        self.pipe_card_img = pygame.image.load("assets/cards/Lead.png")
        self.rope_card_img = pygame.image.load("assets/cards/Rope.png")
        self.revolver_card_img = pygame.image.load("assets/cards/Revolver.png")
        self.wrench_card_img = pygame.image.load("assets/cards/Wrench.png")

        self.dining_card_img = pygame.image.load("assets/cards/Dining.jpg")
        self.hall_card_img = pygame.image.load("assets/cards/Hall.jpg")
        self.kitchen_card_img = pygame.image.load("assets/cards/Kitchen.jpg")
        self.study_card_img = pygame.image.load("assets/cards/Study.jpg")
        self.lounge_card_img = pygame.image.load("assets/cards/Lounge.jpg")
        self.conservatory_card_img = pygame.image.load("assets/cards/Conservatory.jpg")
        self.library_card_img = pygame.image.load("assets/cards/Library.jpg")
        self.billard_card_img = pygame.image.load("assets/cards/Billard.jpg")
        self.ballroom_card_img = pygame.image.load("assets/cards/Ballroom.jpg")

        
        # User Interface object initialization
        tp.init(self.screen, tp.themes.theme_game1)


        # User Interface: Player Name
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


        # User Interface: Lobby Waiting
        self.ready_button = tp.Button("Press to ready up")
        self.ready_button.center_on(self.screen)

        def player_ready_unclick():
            print("Ready Button clicked!")
            # self.is_ready_button_shown = False
            message = {"message_type": "player_ready", "player_name": self.player_name}
            self.ws.send(json.dumps(message))

            self.ui_current_updater = self.ui_lobby_ready.get_updater()
        self.ready_button.at_unclick = player_ready_unclick

        self.lobby_waiting = []
        self.lobby_waiting.append(self.ready_button)
        self.ui_lobby_waiting = tp.Group(self.lobby_waiting)
        self.ui_lobby_waiting_updater = self.ui_lobby_waiting.get_updater()


        # User Interface: Lobby Ready
        self.lobby_ready = []
        self.ui_lobby_ready = tp.Group(self.lobby_ready)


        # User Interface: Player Turn
        self.up_button = tp.Button("Press to move Up")
        self.up_button.center_on(self.screen)

        def up_button_unclick():
            print("Up Button clicked!")
            # self.is_ready_button_shown = False
            message = {"message_type": "player_ready", "player_name": self.player_name}
            self.ws.send(json.dumps(message))

            self.ui_current_updater = self.ui_spare_ui.get_updater()
            print("MOVING TO GAME STATE")
            self.game_state = GameState.GameBoard
        self.up_button.at_unclick = up_button_unclick

        self.player_turn = []
        self.player_turn.append(self.up_button)
        self.ui_player_turn = tp.Group(self.player_turn)


        self.spare_ui = []
        self.ui_spare_ui = tp.Group(self.spare_ui)


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

            self.is_ready_button_shown = True


    def setupGameboard(self):
        self.screen.blit(self.game_board_img, self.game_board)

        # DEBUG RENDER GAME STATE
        player_name = self.font.render(self.player_name, True, BLACK)
        self.screen.blit(player_name, (15, 5))

        self.placeCards()

    def testGrid(self):
        # Create a Grid object
        grid = Grid(7, 7, 95, self.screen)
        grid.draw_circles()
        grid.draw_grid_lines()

    def drawCard(self, card, x, y):
        if card == "Scarlett":
            self.screen.blit(self.scarlett_card_img, (x,y))

    def placeCards(self):
        # This function is meant to place all of the cards that the user has on hand on top of the game board image

        #init an array of cards, this will soon be the cards array in the json packet for the player associated with this client
        self.cards = []

        #scan through all the players in the the game
        for player in self.game_data["players"]:
            name = player["name"]
            # if the name of the player associated with this client matches the json packet at that instance extract the list of cards
            if name == self.player_name:
                self.cards = player["cards"]
                for cards in self.cards:
                    self.drawCard("Scarlett", 30,30)

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

            # RENDER/LOGIC HERE BASED ON GAME STATE
            if self.game_state == GameState.GameStart:
                self.drawGameStart()
                # self.ui_current_updater.update(events=events)
                # Temp for minimal

                # player_name = input("Enter player name: \n")
                # self.game_state = GameState.LobbyWaiting

            elif self.game_state == GameState.LobbyWaiting:
                self.drawLobby()
                # self.ui_current_updater.update(events=events)

                # This awaits for the message that the game has started from the server side. This condition is met only when all players join the lobby and ready up by clicking the UI button
                if self.game_data["game_start"] == "game_started":
                    print("GAME STARTED")
                    self.game_state = GameState.GameBoardInit


            elif self.game_state == GameState.GameBoardInit:
                self.setupGameboard()
                # self.testGrid()
                self.placeCharacters()

                print("GAMEBOARD INIT")
                # Move on to the playerTurn state only if it is the players Turn
                self.game_state = GameState.GameBoard



            elif self.game_state == GameState.GameBoard:
                self.updateGameboard()

                # Check who's turn
                # Move on to the playerTurn state only if it is the players Turn
                if self.game_data["player_turn"] == self.player_name:
                    self.game_state = GameState.PlayerTurn
                    self.ui_current_updater = self.ui_player_turn.get_updater()


                pass
            elif self.game_state == GameState.PlayerTurn:
                if self.is_turn_ui_shown == False:
                    print("Up Button Made")
                    self.is_turn_ui_shown = True
                #
                # if turn is over:
                #     self.ui_current_updater = self.ui_p.get_updater()


                # while True:
                #     message = {}
                #     move_type = input("User, enter 'move' to move, 'accuse' to accuse', or 'claim' to claim\n")
                #     if move_type == "move":
                #         x = input("Enter x coordinate: \n")
                #         y = input("Enter y coordinate: \n")
                #         message = {"message_type": "player_move", "x_coord": x, "y_coord": y,
                #                    "player_name": self.player_name}
                #         break
                #     elif move_type == "accuse":
                #         message = {"message_type": "skip_to_accuse", "player_name": self.player_name}
                #         break
                #     elif move_type == 'claim':
                #         message = {"player_name": self.player_name}
                #         message["message_type"] = "make_claim"
                #         message["character"] = input("Enter character name to claim: \n")
                #         message["weapon"] = input("Enter with what weapon: \n")
                #         message["room"] = input("Enter in what room: \n")
                #         break
                #     else:
                #         print("Invalid move!")
                #
                # self.ws.send(json.dumps(message))
                # self.updateGameboard()

            elif self.game_state == GameState.PlayerWin:
                pass
            elif self.game_state == GameState.PlayerLoss:
                pass
            else:
                print("ERROR: unknown game state")

            self.ui_current_updater.update(events=events)
            pygame.display.flip()
            self.clock.tick(60)  # limits FPS to 60

    def __quit(self):
        pygame.quit()
        self.ws.close()
