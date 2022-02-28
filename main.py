from ast import Constant
from cmath import log10
import csv
import copy
from glob import escape
from math import dist
import sys
import time
from operator import attrgetter
from tkinter import *
from main import *

# SHIPGOAL = [9,1]
# BUFFERGOAL = [4,24]
MID_LINE = 5


class Node:
    def __init__(self, p):
        self.problem = p
        self.heuristic = 0
        self.depth = 0
        self.cost = 0


class container:
    def __init__(self, x, y, w, n):
        self.rowNum = int(x) - 1  # row
        self.colNum = int(y) - 1  # column
        self.weight = int(w)
        self.name = n
        self.seen = False
        self.target = False


def offload(todo_off):  # 1
    print('unload all needed containers first')
    BoxToOffload = []
    for i in range(len(todo_off)):  # parse input and link box in data
        # print(f'here: {len(todo_off)}')
        option, row, col = todo_off[i].split()
        # print(f'unload todo:{row}, {col}')
        BoxToOffload.append(data[int(row) - 1][int(col) - 1])  # input matches manifest

    while (len(BoxToOffload) > 0):  # pop after unload
        needMove = findBox(data, BoxToOffload)  # find target box near top and stuff on top

        if len(needMove) <= 0:
            print('unload box index <=0')
        mytarget = needMove[len(needMove) - 1]

        for box in needMove:  # box in arr + others on top
            if box.target == True:  # is my target, unload to pink
                box.weight = 0
                box.name = 'UNUSED'
                mysequence.append(f'Offload: [{box.rowNum + 1},{box.colNum + 1} to [9,1](pink)')
            else:  # not target, move to elsewhere
                row, col, dist = nearspot(box.rowNum, box.colNum, data)
                swapData(box.rowNum, box.colNum, row, col, data)
                mysequence.append(f'Move: [{box.rowNum + 1},{box.colNum + 1}] to [{row + 1},{col + 1}]')

        BoxToOffload.remove(mytarget)

    mysequence.append('unload all needed containers first')


def load(todo_on):  # 2
    print('load all new containers')
    mysequence.append('load all new containers')
    cost = 0
    flag = False
    for i in range(int(len(todo_on))):
        u, weight, name = todo_on[i].split()
        # print(f"todo weight:{weight} name:{name}")
        tempgrid = data[:-2]
        row, col, dist = nearspot(8, -1, tempgrid)  # virtual pink top left

        data[row][col].name = name
        data[row][col].weight = weight
        mysequence.append(f'Onload: {name} to [{row + 1},{col + 1}]')

    # print('===========ship==================')
    print_ship2(data)


def print_ship2(grid):
    print(f'============grid {len(grid)} x {len(grid[0])} ==================')
    for asd in grid[::-1]:
        temp = []
        for y in range(len(asd)):
            temp.append(asd[y].name[0])
        print(temp)
    print('\n')


def print_ship():
    for x in range(int(len(data))):
        for y in range(int(len(data[0]))):
            print(f'[{data[x][y].rowNum} , {data[x][y].colNum}] w: {data[x][y].weight} n: {data[x][y].name}')


def task1():
    print('task 1 load offload\n')
    # input format "on/off , x, y"
    todo_off = []
    todo_on = []
    userinput = input("input option as: 1/2 , x, y")  # 1 = off, 2 = on
    # off x y are coord of box need unload
    # on: x is weight, y is name

    while userinput != "confirm":

        if userinput[0] == '1':
            todo_off.append(userinput)
        elif userinput[0] == '2':
            todo_on.append(userinput)

        userinput = input("input option as: 1/2 , x, y")

    print('running offload algorithm... \n')
    offload(todo_off)
    print('running load algorithm... \n')
    # u,weight,name = todo_on[0].split()
    # print(f"todo weight:{weight} name:{name}")
    load(todo_on)


# def task2():
#     print('task 2 balance\n')
#     mid = 6
#     total = checkBalance()
#     left = total[0]
#     right = total[1]

#     if abs((left - right))/(left + right) <= 0.1:  # ship is balanced when rate <= 10%
#         print('Ship is balanced\n')
#         return

#     while abs((left - right))/(left + right) > 0.1: # if ship is not balanced ,
#                                                     # we always move the container with closest weight to the difference
#         if left < right:  # 35     40,50,120;
#             diff = right - left  # 175
#             closest_weight = 99999 # 40
#             tmp = 99999
#             for i in range(int(len(data) - 2)):
#                 for j in range(mid, 12):

