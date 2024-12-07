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

from Gameboard import spawnLocations, charColors, customGrid, xScale, yScale, rooms, possible_moves, cardPositions, \
    cardPos, roomLocations

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
        self.foo = False

        self.start_screen_img = pygame.image.load("assets/textures/Start.jpg")
        self.start_screen = self.start_screen_img.get_rect()
        self.start_screen.center = self.screen.get_rect().center

        self.lobby_screen_img = pygame.image.load("assets/textures/Lobby.png")
        self.lobby_screen = self.lobby_screen_img.get_rect()
        self.lobby_screen.center = self.screen.get_rect().center

        self.game_board_img = pygame.image.load("assets/textures/Map2.png")
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

            # This needs to change everytime we change states
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

            player = next(player for player in self.game_data["players"] if player["name"] == self.player_name)
            x = int(player["position"]["x"])
            y = (int(player["position"]["y"]) - 1) % 7

            for move in possible_moves:
                if move[0] == xScale[x].value and move[1] == yScale[y].value:
                    message = {"message_type": "player_move", "x_coord": x, "y_coord": y,
                               "player_name": self.player_name}
                    self.ws.send(json.dumps(message))
                    self.ui_current_updater = self.ui_spare_ui.get_updater()
                    print("MOVING TO GAME BOARD")
                    self.check_player_location((x, y))
                    self.game_state = GameState.GameBoard

        self.up_button.at_unclick = up_button_unclick

        self.down_button = tp.Button("Press to move Down")
        self.down_button.center_on(self.screen)

        def down_button_unclick():
            print("Down Button clicked!")

            player = next(player for player in self.game_data["players"] if player["name"] == self.player_name)
            x = int(player["position"]["x"])
            y = (int(player["position"]["y"]) + 1) % 7

            for move in possible_moves:
                if move[0] == xScale[x].value and move[1] == yScale[y].value:
                    message = {"message_type": "player_move", "x_coord": x, "y_coord": y,
                               "player_name": self.player_name}
                    self.ws.send(json.dumps(message))
                    self.ui_current_updater = self.ui_spare_ui.get_updater()
                    print("MOVING TO GAME BOARD")
                    self.check_player_location((x, y))
                    self.game_state = GameState.GameBoard

        self.down_button.at_unclick = down_button_unclick

        self.left_button = tp.Button("Press to move Left")
        self.left_button.center_on(self.screen)

        def left_button_unclick():
            print("Left Button clicked!")

            player = next(player for player in self.game_data["players"] if player["name"] == self.player_name)
            x = (int(player["position"]["x"]) - 1) % 7
            y = int(player["position"]["y"])

            for move in possible_moves:
                if move[0] == xScale[x].value and move[1] == yScale[y].value:
                    message = {"message_type": "player_move", "x_coord": x, "y_coord": y,
                               "player_name": self.player_name}
                    self.ws.send(json.dumps(message))
                    self.ui_current_updater = self.ui_spare_ui.get_updater()
                    print("MOVING TO GAME BOARD")
                    self.check_player_location((x, y))
                    self.game_state = GameState.GameBoard

        self.left_button.at_unclick = left_button_unclick

        self.right_button = tp.Button("Press to move Right")
        self.right_button.center_on(self.screen)

        def right_button_unclick():
            print("Right Button clicked!")

            player = next(player for player in self.game_data["players"] if player["name"] == self.player_name)
            x = (int(player["position"]["x"]) + 1) % 7
            y = int(player["position"]["y"])

            for move in possible_moves:
                if move[0] == xScale[x].value and move[1] == yScale[y].value:
                    message = {"message_type": "player_move", "x_coord": x, "y_coord": y,
                               "player_name": self.player_name}
                    self.ws.send(json.dumps(message))
                    self.ui_current_updater = self.ui_spare_ui.get_updater()
                    print("MOVING TO GAME BOARD")
                    self.check_player_location((x, y))
                    self.game_state = GameState.GameBoard

        self.right_button.at_unclick = right_button_unclick

        self.down_right_button = tp.Button("Press to move to Kitchen")
        self.down_right_button.center_on(self.screen)

        def down_right_button_unclick():
            print("Down Right Button clicked!")
            player = next(player for player in self.game_data["players"] if player["name"] == self.player_name)
            x = (int(player["position"]["x"]) + 4) % 7
            y = (int(player["position"]["y"]) + 4) % 7

            for move in possible_moves:
                if move[0] == xScale[x].value and move[1] == yScale[y].value:
                    message = {"message_type": "player_move", "x_coord": x, "y_coord": y,
                               "player_name": self.player_name}
                    self.ws.send(json.dumps(message))
                    self.ui_current_updater = self.ui_spare_ui.get_updater()
                    print("MOVING TO GAME BOARD")
                    self.check_player_location((x, y))
                    self.game_state = GameState.GameBoard

        self.down_right_button.at_unclick = down_right_button_unclick

        self.up_right_button = tp.Button("Press to move to Lounge")
        self.up_right_button.center_on(self.screen)

        def up_right_button_unclick():
            print("Up Right Button clicked!")
            player = next(player for player in self.game_data["players"] if player["name"] == self.player_name)
            x = (int(player["position"]["x"]) + 4) % 7
            y = (int(player["position"]["y"]) - 4) % 7

            for move in possible_moves:
                if move[0] == xScale[x].value and move[1] == yScale[y].value:
                    message = {"message_type": "player_move", "x_coord": x, "y_coord": y,
                               "player_name": self.player_name}
                    self.ws.send(json.dumps(message))
                    self.ui_current_updater = self.ui_spare_ui.get_updater()
                    print("MOVING TO GAME BOARD")
                    self.check_player_location((x, y))
                    self.game_state = GameState.GameBoard

        self.up_right_button.at_unclick = up_right_button_unclick

        self.up_left_button = tp.Button("Press to move to Study")
        self.up_left_button.center_on(self.screen)

        def up_left_button_unclick():
            print("Up Left Button clicked!")
            player = next(player for player in self.game_data["players"] if player["name"] == self.player_name)
            x = (int(player["position"]["x"]) - 4) % 7
            y = (int(player["position"]["y"]) - 4) % 7

            for move in possible_moves:
                if move[0] == xScale[x].value and move[1] == yScale[y].value:
                    message = {"message_type": "player_move", "x_coord": x, "y_coord": y,
                               "player_name": self.player_name}
                    self.ws.send(json.dumps(message))
                    self.ui_current_updater = self.ui_spare_ui.get_updater()
                    print("MOVING TO GAME BOARD")
                    self.check_player_location((x, y))
                    self.game_state = GameState.GameBoard

        self.up_left_button.at_unclick = up_left_button_unclick

        self.down_left_button = tp.Button("Press to move to Conservatory")
        self.down_left_button.center_on(self.screen)

        def down_left_button_unclick():
            print("Down Left Button clicked!")
            player = next(player for player in self.game_data["players"] if player["name"] == self.player_name)
            x = (int(player["position"]["x"]) - 4) % 7
            y = (int(player["position"]["y"]) + 4) % 7

            for move in possible_moves:
                if move[0] == xScale[x].value and move[1] == yScale[y].value:
                    message = {"message_type": "player_move", "x_coord": x, "y_coord": y,
                               "player_name": self.player_name}
                    self.ws.send(json.dumps(message))
                    self.ui_current_updater = self.ui_spare_ui.get_updater()
                    print("MOVING TO GAME BOARD")
                    self.check_player_location((x, y))
                    self.game_state = GameState.GameBoard

        self.down_left_button.at_unclick = down_left_button_unclick

        self.suggest_button = tp.Button("Press to suggest")
        self.suggest_button.center_on(self.screen)

        self.suggest_character = tp.TextInput("", placeholder="Suggest Character")
        self.suggest_weapon = tp.TextInput("", placeholder="Suggest Weapon")
        self.suggest_room = tp.TextInput("", placeholder="Suggest Room")

        def suggest_button_unclick():
            print("Suggestion button clicked!")

            character = self.suggest_character.value
            weapon = self.suggest_weapon.value
            room = self.suggest_room.value

            # need to check if suggestion is valid
            message = {"message_type": "make_claim", "player_name": self.player_name, "is_accused": False, "character": character, "weapon": weapon,
                       "room": room}
            self.ws.send(json.dumps(message))
            self.ui_current_updater = self.ui_spare_ui.get_updater()
            print("MOVING TO GAME BOARD")
            self.game_state = GameState.GameBoard

        self.suggest_button.at_unclick = suggest_button_unclick

        self.down_right_button.set_invisible(True)
        self.up_right_button.set_invisible(True)
        self.up_left_button.set_invisible(True)
        self.down_left_button.set_invisible(True)
        self.suggest_character.set_invisible(True)
        self.suggest_weapon.set_invisible(True)
        self.suggest_room.set_invisible(True)
        self.suggest_button.set_invisible(True)

        self.player_turn = []
        self.player_turn.append(self.up_button)
        self.player_turn.append(self.down_button)
        self.player_turn.append(self.left_button)
        self.player_turn.append(self.right_button)
        self.player_turn.append(self.down_right_button)
        self.player_turn.append(self.up_right_button)
        self.player_turn.append(self.up_left_button)
        self.player_turn.append(self.down_left_button)
        self.player_turn.append(self.suggest_character)
        self.player_turn.append(self.suggest_weapon)
        self.player_turn.append(self.suggest_room)
        self.player_turn.append(self.suggest_button)

        self.ui_player_turn = tp.Group(self.player_turn)
        self.ui_player_turn.set_center(175, SCREEN_HEIGHT / 2)

        self.spare_ui = []
        self.ui_spare_ui = tp.Group(self.spare_ui)

        self.ui_current_updater = self.ui_player_name_input_updater

    def drawGameStart(self):
        self.screen.blit(self.start_screen_img, self.start_screen)

        welcome_message = self.font.render("Welcome to Blues Clue-less", True, WHITE)
        self.screen.blit(welcome_message, ((SCREEN_WIDTH / 2) - 200, 20))

        name_prompt = self.font.render("Please type your name to start:", True, WHITE)
        self.screen.blit(name_prompt, ((SCREEN_WIDTH / 2) - 200, 120))

        # DEBUG RENDER GAME STATE
        player_name = self.font.render(self.player_name, True, BLACK)
        self.screen.blit(player_name, (12, 5))

    def drawLobby(self):
        self.screen.blit(self.lobby_screen_img, self.lobby_screen)

        welcome_message = self.font.render("You are now in the Lobby", True, WHITE)
        self.screen.blit(welcome_message, ((SCREEN_WIDTH / 2) - 200, 20))

        welcome_message = self.font.render("Your name is:", True, WHITE)
        self.screen.blit(welcome_message, ((SCREEN_WIDTH / 2) - 200, 120))

        # DEBUG RENDER GAME STATE
        player_name = self.font.render(self.player_name, True, WHITE)
        self.screen.blit(player_name, ((SCREEN_WIDTH / 2) + 50, 120))

        welcome_message = self.font.render("IN LOBBY WAITING, PLAYER COUNT: ", True, WHITE)
        self.screen.blit(welcome_message, ((SCREEN_WIDTH / 2 - 400), 575))

        player_count = str(len(self.game_data["players"]))
        player_count_temp = self.font.render(player_count, True, WHITE)
        self.screen.blit(player_count_temp, ((SCREEN_WIDTH / 2 + 300), 575))

        if self.is_ready_button_shown == False:
            self.is_ready_button_shown = True

    def setupGameboard(self):
        self.screen.blit(self.game_board_img, self.game_board)

        # DEBUG RENDER GAME STATE
        player_name_text = self.font.render("Player Name: ", True, BLACK)
        self.screen.blit(player_name_text, (15, 0))
        player_name = self.font.render((self.player_name), True, BLACK)
        self.screen.blit(player_name, (220, 0))

        your_cards = self.font.render("Your Cards:", True, BLACK)
        self.screen.blit(your_cards, (1050, 40))

        title = self.font.render("Blues Clue-less!", True, BLACK)
        self.screen.blit(title, (580, 0))

        self.placeCards()
        self.placeAvatar()

    def drawCard(self, card, pos):
        x = pos[0]
        y = pos[1]
        # does the card contain a character card, else skip
        if ('character_card' in card):
            if card['character_card'] == "Miss Scarlett":
                self.screen.blit(self.scarlett_card_img, (x, y))
            elif card['character_card'] == "Colonel Mustard":
                self.screen.blit(self.mustard_card_img, (x, y))
            elif card['character_card'] == "Professor Plum":
                self.screen.blit(self.plum_card_img, (x, y))
            elif card['character_card'] == "Mrs. Peacock":
                self.screen.blit(self.peacock_card_img, (x, y))
            elif card['character_card'] == "Reverend Green":
                self.screen.blit(self.green_card_img, (x, y))
            elif card['character_card'] == "Mrs. White":
                self.screen.blit(self.white_card_img, (x, y))
        elif ('room_card' in card):
            if card['room_card'] == "Study":
                self.screen.blit(self.study_card_img, (x, y))
            elif card['room_card'] == "Hall":
                self.screen.blit(self.hall_card_img, (x, y))
            elif card['room_card'] == "Lounge":
                self.screen.blit(self.lounge_card_img, (x, y))
            elif card['room_card'] == "Library":
                self.screen.blit(self.library_card_img, (x, y))
            elif card['room_card'] == "Billiard Room":
                self.screen.blit(self.billard_card_img, (x, y))
            elif card['room_card'] == "Dining Room":
                self.screen.blit(self.dining_card_img, (x, y))
            elif card['room_card'] == "Conservatory":
                self.screen.blit(self.conservatory_card_img, (x, y))
            elif card['room_card'] == "Ballroom":
                self.screen.blit(self.ballroom_card_img, (x, y))
            elif card['room_card'] == "Kitchen":
                self.screen.blit(self.kitchen_card_img, (x, y))

        elif ('weapon_card' in card):
            if card['weapon_card'] == "Candlestick":
                self.screen.blit(self.candle_card_img, (x, y))
            elif card['weapon_card'] == "Dagger":
                self.screen.blit(self.knife_card_img, (x, y))
            elif card['weapon_card'] == "Lead Pipe":
                self.screen.blit(self.pipe_card_img, (x, y))
            elif card['weapon_card'] == "Revolver":
                self.screen.blit(self.revolver_card_img, (x, y))
            elif card['weapon_card'] == "Rope":
                self.screen.blit(self.rope_card_img, (x, y))
            elif card['weapon_card'] == "Wrench":
                self.screen.blit(self.wrench_card_img, (x, y))

    def placeCards(self):
        # This function is meant to place all of the cards that the user has on hand on top of the game board image

        # init an array of cards, this will soon be the cards array in the json packet for the player associated with this client
        self.cards = []

        # scan through all the players in the the game
        for player in self.game_data["players"]:
            name = player["name"]
            # if the name of the player associated with this client matches the json packet at that instance extract the list of cards
            if name == self.player_name:
                self.cards = player["cards"]
                count = 0

                for card in self.cards:

                    # print("Count: ",count)
                    if (self.foo == False):
                        print(card)
                    self.drawCard(card, cardPos[count])
                    if (count == 5):
                        self.foo = True
                    count = count + 1

    def placeAvatar(self):
        title = self.font.render("Your Character:", True, BLACK)
        self.screen.blit(title, (60, 470))
        avatarX = 120
        avatarY = 510

        for player in self.game_data["players"]:
            name = player["name"]
            # if the name of the player associated with this client matches the json packet at that instance extract the list of cards
            if name == self.player_name:
                avatar = player["character"]
                avatarName = self.font.render(avatar, True, BLACK)
                self.screen.blit(avatarName, (60, 650))
                if avatar == "Miss Scarlett":
                    self.screen.blit(self.scarlett_card_img, (avatarX, avatarY))
                elif avatar == "Colonel Mustard":
                    self.screen.blit(self.mustard_card_img, (avatarX, avatarY))
                elif avatar == "Professor Plum":
                    self.screen.blit(self.plum_card_img, (avatarX, avatarY))
                elif avatar == "Mrs. Peacock":
                    self.screen.blit(self.peacock_card_img, (avatarX, avatarY))
                elif avatar == "Reverend Green":
                    self.screen.blit(self.green_card_img, (avatarX, avatarY))
                elif avatar == "Mrs. White":
                    self.screen.blit(self.white_card_img, (avatarX, avatarY))

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
                                   (xScale[x].value, yScale[y].value), CIRCLE_R, 0)
            elif player["character"] == "Miss Scarlett":
                pygame.draw.circle(self.screen, charColors.SCARLET.value,
                                   (xScale[x].value, yScale[y].value), CIRCLE_R, 0)
            elif player["character"] == "Professor Plum":
                pygame.draw.circle(self.screen, charColors.PLUM.value,
                                   (xScale[x].value, yScale[y].value), CIRCLE_R, 0)
            elif player["character"] == "Mrs. Peacock":
                pygame.draw.circle(self.screen, charColors.PEACOCK.value,
                                   (xScale[x].value, yScale[y].value), CIRCLE_R, 0)
            elif player["character"] == "Reverend Green":
                pygame.draw.circle(self.screen, charColors.GREEN.value,
                                   (xScale[x].value, yScale[y].value), CIRCLE_R, 0)
            elif player["character"] == "Mrs. White":
                pygame.draw.circle(self.screen, charColors.WHITE.value,
                                   (xScale[x].value, yScale[y].value), CIRCLE_R, 0)

    def check_player_location(self, coords):
        # check if player is in room and update turn possibilites
        self.suggest_character.set_invisible(True)
        self.suggest_weapon.set_invisible(True)
        self.suggest_room.set_invisible(True)
        self.suggest_button.set_invisible(True)
        self.down_right_button.set_invisible(True)
        self.up_right_button.set_invisible(True)
        self.up_left_button.set_invisible(True)
        self.down_left_button.set_invisible(True)

        for room in rooms:
            # print(
            #     f"room_coords: {(room.value[0], room.value[1])}, "
            #     f" player_coords: {(xScale[x].value, yScale[y].value)}")

            if (room.value[0] == xScale[coords[0]].value) and (room.value[1] == yScale[coords[1]].value):
                self.suggest_character.set_invisible(False)
                self.suggest_weapon.set_invisible(False)
                self.suggest_room.set_invisible(False)
                self.suggest_button.set_invisible(False)

                # Check if you're in a room with possible diagnol moves
                if room.value[0] == roomLocations.STUDY.value[0] and room.value[1] == roomLocations.STUDY.value[
                    1]:
                    self.down_right_button.set_invisible(False)
                elif room.value[0] == roomLocations.CONSERVATORY.value[0] and room.value[1] == \
                        roomLocations.CONSERVATORY.value[1]:
                    self.up_right_button.set_invisible(False)
                elif room.value[0] == roomLocations.KITCHEN.value[0] and room.value[1] == \
                        roomLocations.KITCHEN.value[1]:
                    self.up_left_button.set_invisible(False)
                elif room.value[0] == roomLocations.LOUNGE.value[0] and room.value[1] == \
                        roomLocations.LOUNGE.value[1]:
                    self.down_left_button.set_invisible(False)

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
                # if self.game_data["player_turn"] == self.player_name:
                self.game_state = GameState.PlayerTurn
                self.ui_current_updater = self.ui_player_turn.get_updater()

                # pass
            elif self.game_state == GameState.PlayerTurn:
                self.updateGameboard()





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
