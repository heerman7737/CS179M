import csv
import copy
from math import dist
import sys
import time

SHIPGOAL = [9,1]
BUFFERGOAL = [4,24]

class Node:
    def __init__(self, p):
        self.problem = p
        self.heuristic = 0
        self.depth = 0
        self.cost = 0

class container:
    def __init__(self, x, y, w, n):
        self.coord_x = int(x) 
        self.coord_y = int(y)  
        self.weight = int(w)
        self.name = n
        self.seen = False

# grid = copy(data)
# balanceleft = copy(data with only left half)
# findAvailableSpot

# return the distance needed for all tiles move back to the right spot
# def manhattanDistance(puzzle, goal):
#     # r, c are row and column number of a tile for goal state puzzle
#     # row col are row and column number of a tile for current puzzle
#     global r, row, c, col
#     distance = 0

#     # 3 for loops
#     # 1st loops through numbers 1-8
#     # 2nd & 3rd loop through the 3x3 puzzle
#     # to compare how much distances difference between puzzle and GOAL
#     for k in range(1, 9):
#         for i in range(len(puzzle)):
#             for j in range(len(puzzle)):
#                 if puzzle[i][j] == str(k) and puzzle[i][j] != 0:
#                     row = i
#                     col = j
#                 if goal[i][j] == str(k) and goal[i][j] != 0:
#                     r = i
#                     c = j
#         # sum the row and col difference to get the distance
#         distance += abs(r - row) + abs(c - col)

#     return distance


# # This function is from the psuedo-code in slides provided by Prof. Keogh
# def generalSearch(problem):
#     # record the time when generalSearch starts running
#     tstart = time.time()
#     # set the function only to run 1500 seconds
#     t = 1500

#     nodesExpnd = 0  # store number of expanded nodes
#     maxQSize = 0  # keep track of the maximum queue size
#     q = []  # queue
#     visited = []  # store puzzle we've already visited

#     # make the start node with our puzzle
#     n = Node(problem)

#     # put start node into queue
#     q.append(n)
#     maxQSize += 1
#     # put this puzzle into visited list
#     visited.append(n.problem)

#     # loop until problem solved
#     while True:
#         # if queue is empty, failure
#         if len(q) == 0:
#             return 'Failure! !'

#         # set the current node equal to head of queue
#         # currentnode = Node(q[0].problem)
#         # currentnode.heuristic = q[0].heuristic
#         # currentnode.depth = q[0].depth

#         # pop head of queue
#         currentnode = q.pop(0)
#         # nodesExpnd += 1

#         # print which node is the best to expand
#         print("Expanding note with g(n) = ", currentnode.depth,
#               ", h(n) = ", currentnode.heuristic, ": \n")
#         currentnode.printPuzzle()

#         # sort our queue by lowest h(n) + g(n)
#         # reference: https://thepythonguru.com/python-builtin-functions/sorted/
#         q = sorted(q, key=lambda j: j.cost)

#         # check to see if current node is same as our goal state
#         if checkGoal(currentnode.problem):
#             # print all data
#             print("Puzzle solved!!!\n\n" + "Expanded a total of " + str(nodesExpnd) + " nodes.\n" +
#                   "Maximum number of nodes in the queue was " + str(maxQSize) +
#                   ".\nThe solution depth was ", str(currentnode.depth))
#             return 0

#         # expand all possible child nodes of the current node
#         expndChildren = generateChildren(currentnode, visited)

#         for i in expndChildren:
#             # increment number of expended nodes
#             nodesExpnd += 1

#             # set every child node as a temp node
#             tmp = Node(i)

#             # increment depth
#             tmp.depth = currentnode.depth + 1

#             # set heuristic based on algoChoice

#             tmp.heuristic = manhattanDistance(tmp.problem)

#             # sum depth and heuristic for cost
#             tmp.cost = tmp.depth + tmp.heuristic
#             # put temp node into queue
#             q.append(tmp)
#             # put temp node puzzle into visited list
#             visited.append(tmp.problem)

#             # update max queue size
#             if len(q) > maxQSize:
#                 maxQSize = len(q)

#             # Exit the system if exceeded runtime
#             if time.time() > tstart + t:
#                 print('Exceeded runtime..')
#                 sys.exit()


