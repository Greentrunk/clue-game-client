"""
GUI Module

This module contains the GameState class

Author: Christopher Pohl
Date: 2024-10-21
"""

from enum import Enum
import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#This will break up the coordinates on the gameboard into digestable locations
class Grid:
    def __init__(self, rows, cols, square_size, screen):
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.screen = screen

    def draw_circles(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.square_size + self.square_size // 2
                y = row * self.square_size + self.square_size // 2
                print("X: ", x)
                print("Y: ", y)
                print(" self.square_size // 4: ",  self.square_size // 4)
                pygame.draw.circle(self.screen, BLACK, (x, y), self.square_size // 4)


    def draw_grid_lines(self):
        for row in range(self.rows + 1):
            pygame.draw.line(self.screen, BLACK, (0, row * self.square_size), (self.cols * self.square_size, row * self.square_size))
        for col in range(self.cols + 1):
            pygame.draw.line(self.screen, BLACK, (col * self.square_size, 0), (col * self.square_size, self.rows * self.square_size))


class cardPositions (Enum):
    x0 = 1030
    x1 = 1140

    y0 = 108
    y1 = 288
    y2 = 468

cardPos = [(cardPositions.x1.value,cardPositions.y0.value),
           (cardPositions.x1.value,cardPositions.y1.value),
           (cardPositions.x1.value,cardPositions.y2.value),
           (cardPositions.x0.value,cardPositions.y0.value),
           (cardPositions.x0.value,cardPositions.y1.value),
           (cardPositions.x0.value,cardPositions.y2.value)]

class customGrid (Enum):
    x0 = 420
    x1 = 515
    x2 = 600
    x3 = 680
    x4 = 770
    x5 = 850
    x6 = 950

    xScale = [x0, x1, x2, x3, x4, x5, x6]

    y0 = 95
    y1 = 180
    y2 = 265
    y3 = 345
    y4 = 430
    y5 = 510
    y6 = 595

    yScale = [y0, y1, y2, y3, y4, y5, y6]

xScale = [customGrid.x0, customGrid.x1, customGrid.x2, customGrid.x3, customGrid.x4, customGrid.x5, customGrid.x6]
yScale = [customGrid.y0, customGrid.y1, customGrid.y2, customGrid.y3, customGrid.y4, customGrid.y5, customGrid.y6]
    #
    # xMapStart = 420
    # xincrement = 175
    #
    # x0 = xMapStart
    # x1 = x0 + xincrement
    # x2 = x0 + 2*xincrement
    # x3 = x0 + 3*xincrement
    # x4 = x0 + 4*xincrement
    # x5 = x0 + 5*xincrement
    # x6 = x0 + 6*xincrement
    #
    # yMapStart = 95
    # yincrement = 165
    #
    # y0 = yincrement
    # y1 = y0 + yincrement
    # y2 = y0 + 2*yincrement
    # y3 = y0 + 3*yincrement
    # y4 = y0 + 4*yincrement
    # y5 = y0 + 5*yincrement
    # y6 = y0 + 6*yincrement

class spawnLocations(Enum):
    spawnScarlet = [customGrid.x4.value, customGrid.y0.value]
    spawnMustard = [customGrid.x6.value, customGrid.y2.value]
    spawnPlum = [customGrid.x0.value, customGrid.y2.value]
    spawnPeacock = [customGrid.x0.value, customGrid.y4.value]
    spawnGreen = [customGrid.x2.value, customGrid.y6.value]
    spawnWhite = [customGrid.x4.value, customGrid.y6.value]

class roomLocations(Enum):
    STUDY = [customGrid.x1.value, customGrid.y1.value]
    HALL = [customGrid.x3.value, customGrid.y1.value]
    LOUNGE = [customGrid.x5.value, customGrid.y1.value]
    LIBRARY = [customGrid.x1.value, customGrid.y3.value]
    BILLIARD = [customGrid.x3.value, customGrid.y3.value]
    DINING = [customGrid.x5.value, customGrid.y3.value]
    CONSERVATORY = [customGrid.x1.value, customGrid.y5.value]
    BALLROOM = [customGrid.x3.value, customGrid.y5.value]
    KITCHEN = [customGrid.x5.value, customGrid.y5.value]

class charColors(Enum):
    SCARLET = (255, 0, 0)
    MUSTARD = (255, 255, 30)
    PLUM = (255, 0, 255)
    PEACOCK = (0, 0, 255)
    GREEN = (0, 255, 0)
    WHITE = (230, 230, 200)