#                     if abs(data[i][j].weight - diff) < tmp: # 135
#                         tmp = abs(data[i][j].weight - diff)
#                         closest_weight = data[i][j].weight
#                         closest_x = data[i][j].rowNum #1
#                         closest_y = data[i][j].colNum #3

#             goal = data[closest_x][mid+1]

def balance(grid):
    left, right = checkBalance()
    if abs((left - right)) / (left + right) <= 0.1:  # ship is balanced when rate <= 10%
        print('Ship is balanced\n')
        return

    else:
        print('Ship is NOT balanced\n')
    myboxes = []
    for row in grid:
        for box in row:
            if (box.name != 'UNUSED' and box.name != 'NAN'):
                myboxes.append(box)  # append containers to 1d
    arr1, arr2 = partition(myboxes)
    choice = chooseSide(arr1, arr2)

    if choice == 1:  # arr1 need go left, arr2 need go right
        goLeft = arr1
        goRight = arr2
    else:  # choice == 2
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

    swapable = True  # not move min and still within 10%
    checkLeft = checkRight = True
    while (swapable):

        totalWeightLeft = sumWeight(goLeft)
        totalWeightRight = sumWeight(goRight)
        # print(f'll:{totalWeightLeft} rr: {totalWeightRight}')
        # tLeft =[]
        # tRight =[]
        # for c in goLeft:
        #     tLeft.append(c.weight)
        # for c in goRight:
        #     tRight.append(c.weight)

        # print(f'goleft: {tLeft}\ngoright: {tRight}\nchoice: {choice}')
        # print( f'{goLeft[0].weight} max {max(goLeft, key=attrgetter("weight")).weight}')
        if goLeft[0].colNum > MID_LINE and checkLeft:  # if min is in wrong side/ need move

            if goLeft[0].weight == max(goLeft, key=attrgetter('weight')).weight:
                checkLeft = False
                break
            minLeft = goLeft[0]
            difference = (abs(totalWeightLeft - totalWeightRight) + (minLeft.weight * 2)) / (
                    totalWeightLeft + totalWeightRight)
            if difference < 0.1:  # keep min in right/not move to left still in 10%

                goRight.append(goLeft[0])
                goLeft.pop(0)
                goLeft = goLeft[1:] + [goLeft[0]]
                totalWeightLeft = sumWeight(goLeft)
                totalWeightRight = sumWeight(goRight)

            else:  # min is already in correct side
                print('no check left')
                checkLeft = False
        else:
            goRight = goRight[1:] + [goRight[0]]

        if goRight[0].colNum <= MID_LINE and checkRight:  # if min is in wrong side/ need move
            if goRight[0].weight == max(goRight, key=attrgetter('weight')).weight:
                checkRight = False
                break

            minRight = goRight[0]
            difference = (abs(totalWeightRight - totalWeightLeft) + (minRight.weight * 2)) / (
                    totalWeightRight + totalWeightLeft)
            if difference < 0.1:  # keep min in Left/not move to Right still in 10%
                goLeft.append(goRight[0])
                goRight.pop(0)
                goLeft = goLeft[1:] + [goLeft[0]]
                totalWeightLeft = sumWeight(goLeft)
                totalWeightRight = sumWeight(goRight)
            else:  # min is already in correct side
                print('no check right')
                checkRight = False
        else:
            goRight = goRight[1:] + [goRight[0]]

        if not checkLeft and not checkRight:
            swapable = False

    tempGoLeft = []
    for box in goLeft:
        if box.colNum > MID_LINE:  # is in wrong side
            tempGoLeft.append(box)
    tempGoLeft, goLeft = goLeft, tempGoLeft  # swap
    tempGoLeft.clear()

    tempGoRight = []
    for box in goRight:
        if box.colNum <= MID_LINE:  # is in wrong side
            tempGoRight.append(box)
    tempGoRight, goRight = goRight, tempGoRight  # swap
    tempGoRight.clear()

    tLeft = []
    tRight = []
    for c in goLeft:
        tLeft.append(c.weight)
    for c in goRight:
        tRight.append(c.weight)
    print(f'goleft: {tLeft}\ngoright: {tRight}\nchoice: {choice}')

    needmove = []
    for c in goLeft:
        needmove.append(c)
    for c in goRight:
        needmove.append(c)

    # print(f'needmove: {needmove[0].name}')
    BalanceBoxes(needmove)


