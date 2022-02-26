from ast import Constant
from cmath import log10
import csv
import copy
from math import dist
import sys
import time
from operator import attrgetter

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
        self.target = False



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

def balance(grid):
    mid = 6
    left, right = checkBalance()
    if abs((left - right))/(left + right) <= 0.1:  # ship is balanced when rate <= 10%
        print('Ship is balanced\n')
        return
    
    else:
        print('Ship is NOT balanced\n')
    myboxes = []
    for row in grid:
        for box in row:
            if(box.name !='UNUSED' and box.name != 'NAN'):
                myboxes.append(box) # append containers to 1d
    arr1,arr2 = partition(myboxes)
    choice = chooseSide(arr1,arr2)

    if choice == 1: # arr1 need go left, arr2 need go right
        goLeft = arr1
        goRight = arr2
    else: # choice == 2
        goLeft = arr2
        goRight = arr1

    goLeft.sort(key=lambda x: x.weight)
    goRight.sort(key=lambda x: x.weight)

    # tLeft =[]
    # tRight =[]
    # for c in goLeft:
    #     tLeft.append(c.weight)
    # for c in goRight:
    #     tRight.append(c.weight)
   

    # print(f'goleft: {tLeft}\ngoright: {tRight}\nchoice: {choice}')

    swapable =True # not move min and still within 10%
    checkLeft = checkRight = True
    while(swapable):

        totalWeightLeft = sumWeight(goLeft)
        totalWeightRight = sumWeight(goRight)
        # print(f'll:{totalWeightLeft} rr: {totalWeightRight}')
        # tLeft =[]
        # tRight =[]
        # for c in goLeft:
        #     tLeft.append(c.weight)
        # for c in goRight:
        #     tRight.append(c.weight)
    

        #print(f'goleft: {tLeft}\ngoright: {tRight}\nchoice: {choice}')
        #print( f'{goLeft[0].weight} max {max(goLeft, key=attrgetter("weight")).weight}')
        if goLeft[0].coord_y > 6 and checkLeft: # if min is in wrong side/ need move
            
            if goLeft[0].weight == max(goLeft, key=attrgetter('weight')).weight:
                checkLeft =False
                break
            minLeft = goLeft[0]
            difference = (abs(totalWeightLeft - totalWeightRight) +(minLeft.weight*2))/(totalWeightLeft + totalWeightRight)
            if  difference < 0.1:# keep min in right/not move to left still in 10%

                goRight.append(goLeft[0])
                goLeft.pop(0)
                goLeft = goLeft[1:] + [goLeft[0]]
                totalWeightLeft = sumWeight(goLeft)
                totalWeightRight = sumWeight(goRight)
                
            else: # min is already in correct side 
                print('no check left')
                checkLeft =False
        else:
            goRight = goRight[1:] + [goRight[0]]


        if goRight[0].coord_y <= 6 and checkRight : # if min is in wrong side/ need move
            if goRight[0].weight == max(goRight, key=attrgetter('weight')).weight:
                checkRight = False
                break

            minRight = goRight[0]
            difference = (abs(totalWeightRight - totalWeightLeft) +(minRight.weight*2))/(totalWeightRight + totalWeightLeft)
            if difference  < 0.1:# keep min in Left/not move to Right still in 10%
                goLeft.append(goRight[0])
                goRight.pop(0)
                goLeft = goLeft[1:] + [goLeft[0]]
                totalWeightLeft = sumWeight(goLeft)
                totalWeightRight = sumWeight(goRight)
            else: # min is already in correct side
                print('no check right')
                checkRight = False
        else:
            goRight = goRight[1:] + [goRight[0]]
            
        if not checkLeft and not checkRight:
            swapable = False

    tempGoLeft = []
    for box in goLeft:
        if box.coord_y > 6: # is in wrong side
            tempGoLeft.append(box)
    tempGoLeft, goLeft = goLeft, tempGoLeft #swap
    tempGoLeft.clear()

    tempGoRight = []
    for box in goRight:
        if box.coord_y <= 6: # is in wrong side
            tempGoRight.append(box)
    tempGoRight, goRight = goRight, tempGoRight #swap
    tempGoRight.clear()


    tLeft =[]
    tRight =[]
    for c in goLeft:
        tLeft.append(c.weight)
    for c in goRight:
        tRight.append(c.weight)
    print(f'goleft: {tLeft}\ngoright: {tRight}\nchoice: {choice}')

    needmove = []
    needmove.append(goLeft)
    needmove.append(goRight)
    moveBoxes(needmove)
        
        
def moveBoxes(arr):

    #while len(arr)>0: # pop after move
    print("need write this ")



def findBox(grid,arr):
    names= []
    names.append(box.name for box in arr)
    for row in grid[::-1]: # top row first
        for box in range (len(row)):
            if box.name in names:
                return box

    

    
def sumWeight(arr):
    total = 0
    for c in arr:
        #if c.coord_y > 6:
        total += c.weight
    return total




def chooseSide(arr1,arr2):
    # arr1 left
    arr1_to_left = 0
    arr1_to_right = 0
    arr2_to_left = 0
    arr2_to_right = 0

    for x in arr1:
        if x.coord_y > 6: # is on right
            arr1_to_left += x.coord_y - 6 # dist to left
        else: # is on left
            arr1_to_right += 6 - x.coord_y # dist to right
    
    for x in arr2:
        if x.coord_y > 6:
            arr2_to_left += x.coord_y - 6
        else:
            arr2_to_right += 6 - x.coord_y

    sol_1_left = arr1_to_left + arr2_to_right
    sol_2_left = arr2_to_left + arr1_to_right
    if sol_1_left<sol_2_left: 
        return 1 # first param need to left, second to right
    else:
        return 2 # second param need to left, first to right
 


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

def markBox(grid,names): # mark target boxes
    for row in grid:# mark target boxes
        for box in row:
            if box.name in names: #name matches todo list
                box.target= True
    return grid

def partition(arr):

    arr = sorted(arr, key=lambda x:x.weight, reverse=True)
    sum1 = 0
    sum2 = 0 
    l1 =[]
    l2 =[]
    for i in range(len(arr)):
        if sum1 <=sum2:
            sum1+=arr[i].weight
            l1.append(arr[i])
        else:
            sum2+=arr[i].weight
            l2.append(arr[i])
    return l1,l2


    

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




def menu():
    choice = int(input("1. Load/offload \n2. Balance\n"))

    if choice == 1:
        # print('task 1 load offload\n')
        task1()


    elif choice == 2:
        # print('task 2 balance\n')
        balance(data)

    else:
        print('unknown choice, exit')


if __name__ == '__main__':


    # #a = [3044,1100,2020,10000,2011,2007,2000]
    # a =[9041,10001,500,600,100,10]
    # n = len(a)
 
    # print(
    #   "2 sets is ", select(a, 0, sum(a)/2))

    ship = []
    # change path below to target manifest location
    path = r"./manifests/ShipCase5.txt"
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
    print(
      "2 sets is ")
    t1, t2 = partition(ship)

    # t1 = 120
    # t2 = 40,50,35
    for x in t1:
        print(f'here: {x.weight}')

    choice = chooseSide(t2,t1)
    print(f'choice: {choice}')
    # for x in range(int(len(data))):
    #     for y in range(int(len(data[0]))):
    #         print(f'[{data[x][y].coord_x} , {data[x][y].coord_y}] w: {data[x][y].weight} n: {data[x][y].name}')
    #print_ship2()
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