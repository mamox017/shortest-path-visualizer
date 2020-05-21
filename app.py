#imports
import time, sys, pygame, math, numpy
from queue import PriorityQueue
#BOARD IS POINT[Y][X]
#Pygame setup
pygame.init()
pygame.display.set_caption("Shortest Path Visualizer, Created by: Mootii Mamo, linkedin.com/in/mootii") 
#set flags
SETUP_WALLS = 0
SET_POINTS = 1
DISPLAY_INFO = 2
#color flags
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
#for clarity
x = 0
y = 1
        
'''class Node():
    def __init__(self, parentNode, pos):
        self.position = pos
        self.parent = parentNode
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, otherNode):
        return self.position == otherNode.position'''

class Grid():
    def __init__(self, row, col):
        #display settings
        self.screen = pygame.display.set_mode((col-30, row+30))
        self.screen.fill((150, 150, 150))
        #size variables
        self.screenSize = (col, row)
        self.row = row//30
        self.col = col//30
        #main board
        self.board = numpy.zeros((self.row-1, self.col-1))
        self.barredPoints = []
        #boardButtons
        self.wallButton = buttonSetup(self, 0)
        self.locButton = buttonSetup(self, 1)
        self.infoButton = buttonSetup(self, 2)
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
        self.board = numpy.zeros((self.row, self.col))
        self.screen.fill((150, 150, 150))

    def sync(self, board):
        self.board = board

class aStarAlgorithmSolver():
    def __init__(self, board, display):
        self.board = board
        self.dis = display
        self.checkedPoints = []


    def algorithm(self, p1, p2):
        if (p1 == p2):
            return
        startNode = Node(p1[x], p1[y], None)

        q = PriorityQueue()
        q.put((0, startNode))
        #for i in range(len(self.board)):
            #for j in range(len(self.board[i])):
                #if(self.board[i][j] not in self.dis.barredPoints):
                    #currNode = Node(j, i, None)
                    #currNode.cost = self.checkDist(p1, (j, i))
                    #q.put((-currNode.cost, currNode))

        while(not q.empty()):
            #gets lowest cost
            p = q.get()
            if(p.coord == p2):
                return
            if (p[x]+1 < 29):
                q.append((p[x]+1, p[y]))
            if (p[x]-1 >= 0):
                q.append((p[x]-1, p[y]))
            if (p[y]+1 < 29):
                q.append((p[x], p[y]+1))
            if (p[y]-1 >= 0):
                q.append((p[x], p[y]-1))


    def recurseSides(self, p1, p2):
        if (p1 == p2):
            return

        testPoints = []
        self.checkedPoints.append(p1)
        if (p1[x]+1 < 29):
            testPoints.append((p1[x]+1, p1[y]))
        if (p1[x]-1 >= 0):
            testPoints.append((p1[x]-1, p1[y]))
        if (p1[y]+1 < 29):
            testPoints.append((p1[x], p1[y]+1))
        if (p1[y]-1 >= 0):
            testPoints.append((p1[x], p1[y]-1))

        mindist = 100
        minIndex = -1
        for i in range(len(testPoints)):
            currPoint = (testPoints[i][x], testPoints[i][y])
            if (mindist > self.checkDist(testPoints[i], p2) and currPoint not in self.dis.barredPoints
                and currPoint not in self.checkedPoints):
                mindist = self.checkDist(testPoints[i], p2)
                minIndex = i
        self.markPath(testPoints[minIndex])
        self.dis.draw(0)
        self.recurseSides(testPoints[minIndex], p2)


    def markPath(self, point):
        #print(str(point))
        self.board[point[1]][point[0]] = 3

    def checkDist(self, p1, p2):
        #for clarity
        x = 0
        y = 1
        
        initialYDist = p2[y]-p1[y]
        initialXDist = p2[x]-p1[x]
        return math.sqrt(math.pow(initialYDist,2)+math.pow(initialXDist,2))

    def getBoard(self):
        return self.board
        


