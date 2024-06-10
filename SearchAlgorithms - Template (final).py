import queue
import math

class Node:
    id = None
    up = None
    down = None
    left = None
    right = None
    previousNode = None
    edgeCost = None
    gOfN = 0  # total edge cost
    hOfN = None  # heuristic value
    heuristicFn = None

    def __init__(self, value):
        self.value = value

    def calculateManhattanDistance(self, end):
        return abs(round(self.id[0]) - round(end.id[0])) + abs(round(self.id[1]) - round(end.id[1]))

    def calculateEuclideanDistance(self, node1):
        x1, y1 = self.id
        x2, y2 = node1.id
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def __lt__(self, other):
        # Comparing nodes based on their total cost (gOfN + hOfN)
        return (self.gOfN + self.hOfN) < (other.gOfN + other.hOfN)


class SearchAlgorithms:
    Path = []
    fullPath = []
    totalCost = -1
    maze = []  # The 2D array Maze
    rows = 0  # Number of rows
    columns = 0  # Number of columns
    mazenode = []
    visited = set()  # Add visited set attribute
    cost = []

    def __init__(self, mazeStr, cost=None):
        self.maze = [j.split(',') for j in mazeStr.split(' ')]
        # get number of columns
        for i in mazeStr:
            if i == ',':
                self.columns += 1
            if i == ' ':
                break
        # get number of rows
        for i in mazeStr:
            if i == ' ':
                self.rows += 1
        self.rows = self.rows + 1
        self.columns = self.columns + 1
        self.mazenode = self.createnodes()
        self.fullPath = []
        self.Path = []
        self.visited = set()  # Initialize visited set
        self.cost = cost
        pass

    def createnodes(self):
        mazenode = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                mazenode[i][j] = Node(self.maze[i][j])
                mazenode[i][j].id = (i, j)
                if i + 1 < self.rows:
                    mazenode[i][j].down = (i + 1, j)
                if i - 1 >= 0:
                    mazenode[i][j].up = (i - 1, j)
                if j - 1 >= 0:
                    mazenode[i][j].left = (i, j - 1)
                if j + 1 < self.columns:
                    mazenode[i][j].right = (i, j + 1)
        return mazenode

    def DFS(self):
        rows = self.rows
        columns = self.columns
        currentnode = None
        visited = []
        stack = []
        for i in range(rows):
            for j in range(columns):
                if self.mazenode[i][j].value == 'S':
                    currentnode = self.mazenode[i][j]
                    break
        stack.append(currentnode)
        while currentnode.value != 'E':
            recentnode = stack.pop(0)
            x = recentnode.id[0]
            y = recentnode.id[1]
            self.fullPath.append(self.get_single_index(recentnode.id))
            currentnode = self.mazenode[x][y]
            if currentnode not in stack:
                visited.append(currentnode.id)
            neighbors = [recentnode.right, recentnode.left, recentnode.down, recentnode.up]
            for neighbor in neighbors:
                if (neighbor not in visited and neighbor is not None):
                    neighbor_x = neighbor[0]
                    neighbor_y = neighbor[1]
                    if self.mazenode[neighbor_x][neighbor_y].value != '#':
                        stack.insert(0, self.mazenode[neighbor_x][neighbor_y])
                        self.mazenode[neighbor_x][neighbor_y].previousNode = currentnode
                        visited.append(self.mazenode[neighbor_x][neighbor_y].id)

        self.Path.append(self.get_single_index(recentnode.id))
        while recentnode.value != 'S':
            recentnode = recentnode.previousNode
            self.Path.append(self.get_single_index(recentnode.id))
        self.Path.reverse()
        return self.Path, self.fullPath

    def BFS(self):
        rows = self.rows
        columns = self.columns
        currentnode = Node(1)
        visited = []
        queue = []
        for i in range(rows):
            for j in range(columns):
                if self.mazenode[i][j].value == 'S':
                    currentnode = self.mazenode[i][j]
                    break
        # print(currentnode.value, currentnode.up, currentnode.down, currentnode.left, currentnode.right)
        queue.append(currentnode)
        while currentnode.value != 'E':
            recentnode = queue.pop(0)
            x = recentnode.id[0]
            y = recentnode.id[1]
            currentnode = self.mazenode[x][y]
            neighbors = [recentnode.up, recentnode.down, recentnode.left, recentnode.right]
            for neighbor in neighbors:
                if neighbor not in visited and neighbor is not None:
                    neighbor_x = neighbor[0]
                    neighbor_y = neighbor[1]
                    if self.mazenode[neighbor_x][neighbor_y].value != '#':
                        queue.append(self.mazenode[neighbor_x][neighbor_y])
                        self.mazenode[neighbor_x][neighbor_y].previousNode = currentnode
            if recentnode.id not in visited:
                visited.append(self.mazenode[x][y].id)
                self.fullPath.append(self.get_single_index(recentnode.id))
        self.Path.append(self.get_single_index(recentnode.id))
        while recentnode.value != 'S':
            recentnode = recentnode.previousNode
            self.Path.append(self.get_single_index(recentnode.id))
        self.Path.reverse()
        return self.Path, self.fullPath

    def UCS(self):
        array = []
        currentnode = None
        visited = []
        end = None
        for i in range(self.rows):
            for j in range(self.columns):
                if self.mazenode[i][j].value == 'S':
                    currentnode = self.mazenode[i][j]
                    break
        nodecost = self.cost[self.get_single_index(currentnode.id)]
        currentnode.edgeCost = nodecost
        array.append(currentnode)
        visited.append(currentnode.id)

        while currentnode.value != 'E':
            min = 1000
            for i in array:
                if i.edgeCost < min:
                    min = i.edgeCost
                    currentnode = i
            self.fullPath.append(self.get_single_index(currentnode.id))
            visited.append(currentnode.id)
            self.totalCost = currentnode.edgeCost
            currentnode.edgeCost = 100

            neighbors = [currentnode.up, currentnode.down, currentnode.left, currentnode.right]
            for neighbor in neighbors:
                if neighbor is not None and neighbor not in visited:
                    neighbor_x = neighbor[0]
                    neighbor_y = neighbor[1]
                    if self.mazenode[neighbor_x][neighbor_y].value != '#':
                        nodecost = self.cost[self.get_single_index(neighbor)]
                        self.mazenode[neighbor_x][neighbor_y].edgeCost = nodecost + min
                        self.mazenode[neighbor_x][neighbor_y].previousNode = currentnode
                        array.append(self.mazenode[neighbor_x][neighbor_y])
        self.Path.append(self.get_single_index(currentnode.id))
        while currentnode.value != 'S':
            currentnode = currentnode.previousNode
            self.Path.append(self.get_single_index(currentnode.id))
        self.Path.reverse()
        return self.Path, self.fullPath, self.totalCost

    def AstarEuclideanHeuristic(self):
        openlist = []
        closedlist = []
        currentnode = None
        end = None
        for i in range(self.rows):
            for j in range(self.columns):
                if self.mazenode[i][j].value == 'E':
                    end = self.mazenode[i][j]
                    break
        for i in range(self.rows):
            for j in range(self.columns):
                if self.mazenode[i][j].value == 'S':
                    currentnode = self.mazenode[i][j]
                    break
        currentnode.heuristicFn = currentnode.calculateEuclideanDistance(end)
        currentnode.edgeCost = 0
        openlist.append(currentnode)
        while currentnode.value != 'E':
            openlist = sorted(openlist, key=lambda node: node.heuristicFn)
            currentnode = openlist.pop(0)
            self.fullPath.append(self.get_single_index(currentnode.id))
            closedlist.append(currentnode)
            if currentnode.value == 'E':
                self.Path.append(self.get_single_index(currentnode.id))
                self.totalCost = currentnode.gOfN
                while currentnode.value != 'S':
                    currentnode = currentnode.previousNode
                    self.Path.append(self.get_single_index(currentnode.id))
                self.Path.reverse()
                return self.Path, self.fullPath, self.totalCost
            neighbors = [currentnode.up, currentnode.down, currentnode.left, currentnode.right]
            for neighbor in neighbors:
                if neighbor is not None:
                    n = self.mazenode[neighbor[0]][neighbor[1]]
                    if n not in openlist and n not in closedlist:
                        neighbor_x = neighbor[0]
                        neighbor_y = neighbor[1]
                        if self.mazenode[neighbor_x][neighbor_y].value != '#':
                            nodecost = self.cost[self.get_single_index(neighbor)]
                            neighbor_node = self.mazenode[neighbor_x][neighbor_y]
                            neighbor_node.gOfN = nodecost + currentnode.gOfN
                            neighbor_node.heuristicFn = neighbor_node.gOfN + neighbor_node.calculateEuclideanDistance(end)
                            neighbor_node.previousNode = currentnode
                            openlist.append(self.mazenode[neighbor_x][neighbor_y])
                    elif n in openlist and n not in closedlist:
                        neighbor_x = neighbor[0]
                        neighbor_y = neighbor[1]
                        neighbor_node = self.mazenode[neighbor_x][neighbor_y]
                        if neighbor_node.heuristicFn > neighbor_node.gOfN + currentnode.calculateEuclideanDistance(neighbor_node):
                            neighbor_node.heuristicFn = neighbor_node.gOfN + neighbor_node.calculateEuclideanDistance(end)

        return self.Path, self.fullPath, self.totalCost

    def AstarManhattanHeuristic(self):
        openlist = []
        closedlist = []
        currentnode = None
        end = None
        for i in range(self.rows):
            for j in range(self.columns):
                if self.mazenode[i][j].value == 'E':
                    end = self.mazenode[i][j]
                    break
        for i in range(self.rows):
            for j in range(self.columns):
                if self.mazenode[i][j].value == 'S':
                    currentnode = self.mazenode[i][j]
                    break
        currentnode.heuristicFn = currentnode.calculateManhattanDistance(end)
        currentnode.edgeCost = 0
        openlist.append(currentnode)
        while currentnode.value != 'E':
            openlist = sorted(openlist, key=lambda node: node.heuristicFn)
            currentnode = openlist.pop(0)
            self.fullPath.append(self.get_single_index(currentnode.id))
            closedlist.append(currentnode)
            if currentnode.value == 'E':
                self.Path.append(self.get_single_index(currentnode.id))
                self.totalCost = currentnode.gOfN
                while currentnode.value != 'S':
                    currentnode = currentnode.previousNode
                    self.Path.append(self.get_single_index(currentnode.id))
                self.Path.reverse()
                return self.Path, self.fullPath, self.totalCost
            neighbors = [currentnode.up, currentnode.down, currentnode.left, currentnode.right]
            for neighbor in neighbors:
                if neighbor is not None:
                    n = self.mazenode[neighbor[0]][neighbor[1]]
                    if n not in openlist and n not in closedlist:
                        neighbor_x = neighbor[0]
                        neighbor_y = neighbor[1]
                        if self.mazenode[neighbor_x][neighbor_y].value != '#':
                            nodecost = 1
                            neighbor_node = self.mazenode[neighbor_x][neighbor_y]
                            neighbor_node.gOfN = nodecost + currentnode.gOfN
                            neighbor_node.heuristicFn = neighbor_node.gOfN + neighbor_node.calculateManhattanDistance(end)
                            neighbor_node.previousNode = currentnode
                            openlist.append(self.mazenode[neighbor_x][neighbor_y])
                    elif n in openlist and n not in closedlist:
                        neighbor_x = neighbor[0]
                        neighbor_y = neighbor[1]
                        neighbor_node = self.mazenode[neighbor_x][neighbor_y]
                        if neighbor_node.heuristicFn > neighbor_node.gOfN + currentnode.calculateManhattanDistance(neighbor_node):
                            neighbor_node.heuristicFn = neighbor_node.gOfN + neighbor_node.calculateManhattanDistance(end)

        return self.Path, self.fullPath, self.totalCost

    def get_single_index(self, pos):
        return pos[0] * self.columns + pos[1]

