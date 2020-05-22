#imports
import pygame
#set flags
SETUP_WALLS = 0
SET_POINTS = 1
DISPLAY_INFO = 2
#color flags
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

#class for creating buttons
class buttonSetup():
    #constructor
    def __init__(self, display, buttonType):
        self.screen = display.screen
        self.pixels = display.screenSize
        self.buttonType = buttonType

        self.wallRect = None
        self.pointRect = None
        self.infoRect = None
        self.infotextRect = None
        self.failtextRect = None

    #drawing method
    def drawButton(self):
        #Drawing the clear board button
        if (self.buttonType == SETUP_WALLS):
            image = pygame.image.load('png/Wallbutton.png').convert()
            self.wallRect = image.get_rect()
            self.wallRect.center = (self.pixels[0]//3, self.pixels[1])
            self.screen.blit(image, self.wallRect)
        #drawing the set points button
        elif (self.buttonType == SET_POINTS):
            image = pygame.image.load('png/Pointbutton.png').convert()
            self.pointRect = image.get_rect()
            self.pointRect.center = (((self.pixels[0]-self.pixels[0]//3), self.pixels[1]))
            self.screen.blit(image, self.pointRect)
        #drawing the info button
        elif (self.buttonType == DISPLAY_INFO):
            image = pygame.image.load('png/infobutton.png').convert()
            self.infoRect = image.get_rect()
            self.infoRect.center = ((25, self.pixels[1]+5))
            self.screen.blit(image, self.infoRect)

    #loading up directions for point setting
    def pointClicked(self):
        image = pygame.image.load('png/box.png').convert()
        self.inRect = image.get_rect()
        self.inRect.center = (self.pixels[0]//2, self.pixels[1]//2)
        self.screen.blit(image, self.inRect)

    #loading up the information box
    def infoClicked(self):
        image = pygame.image.load('png/info.png').convert()
        self.infotextRect = image.get_rect()
        self.infotextRect.center = (self.pixels[0]//2, self.pixels[1]//2)
        self.screen.blit(image, self.infotextRect)

    #drawing fail message info box for impossible paths
    def failedMessage(self):
        image = pygame.image.load('png/fail_message.png').convert()
        self.failtextRect = image.get_rect()
        self.failtextRect.center = (self.pixels[0]//2, self.pixels[1]//2)
        self.screen.blit(image, self.failtextRect)