def BalanceBoxes(arr):
    targetBoxes = arr
    while len(targetBoxes) > 0:  # pop after move
        print("need write this ")

        needMove = findBox(data, arr)

        for i in needMove:
            print(f'name: {i.name}')
        mytarget = needMove[len(needMove) - 1]
        # print(f'targetaaaaaaaaaaaaaaaaaa: {len(needMove)}')
        if len(needMove) <= 0:
            print('balance box index <=0')

        for box in needMove:  # box in arr + others on top
            if box.target == False:  # need move but not wanted
                if box.colNum > MID_LINE:  # it's on right
                    tempGrid = [row[MID_LINE - 1:] for row in data]  # index 0-5
                    tempGrid = tempGrid[:-2]
                    print_ship2(tempGrid)
                    row, col, dist = nearspot(box.rowNum, -1, tempGrid)
                    col += MID_LINE + 1  # offset for sliced grid
                    print(f'right to right: {box.name} coord: {box.rowNum} , {box.colNum}')
                    print(f'near: {row} , {col}')
                    mysequence.append(f'Move: [{box.rowNum + 1},{box.colNum + 1}] to [{row + 1},{col + 1}]')
                    swapData(box.rowNum, box.colNum, row, col, data)
                    state = copy.deepcopy(data)
                    states.append(state)
                    print_ship2(data)


                else:  # its on left
                    tempGrid = [row[:MID_LINE + 1] for row in data]
                    tempGrid = tempGrid[:-2]
                    print_ship2(tempGrid)
                    row, col, dist = nearspot(box.rowNum, box.colNum, tempGrid)
                    print(f'left to left: {box.name} coord: {box.rowNum} , {box.colNum}')
                    print(f'near: {row} , {col} dist:{dist}')
                    mysequence.append(f'Move: [{box.rowNum + 1},{box.colNum + 1}] to [{row + 1},{col + 1}]')
                    swapData(box.rowNum, box.colNum, row, col, data)
                    state = copy.deepcopy(data)
                    states.append(state)
                    print_ship2(data)
            else:  # is target box
                if box.colNum <= MID_LINE:  # it's on left
                    tempGrid = [row[MID_LINE + 1:] for row in data]  # index for right
                    tempGrid = tempGrid[:-2]
                    print_ship2(tempGrid)
                    row, col, dist = nearspot(box.rowNum, -1, tempGrid)
                    col += MID_LINE + 1  # offset for sliced grid
                    # mysequence.append("balance: ")
                    print(f'left to right: {box.name} coord: {box.rowNum} , {box.colNum}')
                    print(f'near: {row} , {col} dist:{dist}')
                    mysequence.append(f'Move: [{box.rowNum + 1},{box.colNum + 1}] to [{row + 1},{col + 1}]')
                    swapData(box.rowNum, box.colNum, row, col, data)
                    state = copy.deepcopy(data)
                    states.append(state)
                    print_ship2(data)

                else:  # its on right
                    tempGrid = [row[:MID_LINE + 1] for row in data]
                    tempGrid = tempGrid[:-2]
                    print_ship2(tempGrid)
                    row, col, dist = nearspot(box.rowNum, box.colNum, tempGrid)
                    print(f'right to left: {box.name} coord: {box.rowNum} , {box.colNum}')
                    print(f'near: {row} , {col}')
                    mysequence.append(f'Move: [{box.rowNum + 1},{box.colNum + 1}] to [{row + 1},{col + 1}]')
                    swapData(box.rowNum, box.colNum, row, col, data)
                    state = copy.deepcopy(data)
                    states.append(state)
                    print_ship2(data)
        targetBoxes.remove(mytarget)


def swapData(row1, col1, row2, col2, grid):
    # 2 is always unused before swap
    grid[row2][col2].weight, grid[row1][col1].weight = grid[row1][col1].weight, grid[row2][col2].weight
    grid[row2][col2].name, grid[row1][col1].name = grid[row1][col1].name, grid[row2][col2].name


def findBox(grid, arr):
    names = []
    needMoves = []
    for box in arr:
        names.append(box.name)
    # print(f'hhhhhhhhhhhh {names}')
    for row in grid[::-1]:  # top row first
        for box in row:
            # print(f'ccccc: {row} col {col}')
            # box = grid[row][col]

            if box in arr:  # found target box

                temp = checkTop(grid, box)
                for asd in temp[::-1]:
                    needMoves.append(asd)
                box.target = True
                needMoves.append(box)
                return needMoves
    # print(f'hhhhhhhhhhhh {len(needMoves)}')


