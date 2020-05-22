import numpy as np
import heapq

class aStarAlgorithmSolver():
    def __init__(self, board, display):
        self.board = board
        self.dis = display
        self.checkedPoints = []

    def heuristicCalculator(self, x, y):
        return np.sqrt((y[0]-x[0]) ** 2 + (y[1]-x[1]) ** 2)

    # A* search
    def astar_search(self, board, start, goal):
        #neighbors to check with each iteration (no diagonals allowed)
        neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
        #sets
        closed = set()
        came_from = {}
        #scores
        gscore = {start:0}
        fscore = {start:self.heuristicCalculator(start, goal)}
        #push first onto queue
        holder = []
        heapq.heappush(holder, (fscore[start], start))

        #algorithm loop
        while len(holder) > 0:
            currPoint = heapq.heappop(holder)[1]
            if currPoint == goal:
                path = []
                while currPoint in came_from:
                    path.append(currPoint)
                    currPoint = came_from[currPoint]
                return path
            
            closed.add(currPoint)
            
            for i, j in neighbors:
                neighbor = currPoint[0] + i, currPoint[1] + j            
                gscore_x = gscore[currPoint] + self.heuristicCalculator(currPoint, neighbor)
                #border checking
                if 0 <= neighbor[0] and neighbor[0] < 29:
                    if 0 <= neighbor[1] and neighbor[1] < 29:                
                        if board[neighbor[1]][neighbor[0]] == 1:
                            continue
                    else:
                        continue
                else:
                    continue
                if neighbor in closed and gscore_x >= gscore.get(neighbor, 0):
                    continue
                if  gscore_x < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in holder]:
                    came_from[neighbor] = currPoint
                    gscore[neighbor] = gscore_x
                    fscore[neighbor] = gscore_x + self.heuristicCalculator(neighbor, goal)
                    heapq.heappush(holder, (fscore[neighbor], neighbor))


    def markPath(self, point):
        self.board[point[1]][point[0]] = 3

    def checkDist(self, p1, p2):
        initialYDist = p2[y]-p1[y]
        initialXDist = p2[x]-p1[x]
        return math.sqrt((initialYDist ** 2)+(initialXDist**2))

    def getBoard(self):
        return self.board