# # return node that is expanded to all possible
# def generateChildren(currentNode, visited):
#     # list to store child nodes
#     childrenNode = []
#     global row, col
#     # find current location of zero
#     for i in range(len(currentNode.problem)):
#         for j in range(len(currentNode.problem)):
#             if int(currentNode.problem[i][j]) == 0:
#                 row = i
#                 col = j
#     # decide where can we move zero to
#     # row not 0, can go up
#     if row != 0:
#         newPuzzle = moveUp(currentNode.problem, row, col)
#         # check if we've visited this puzzle before
#         if newPuzzle not in visited:
#             childrenNode.append(newPuzzle)

#     # row not 2, can go down
#     if row != (len(currentNode.problem) - 1):
#         newPuzzle = moveDown(currentNode.problem, row, col)
#         # check if we've visited this puzzle before
#         if newPuzzle not in visited:
#             childrenNode.append(newPuzzle)

#     # col not 0, can go left
#     if col != 0:
#         newPuzzle = moveLeft(currentNode.problem, row, col)
#         # check if we've visited this puzzle before
#         if newPuzzle not in visited:
#             childrenNode.append(newPuzzle)

#     # col not 2, can go right
#     if col != (len(currentNode.problem) - 1):
#         newPuzzle = moveRight(currentNode.problem, row, col)
#         # check if we've visited this puzzle before
#         if newPuzzle not in visited:
#             childrenNode.append(newPuzzle)

#     return childrenNode


# def checkGoal(puzzle, goal):
#     if puzzle == goal:
#         return True
#     return False


# # return new puzzle that zero has been moved up
# def moveUp(p, row, col):
#     newPuzzle = copy.deepcopy(p)

#     temp = newPuzzle[row][col]
#     newPuzzle[row][col] = newPuzzle[row - 1][col]  # moving up
#     newPuzzle[row - 1][col] = temp  # swapping

#     return newPuzzle


# # return new puzzle that zero has been moved down
# def moveDown(p, row, col):
#     newPuzzle = copy.deepcopy(p)

#     temp = newPuzzle[row][col]
#     newPuzzle[row][col] = newPuzzle[row + 1][col]  # moving up
#     newPuzzle[row + 1][col] = temp  # swapping

#     return newPuzzle


# # return new puzzle that zero has been moved left
# def moveLeft(p, row, col):
#     newPuzzle = copy.deepcopy(p)

#     temp = newPuzzle[row][col]
#     newPuzzle[row][col] = newPuzzle[row][col - 1]  # moving up
#     newPuzzle[row][col - 1] = temp  # swapping

#     return newPuzzle


# # return new puzzle that zero has been moved right
# def moveRight(p, row, col):
#     newPuzzle = copy.deepcopy(p)

#     temp = newPuzzle[row][col]
#     newPuzzle[row][col] = newPuzzle[row][col + 1]  # moving up
#     newPuzzle[row][col + 1] = temp  # swapping

#     return newPuzzle


def offload(todo_off):  # 1
    print('unload all needed containers first')
    for i in range(len(todo_off)):
        print(f'here: {len(todo_off)}')

    moves.append('unload all needed containers first')




def load(todo_on):  # 2
    print('load all new containers')
    moves.append('load all new containers')
    cost = 0
    flag = False
    for i in range(int(len(todo_on))):
        u,weight,name = todo_on[i].split()
        #print(f"todo weight:{weight} name:{name}")
        row, col ,dist = nearspot(8,-1,data) #virtual pink top left
        
        data[row][col].name =name
        data[row][col].weight =weight
    #print('===========ship==================')
    print_ship2()
    #print(moves)

def print_ship2():
    for asd in data[::-1]:
        temp = []
        for y in range (len(asd)):
            temp.append(asd[y].name[0])
        print(temp)
        
        
            
    
def print_ship():
    for x in range(int(len(data))):
        for y in range(int(len(data[0]))):
            print(f'[{data[x][y].coord_x} , {data[x][y].coord_y}] w: {data[x][y].weight} n: {data[x][y].name}')

def task1():
    print('task 1 load offload\n')
    # input format "on/off , x, y"
    todo_off = []
    todo_on = []
    userinput = input("input option as: 1/2 , x, y")  # 1 = off, 2 = on
    #off x y are coord of box need unload
    #on: x is weight, y is name

    while userinput != "confirm":

        if userinput[0] == '1':
            todo_off.append(userinput)
        elif userinput[0] == '2':
            todo_on.append(userinput)

        userinput = input("input option as: 1/2 , x, y")

    print('running offload algorithm... \n')
    offload(todo_off)
    print('running load algorithm... \n')
    #u,weight,name = todo_on[0].split()
    #print(f"todo weight:{weight} name:{name}")
    load(todo_on)