def checkTop(grid, currentBox):
    needMove = []
    row = currentBox.rowNum
    col = currentBox.colNum
    for i in range(row + 1, len(grid)):
        if grid[i][col].name != 'UNUSED' and grid[i][col].name != 'NAN':
            needMove.append(grid[i][col])

    return needMove


def sumWeight(arr):
    total = 0
    for c in arr:
        # if c.colNum > 6:
        total += c.weight
    return total


def chooseSide(arr1, arr2):
    # arr1 left
    arr1_to_left = 0
    arr1_to_right = 0
    arr2_to_left = 0
    arr2_to_right = 0

    for x in arr1:
        if x.colNum > 6:  # is on right
            arr1_to_left += x.colNum - 6  # dist to left
        else:  # is on left
            arr1_to_right += 6 - x.colNum  # dist to right

    for x in arr2:
        if x.colNum > 6:
            arr2_to_left += x.colNum - 6
        else:
            arr2_to_right += 6 - x.colNum

    sol_1_left = arr1_to_left + arr2_to_right
    sol_2_left = arr2_to_left + arr1_to_right
    if sol_1_left < sol_2_left:
        return 1  # first param need to left, second to right
    else:
        return 2  # second param need to left, first to right


def checkside(x, y):  # already top layer
    if data[x][y].name == 'UNUSED':  # if spot is available, return
        return x, y
    else:  # check 8 spots around x y
        radius = 1
        row = x
        col = y
        if data[row][col + radius].name == 'UNUSED' and data[row - radius][
            col + radius].name != 'UNUSED':  # right spot is available and not mid air

            # return: available_rowNum, available_colNum, distance
            return row, col + radius

        if data[row][col - radius].name == 'UNUSED' and data[row - radius][
            col + radius].name != 'UNUSED':  # left corner is available and not mid air

            # return: available_rowNum, available_colNum, distance
            return row, col - radius


def AvailableSpot(x, y, grid):
    spots = []

    for i in range(len(grid[0])):  # 12
        for j in range(len(grid)):  # 8 or 10
            if validspot(j, i, grid) and y != i:  # not check self
                d = getdistance(x, y, j, i)
                spots.append([j, i, d])
                print("spot: ")
                print([j, i, d])
                break
            else:
                continue

    return spots


def getdistance(src_x, src_y, des_x, des_y):  # h(n) distance from source to destination, ignore blocks in between
    return abs(src_x - des_x) + abs(src_y - des_y)


def nearspot(x, y, grid):  # return the x , y ,dist of nearest aviliable spot
    spots = AvailableSpot(x, y, grid)
    sorted_list = sorted(spots, key=lambda x: x[2])
    if y == -1:
        sorted_list[0][2] += 1
    global estimatedTime
    estimatedTime += int(sorted_list[0][2])
    print(f'time: {estimatedTime}')
    return sorted_list[0]


def validspot(row, col, grid):  # is available and not mid air
    if grid[row][col].name == 'UNUSED' and grid[row - 1][col].name != 'UNUSED':
        return True
    if grid[row][col].name == 'UNUSED' and row == 0:  # is available and already bottom row
        return True

    return False


def markBox(grid, names):  # mark target boxes
    for row in grid:  # mark target boxes
        for box in row:
            if box.name in names:  # name matches todo list
                box.target = True
    return grid


def partition(arr):
    arr = sorted(arr, key=lambda x: x.weight, reverse=True)
    sum1 = 0
    sum2 = 0
    l1 = []
    l2 = []
    for i in range(len(arr)):
        if sum1 <= sum2:
            sum1 += arr[i].weight
            l1.append(arr[i])
        else:
            sum2 += arr[i].weight
            l2.append(arr[i])
    return l1, l2


def checkBalance():
    mid = 6
    total_left = 0
    # if(abs(left-right))
    for i in range(int(len(data) - 2)):
        for j in range(mid):
            total_left += data[i][j].weight

    total_right = 0
    for i in range(int(len(data) - 2)):
        for j in range(mid, 12):
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


def getGrid(r):
    arr = []
    for i in range(9, -1, -1):
        col = []
        for j in range(12):
            col.append(states[r][i][j].name)
        arr.append(col)
    print(arr)
    return arr