class buttonSetup():
    def __init__(self, display, buttonType):
        self.screen = display.screen
        self.pixels = display.screenSize
        self.buttonType = buttonType

    def drawButton(self):
        #Drawing the clear board button
        if (self.buttonType == SETUP_WALLS):
            image = pygame.image.load('Wallbutton.png').convert()
            self.wallRect = image.get_rect()
            self.wallRect.center = (self.pixels[0]//3, self.pixels[1])
            self.screen.blit(image, self.wallRect)
        #drawing the set points button
        elif (self.buttonType == SET_POINTS):
            image = pygame.image.load('Pointbutton.png').convert()
            self.pointRect = image.get_rect()
            self.pointRect.center = (((self.pixels[0]-self.pixels[0]//3), self.pixels[1]))
            self.screen.blit(image, self.pointRect)
        #drawing the info button
        elif (self.buttonType == DISPLAY_INFO):
            image = pygame.image.load('infobutton.png').convert()
            self.infoRect = image.get_rect()
            self.infoRect.center = ((25, self.pixels[1]+5))
            self.screen.blit(image, self.infoRect)

    #loading up directions for point setting
    def pointClicked(self):
        image = pygame.image.load('box.png').convert()
        self.inRect = image.get_rect()
        self.inRect.center = (self.pixels[0]//2, self.pixels[1]//2)
        self.screen.blit(image, self.inRect)

    #loading up the information box
    def infoClicked(self):
        image = pygame.image.load('info.png').convert()
        self.infotextRect = image.get_rect()
        self.infotextRect.center = (self.pixels[0]//2, self.pixels[1]//2)
        self.screen.blit(image, self.infotextRect)
        


def main():
    #Startup the display
    dis = Grid(900, 900)
    #Conditionals
    notSetupBox = False
    begin = False
    twoPointCounter = 0
    overlay = 0
    #Draw
    dis.draw(overlay)
    twoPointList = []
    
    #Main loop
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                loc = pygame.mouse.get_pos()
                #Clicking Clear Board
                if(dis.wallButton.wallRect.collidepoint(loc)):
                    dis.clear()
                    begin = False
                    notSetupBox = False
                    overlay = 0
                    twoPointCounter = 0
                    dis.barredPoints = []
                    twoPointList = []
                #clicking setup points
                elif(dis.locButton.pointRect.collidepoint(loc)):
                    dis.locButton.pointClicked()
                    begin = True
                    overlay = True
                    notSetupBox = True
                elif(dis.infoButton.infoRect.collidepoint(loc)):
                    dis.infoButton.infoClicked()
                    overlay = True
                elif(overlay and notSetupBox and dis.locButton.inRect.collidepoint(loc)):
                    overlay = False
                    notSetupBox = False
                elif(overlay and not notSetupBox and dis.infoButton.infotextRect.collidepoint(loc)):
                    overlay = False
                    #set up point choosing
                elif(loc[0]//30 < 29 and loc[1]//30 < 29 and not overlay and begin):
                    if (twoPointCounter < 2):
                        twoPointList.append((loc[0]//30, loc[1]//30))
                        #print(str(twoPointList))
                        dis.mark(loc[1]//30, loc[0]//30)
                        twoPointCounter = twoPointCounter + 1
                        if (twoPointCounter == 2):
                            s = aStarAlgorithmSolver(dis.board, dis)
                            s.recurseSides(twoPointList[0], twoPointList[1])
                            #dis.sync(s.getBoard)
                            #print(str(s.checkDist()))
                elif(loc[0]//30 < 29 and loc[1]//30 < 29 and not overlay and not begin):
                    dis.mousedown = True
                    dis.color(loc[1]//30, loc[0]//30)
            elif event.type == pygame.MOUSEBUTTONUP:
                dis.mousedown = False
            elif event.type == pygame.MOUSEMOTION:
                
                if dis.mousedown:
                    col, row = event.pos
                    if(col//30 < len(dis.board[0]) and row//30 < len(dis.board[0])):
                        dis.color(row//30, col//30)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        dis.draw(overlay)
        pygame.display.flip()

main()
