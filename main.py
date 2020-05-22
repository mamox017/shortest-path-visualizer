#imports
import time, sys, pygame, math, numpy as np
import heapq
from grid import *
from buttonsetup import *
from algorithm import *

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

def main():
    #Startup the display
    dis = grid(900, 900)
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
        #get events from pygame event queue
        for event in pygame.event.get():
            #if there is a click on the screen, choose from these options
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
                #clicking open info
                elif(dis.infoButton.infoRect.collidepoint(loc)):
                    dis.infoButton.infoClicked()
                    overlay = True
                #clicking on info
                elif(overlay and notSetupBox and dis.locButton.inRect.collidepoint(loc)):
                    overlay = False
                    notSetupBox = False
                #removing messages from screen
                elif(overlay and not notSetupBox):
                    #remove fail message from screen
                    if (dis.locButton.failtextRect):
                        if (dis.locButton.failtextRect.collidepoint(loc)):
                            overlay = False
                    #remove info message from screen
                    elif (dis.infoButton.infotextRect):
                        if (dis.infoButton.infotextRect.collidepoint(loc)):
                            overlay = False
                #if it is time to select the start and end points
                elif(loc[0]//30 < 29 and loc[1]//30 < 29 and not overlay and begin):
                    if (twoPointCounter < 2):
                        twoPointList.append((loc[0]//30, loc[1]//30))
                        #print(str(twoPointList))
                        dis.mark(loc[1]//30, loc[0]//30)
                        twoPointCounter = twoPointCounter + 1
                        if (twoPointCounter == 2):
                            s = aStarAlgorithmSolver(dis.board, dis)
                            path = s.astar_search(dis.board, twoPointList[0], twoPointList[1])
                            
                            if (path == None):
                                print("A* Search Failed!")
                                dis.draw(overlay)
                                dis.locButton.failedMessage()
                                overlay = True
                            else:
                                for i in range(len(path)):
                                    if(i == 0):
                                        dis.mark(path[i][1], path[i][0])
                                    else:
                                        s.markPath(path[i])
                #selecting wall points
                elif(loc[0]//30 < 29 and loc[1]//30 < 29 and not overlay and not begin):
                    dis.mousedown = True
                    dis.color(loc[1]//30, loc[0]//30)
            #letting go of mouse click
            elif event.type == pygame.MOUSEBUTTONUP:
                dis.mousedown = False
            #holding the mouse down
            elif event.type == pygame.MOUSEMOTION:
                if dis.mousedown:
                    col, row = event.pos
                    if(col//30 < len(dis.board[0]) and row//30 < len(dis.board[0])):
                        dis.color(row//30, col//30)
            #clicking the X to exit
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #updating screen
        dis.draw(overlay)
        pygame.display.flip()

main()