def creategrid(r):
    arr = getGrid(r)

    for i in range(10):
        for j in range(12):
            n = arr[i][j]
            if (n == 'NAN'):
                Button(frame2, text=n, height=3, width=6, bg='black', fg='white').grid(row=i, column=j, ipadx=3,
                                                                                       ipady=3)
            elif (n == 'UNUSED'):
                Button(frame2, text=n, height=3, width=6, bg='white', fg='black').grid(row=i, column=j, ipadx=3,
                                                                                       ipady=3)
            else:
                Button(frame2, text=n, height=3, width=6, bg='blue', fg='white').grid(row=i, column=j, ipadx=3, ipady=3)
    for i in range(8):
        for j in range(12):
            n = arr[i][j]
            if (n == 'NAN'):
                Button(frame2, text=n, height=3, width=6, bg='black', fg='white').grid(row=i, column=j, ipadx=3,
                                                                                       ipady=3)
            elif (n == 'UNUSED'):
                Button(frame2, text=n, height=3, width=6, bg='white', fg='black').grid(row=i, column=j, ipadx=3,
                                                                                       ipady=3)
            else:
                Button(frame2, text=n, height=3, width=6, bg='blue', fg='white').grid(row=i, column=j, ipadx=3, ipady=3)


def counter():
    global step
    global frame
    global ws
    global mysequence
    if (len(states) - 1 == step):

        done_label = Label(frame, text="Congrats! Job is Done")
        # done_label.place(relx=2, rely=2, anchor='ne')
        done_label.pack(ipadx=10, ipady=10)
    else:
        seq = mysequence[step]
        seq_label = Label(frame, text=seq)
        seq_label.pack(ipadx=10, ipady=10)
        step = step + 1
    creategrid(step)


if __name__ == '__main__':

    # #a = [3044,1100,2020,10000,2011,2007,2000]
    # a =[9041,10001,500,600,100,10]
    # n = len(a)

    # print(
    #   "2 sets is ", select(a, 0, sum(a)/2))

    ship = []
    # change path below to target manifest location
    path = r"./manifests/testBlue.txt"
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
    mysequence = []  # give instruction to operator to move
    states = []
    step = 0
    estimatedTime = 0
    crane_x = 9
    crane_y = 1

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
    inital = copy.deepcopy(data)
    states.append(inital)
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
    # for x in t1:
    #     print(f'here: {x.weight}')

    choice = chooseSide(t2, t1)
    print(f'choice: {choice}')
    # for x in range(int(len(data))):
    #     for y in range(int(len(data[0]))):
    #         print(f'[{data[x][y].rowNum} , {data[x][y].colNum}] w: {data[x][y].weight} n: {data[x][y].name}')
    # print_ship2()
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
    # tempGrid = [row[:6] for row in data]
    # tempGrid = data[:-2]
    # tr,tc,d = nearspot(8,-1,tempGrid)
    # print(f'near: {tr} , {tc} dist:{d}')
    print_ship2(data)
    menu()  # display main menu, input choice
    print('moving sequence:\n')
    print(mysequence)
    print(f'estimated time: {estimatedTime}')

    # for i in range(len(states)):
    #    print_ship2(states[i])

    f = open("demofile2.txt", "w")
    for row in data[:-2]:
        for box in row:
            s = str(box.weight).zfill(5)
            f.write(f"[{str(box.rowNum + 1).zfill(2)},{str(box.colNum + 1).zfill(2)}], {{{s}}}, {box.name}\n")

    f.close()
    ws = Tk()
    ws.title('179M')
    ws.geometry('1200x900')
    ws.config(bg='#F2B33D')

    frame1 = Frame(ws)
    frame1.pack(side=TOP, fill=X)

    # frame3 = Frame(ws)
    # frame3.pack(side=BOTTOM, fill=X, pady=5)

    frame2 = Frame(ws)
    frame2.pack(side=LEFT, fill=Y, padx=10, pady=10)

    frame = Frame(ws)  # parent of frame4 and frame5
    frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
    # frame.grid_columnconfigure(0, weight=1)
    # frame.grid_rowconfigure(0, weight=1)
    # frame.grid_rowconfigure(1, weight=1)
    # frame4 = Frame(frame, bd=1, relief='solid')
    # frame4.grid(sticky='nsew', padx=5, pady=5)
    #
    # frame4 = Frame(frame, bd=1, relief='solid')
    # frame4.grid(sticky='nsew', padx=5, pady=5)
    Button(frame, text="Next", height=3, width=6, bg='white', fg='black', command=counter).pack(ipadx=3, ipady=3)
    creategrid(0)
    frame.pack(expand=True)
    ws.mainloop()

    # for x in range(int(len(data))):
    #     for y in range(int(len(data[0]))):
    #         print(f'[{data[x][y].rowNum} , {data[x][y].colNum}] w: {data[x][y].weight} n: {data[x][y].name}')
