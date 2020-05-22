import numpy as np
import pygame
from buttonsetup import *

#set flags
SETUP_WALLS = 0
SET_POINTS = 1
DISPLAY_INFO = 2
#color flags
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class grid():
    def __init__(self, row, col):
        #display settings
        self.screen = pygame.display.set_mode((col-30, row+30))
        self.screen.fill((150, 150, 150))
        #size variables
        self.screenSize = (col, row)
        self.row = row//30
        self.col = col//30
        #main board
        self.board = np.zeros((self.row-1, self.col-1))
        self.barredPoints = []
        #boardButtons
        self.wallButton = buttonSetup(self, SETUP_WALLS)
        self.locButton = buttonSetup(self, SET_POINTS)
        self.infoButton = buttonSetup(self, DISPLAY_INFO)
        self.mousedown = False

    #instead of drawing all every loop, draw single dots
    def draw(self, overlay):
        if (not overlay):
            self.screen.fill((150, 150, 150))
            for i in range(self.row-1):
                for j in range(self.col-1):
                    rect = pygame.Rect(j*30, i*30, 30, 30)
                    if(self.board[i][j] == 0):
                        pygame.draw.rect(self.screen, BLACK, rect, 1)
                    elif(self.board[i][j] == 1):
                        pygame.draw.rect(self.screen, RED, rect, 0)
                    elif(self.board[i][j] == 2):
                        pygame.draw.rect(self.screen, GREEN, rect, 0)
                    elif(self.board[i][j] == 3):
                        pygame.draw.rect(self.screen, YELLOW, rect, 0)
                    
        self.wallButton.drawButton()
        self.locButton.drawButton()
        self.infoButton.drawButton()
        pygame.display.flip()
                    
    def color(self, row, col):
        self.barredPoints.append((col, row))
        self.board[row][col] = 1

    def mark(self, row, col):
        self.board[row][col] = 2

    def clear(self):
        self.board = np.zeros((self.row, self.col))
        self.screen.fill((150, 150, 150))

    def sync(self, board):
        self.board = board