def task2():
    print('task 2 balance\n')
    mid = 6
    total = checkBalance()
    left = total[0]
    right = total[1]

    if abs((left - right))/(left + right) <= 0.1:  # ship is balanced when rate <= 10%
        print('Ship is balanced\n')
        return

    while abs((left - right))/(left + right) > 0.1: # if ship is not balanced ,
                                                    # we always move the container with closest weight to the difference
        if left < right:  # 35     40,50,120;
            diff = right - left  # 175
            closest_weight = 99999 # 40
            tmp = 99999
            for i in range(int(len(data) - 2)):
                for j in range(mid, 12):

                    if abs(data[i][j].weight - diff) < tmp: # 135
                        tmp = abs(data[i][j].weight - diff)
                        closest_weight = data[i][j].weight
                        closest_x = data[i][j].coord_x #1
                        closest_y = data[i][j].coord_y #3

            goal = data[closest_x][mid+1]


def findAvailableSpot(x ,y,grid,current): #find available spot surrounds current spot, and return coord x, y
    
    
    row = x
    col = y
    max_row = int(len(grid))
    max_col = int(len(grid[0]))
    #print(f"data: {grid[0][6].name}\n")
    if(validspot(row,col,grid) and not grid[row][col].seen): #check current is UNUSED and not expanded/visited before
        grid[row][col].seen = True
        return row,col


    
    
    bot_row = row-1 #check bot
    bot_col = col
    if(bot_row<=max_row and bot_col<=max_col and bot_row >=0 and bot_col >=0 and not grid[bot_row][bot_col].seen and col!=current):
        if(validspot(bot_row,bot_col,grid) ): 
            grid[bot_row][bot_col].seen = True
            return bot_row,bot_col
        elif(grid[bot_row][bot_col].name == 'UNUSED') :# spot can't place container but can expand
            return findAvailableSpot(bot_row,bot_col,grid)
    
    left_row = row #check left
    left_col = col-1
    if(left_row<=max_row and left_col<=max_col and left_row >=0 and left_col >=0 and not grid[left_row][left_col].seen):

        if(validspot(left_row,left_col,grid) ): 
            grid[left_row][left_col].seen = True
            return left_row,left_col
        elif(grid[left_row][left_col].name == 'UNUSED') :# spot can't place container but can expand
            return findAvailableSpot(left_row,left_col,grid)
    
    right_row = row #check right
    right_col = col+1
    if(right_row<=max_row and right_col<=max_col and right_row >=0 and right_col >=0 and not grid[right_row][right_col].seen):
        if(validspot(right_row,right_col,grid) ):
            grid[right_row][right_col].seen = True 
            return right_row,right_col
        elif(grid[right_row][right_col].name == 'UNUSED') :# spot can't place container but can expand
            return findAvailableSpot(right_row,right_col,grid)

    top_row = row+1 #check top
    top_col = col
    if(top_row<=max_row and top_col<=max_col and top_row >=0 and top_col >=0 and not grid[top_row][top_col].seen):
        if(validspot(top_row,top_col,grid) ):
            grid[top_row][top_col].seen = True 
            return top_row,top_col
        elif(grid[top_row][top_col].name == 'UNUSED') :# spot can't place container but can expand
            return findAvailableSpot(top_row,top_col,grid)
    return 78,90
   
def checkside(x,y): # already top layer
    if data[x][y].name == 'UNUSED': #if spot is available, return
        return x,y
    else: # check 8 spots around x y 
        radius = 1
        row = x
        col = y
        if data[row][col+radius].name == 'UNUSED' and data[row-radius][col+radius].name !='UNUSED': # right spot is available and not mid air
               
                # return: available_coord_x, available_coord_y, distance
                return row,col+radius
            
        if data[row][col-radius].name == 'UNUSED' and data[row-radius][col+radius].name !='UNUSED': # left corner is available and not mid air
            
            # return: available_coord_x, available_coord_y, distance
            return row,col-radius


def AvailableSpot(x,y,grid):
    spots = []

    for i in range(len(grid[0])): #12
        for j in range(len(grid)): # 8 or 10
            if validspot(j,i,grid) and y !=i: #not check self 
                d = getdistance(x,y,j,i)
                spots.append ([j,i,d])
                break
            else:
                continue
    
    return spots