def main():
    s1 = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = s1.BFS()
    print('BFS Path: ' + str(path), end='\nFull Path is: ')
    print(fullPath)

    s2 = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = s2.DFS()
    print('DFS Path: ' + str(path), end='\nFull Path is: ')
    print(fullPath)

    s3 = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.',
                          [0, 15, 2, 100, 60, 35, 30, 3
                              , 100, 2, 15, 60, 100, 30, 2
                              , 100, 2, 2, 2, 40, 30, 2, 2
                              , 100, 100, 3, 15, 30, 100, 2
                              , 100, 0, 2, 100, 30])
    path, fullPath, totalcost = s3.UCS()
    print('UCS Path: ' + str(path), end='\nFull Path is: ')
    print(fullPath)
    print('Total cost: ' + str(totalcost))

    s4 = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.',
                          [0, 15, 2, 100, 60, 35, 30, 3
                              , 100, 2, 15, 60, 100, 30, 2
                              , 100, 2, 2, 2, 40, 30, 2, 2
                              , 100, 100, 3, 15, 30, 100, 2
                              , 100, 0, 2, 100, 30])
    path, fullPath, totalcost = s4.AstarEuclideanHeuristic()
    print('AstarEuclideanHeuristic Path: ' + str(path), end='\nFull Path is: ')
    print(fullPath)
    print('Total cost: ' + str(totalcost))

    s5 = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath, totalcost = s5.AstarManhattanHeuristic()
    print('AstarManhattanHeuristic Path: ' + str(path), end='\nFull Path is: ')
    print(fullPath)
    print('Total cost: ' + str(totalcost))

main()