def getdistance(src_x,src_y,des_x,des_y): #h(n) distance from source to destination, ignore blocks in between
    return abs(src_x-des_x) + abs(src_y-des_y)
   
def nearspot(x,y,grid):  #return the x , y ,dist of nearest aviliable spot
    spots = AvailableSpot(x,y,grid) 
    #for i in range(len(spots)):
        #print(f'lit: {spots[i]}')
    sorted_list = sorted(spots, key=lambda x:x[2])
    #for i in range(len(spots)):
        #print(f'litaa: {spots[i]}')
    #print(f'litaa: {sorted_list[0]}')
    
    return sorted_list[0]



def validspot(row,col,grid): #is available and not mid air
    if grid[row][col].name == 'UNUSED' and grid[row-1][col].name !='UNUSED':
        return True
    if grid[row][col].name == 'UNUSED' and row==0:#is available and already bottom row
        return True

    return False



def checkBalance():

    mid = 6
    total_left = 0
    # if(abs(left-right))
    for i in range(int(len(data)-2)):
        for j in range(mid):
            total_left += data[i][j].weight

    total_right = 0
    for i in range(int(len(data) - 2)):
        for j in range(mid,12):
            total_right += data[i][j].weight

    return total_left, total_right



    # print(total_right, total_left)



def menu():
    choice = int(input("1. Load/offload \n2. Balance\n"))

    if choice == 1:
        # print('task 1 load offload\n')
        task1()


    elif choice == 2:
        # print('task 2 balance\n')
        task2()

    else:
        print('unknown choice, exit')


if __name__ == '__main__':


    ship = []
    # change path below to target manifest location
    path = r"./manifests/CrisDeBurg.txt"
    with open(path, newline='') as csvfile:
        # read manifest and clean useless symbols, store to array of object"container"
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:

            for v in row[0].split():
                x = (row[0].split())[0][1:] 
                y = (row[1].split())[0][:-1]
                weight = (row[2].split())[0][1:6]
                name = (",".join(row[3:]))
                name = name[1:]
                ship.append(container(x, y, weight, name))
                # print(f'cord: ( {x}, {y} ) weight: {weight} name: {name} ')
    # print(f'size: x: {len(ship)} y: {len(ship[0])}')
    # print(ship[95].name)
    # print(f"size: {len(ship)}\n")

    # col = index % 12
    # row = index // 8

    # global var here
    data = []  # 10x12 ship 2d grid
    buffer = []  # 4x24 buffer zone 2d grid
    todo = []  # load/offload todo list
    moves = []  # give instruction to operator to move

    for x in range(8):  # store manifest to ship grid 8x12
        row = []
        for y in range(12):
            row.append(ship[y + (12 * x)])
        data.append(row)

    for x in range(9, 11):  # use ship's row 9,10 as buffer
        row = []
        for y in range(12):
            row.append(container(x, y + 1, 0, "UNUSED"))
        data.append(row)

    for x in range(4):  # use ship's row 9,10 as buffer
        row = []
        for y in range(24):
            row.append(container(x + 1, y + 1, 0, "UNUSED"))
        buffer.append(row)

    print(f'size: x: {len(data)} y: {len(data[0])}')

    # for x in range(int(len(data))):
    #     for y in range(int(len(data[0]))):
    #         print(f'[{data[x][y].coord_x} , {data[x][y].coord_y}] w: {data[x][y].weight} n: {data[x][y].name}')
    print_ship2()
    # d = []
    # indexx=0
    # indexy=6
    # #d =findAvailableSpot(indexx ,indexy,data)
    # spot = nearspot(indexx, indexy,data)
    
    # print(f'cord: {spot[0]},{spot[1]} dist: {spot[2]}')
    # print(f"name: {data[indexx][indexy].name}\n")
    
    # temp =data[indexx][indexy]
    # data[indexx][indexy] = data[d[0]][d[1]]
    # data[d[0]][d[1]] = data[indexx][indexy]
    # print(f'manifest_ cord {d[0]+1}, {d[1]+1} \n')
    
    menu()  # display main menu, input choice

    # for x in range(int(len(data))):
    #     for y in range(int(len(data[0]))):
    #         print(f'[{data[x][y].coord_x} , {data[x][y].coord_y}] w: {data[x][y].weight} n: {data[x][y].name}')