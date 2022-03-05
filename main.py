from ast import Constant
from cmath import log10
import csv
import copy
from glob import escape, glob
import imp
from math import dist
import sys
import time
from operator import attrgetter
from functools import partial
from tkinter import filedialog
from tkinter import *
from tkinter.tix import *
from turtle import ondrag
from main import *
from itertools import chain
from datetime import datetime
import os

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


def offload(box, isOnPort):  # move current box
    global crane_x
    global crane_y
    global estimatedTime
    print('unload all needed containers first')

    if box.target == True:  # is my target, unload to pink
        nameLogBox = box.name
        box.weight = 0
        box.name = 'UNUSED'  # delete box
        box.target = False
        state = copy.deepcopy(data)
        states.append(state)
        mysequence.append(f'Offload: [{box.rowNum + 1},{box.colNum + 1}] to [9,1](pink)')
        writeLog(f'"{nameLogBox}" is offloaded')

        tempTime = getdistance(crane_x, crane_y, box.rowNum, box.colNum) + getdistance(box.rowNum, box.colNum, 8, 0)
        # print('ttttttttttttttttttttttt')
        print(getdistance(crane_x, crane_y, box.rowNum, box.colNum))
        if isOnPort:
            tempTime += 2
        estimatedTime += tempTime + 2
        estimatedTimeEach.append(tempTime)
        crane_x = 8
        crane_y = 0
        isOnPort = True
    else:  # not target, move to elsewhere
        nameLogBox = box.name

        row, col, dist = nearspot(box.rowNum, box.colNum, data)
        swapData(box.rowNum, box.colNum, row, col, data)
        state = copy.deepcopy(data)
        states.append(state)
        mysequence.append(f'Move: [{box.rowNum + 1},{box.colNum + 1}] to [{row + 1},{col + 1}]')
        writeLog(f'"{nameLogBox}" is moved to ship: [{row},{col}]')
        tempTime = getdistance(crane_x, crane_y, box.rowNum, box.colNum) + getdistance(box.rowNum, box.colNum, row, col)
        if isOnPort:
            tempTime += 2
        estimatedTime += tempTime
        estimatedTimeEach.append(tempTime)
        crane_x = row
        crane_y = col
        isOnPort = False
    return isOnPort


def load(todo_on, isOnPort):  # 2
    global crane_x
    global crane_y
    global estimatedTime
    print('load all new containers')

    useless, weight, name = todo_on[0].split()
    todo_on.pop(0)
    # print(f"todo weight:{weight} name:{name}")
    tempgrid = data[:-2]
    row, col, dist = nearspot(8, -1, tempgrid)  # virtual pink top left

    data[row][col].name = name
    data[row][col].weight = weight
    state = copy.deepcopy(data)
    states.append(state)
    mysequence.append(f'Onload: {name} to [{row + 1},{col + 1}]')
    writeLog(f'"{name}" is onloaded to ship: [{row},{col}]')

    tempTime = getdistance(crane_x, crane_y, 8, 0) + getdistance(8, 0, row, col)
    if isOnPort:
        tempTime += 2
    estimatedTime += tempTime
    estimatedTimeEach.append(tempTime)
    crane_x = row
    crane_y = col
    # print('===========ship==================')
    print_ship2(data)
    if checkBot(row, col):
        return True, data[row][col]
    return False, data[row][col]


def checkBot(row, col):
    for i in reversed(range(0, row + 1)):
        # print(f'checkbot: {i}')
        if data[i][col].target == True:
            print(f'ccccccccheckbot: {i} true')
            return True
    return False


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
    global crane_x
    global crane_y
    global estimatedTime
    isOnPort = True
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

    BoxToOffload = []
    for i in range(len(todo_off)):  # parse input and link box in data
        # print(f'here: {len(todo_off)}')
        option, offrow, offcol = todo_off[i].split()
        # print(f'unload todo:{row}, {col}')
        BoxToOffload.append(data[int(offrow) - 1][int(offcol) - 1])  # input matches manifest

    needMove = findBox(data, BoxToOffload)  # find target boxes and stuff on top

    while len(needMove) > 0 or len(todo_on) > 0:  # if one of two task is not done
        onDist = offDist = 999999
        if len(todo_on) > 0:
            onDist = 0
            if not isOnPort:
                onDist = getdistance(crane_x, crane_y, 8, 0) + 2
        if len(needMove) > 0:  # if has offload task left, calc offDist

            box = nearBox(data, needMove)
            offDist = getdistance(crane_x, crane_y, box.rowNum, box.colNum)
            if isOnPort:
                offDist += 2
        if offDist < onDist:  # offload cost better than onload
            print('running offload algorithm... \n')
            isOnPort = offload(box, isOnPort)
            needMove.remove(box)


        else:  # onload cost better than offload
            print('running load algorithm... \n')
            isOnPort = False
            isTargetUnder, newBox = load(todo_on, isOnPort)  # will pop inside load func
            if isTargetUnder:
                needMove.append(newBox)


def SIFT():
    print("running sift...")
    flatten_data = list(chain.from_iterable(data))  # make 2d list 1d
    flatten_box = []
    leftNext = True  # start load on left side first
    colSize = len(data[0]) / 2  # ie 6
    currentRow = 0
    offsetCol = 0  # offset, not actual colNum

    for each in flatten_data:  # keep box, not unused, NAN
        if each.weight != 0:

            flatten_boxes.append(each)
    allBox = sorted(flatten_boxes, key=lambda x: x.weight, reverse=True) # sort weight heavy -> light

    for each in allBox:
        print(f'allbox: {each.name}')
    while len(allBox) > 0 :  # large weight front, pop after done loop
        box = allBox[0]
        #print(f'\n\nworking on box: {box.name}')
        
        if leftNext:
            col = MID_LINE - offsetCol # goal left
        else:
            col = MID_LINE + offsetCol + 1 #goal right
            offsetCol+=1
        row = currentRow #goal col 
        print(f'moving {box.name} to  {row} , {col}')
        if data[row][col].name != 'NAN':
            leftNext = not leftNext # switch turn between left and right
            if data[row][col].name =='UNUSED': # goal spot is empty, just move
                nameLogBox = box.name
                swapData(box.rowNum, box.colNum, row, col, data)
                state = copy.deepcopy(data)
                states.append(state)
                tempTime = getdistance(crane_x, crane_y, box.rowNum, box.colNum) + getdistance(box.rowNum, box.colNum,row, col)
                estimatedTime += tempTime
                estimatedTimeEach.append(tempTime)
                mysequence.append(f'Move: [{box.rowNum + 1},{box.colNum + 1}] to [{row + 1},{col + 1}] ')
                writeLog(f'"{nameLogBox}" is moved to [{row},{col}]')
                crane_x = row
                crane_y = col
                
            else: # goal spot has box, remove whole col
                #print(f'box at goal: {data[row][col].name} ')
                removedNames,allBox = removeFromGoal(data[row][col],allBox)
                nameLogBox = box.name                        
                swapData(box.rowNum, box.colNum, row, col, data)
                state = copy.deepcopy(data)
                states.append(state)
                tempTime = getdistance(crane_x, crane_y, box.rowNum, box.colNum) + getdistance(box.rowNum, box.colNum,row, col)
                estimatedTime += tempTime
                estimatedTimeEach.append(tempTime)
                mysequence.append(f'Move: [{box.rowNum + 1},{box.colNum + 1}] to [{row + 1},{col + 1}] ')
                writeLog(f'"{nameLogBox}" is moved to [{row},{col}]')
                crane_x = row
                crane_y = col
                
        
        

        print_ship2(data)
        
        
        allBox.pop(0)


                
def removeFromGoal(box,allBox):
    global crane_x
    global crane_y
    global estimatedTime
    global estimatedTimeEach
    print('remove box and top from goal spot')
    needMove = checkTop(data, box)
    needMove.append(box)
    print(len(needMove))
    removedNames = []
    for eachBox in needMove: # sorted from top -> bot
        
        removedNames.append(eachBox.name)
        row, col, dist = nearspot(eachBox.rowNum, eachBox.colNum, data)
        print(f'removing: {eachBox.name} to {row}, {col}')
        tempname = eachBox.name
        
        for i in range(len(allBox)):
            #print(f'aaaaaaaaaaaaa: {allBox[i].name} bbbbbbbb {tempname}')
            if allBox[i].name == tempname:
                # print(f'aaaaaaaaaaaaa: {allBox[i].name} bbbbbbbb {tempname}')
                # #print('aaaaaaaaaaaaaaaaaaaaa')
                
                # print(f'after {i} sssssss {allBox[i].name}')
                # for e in allBox:
                #     print(f'eee: {e.name}')
                tempTime = getdistance(crane_x, crane_y, eachBox.rowNum, eachBox.colNum) + getdistance(eachBox.rowNum, eachBox.colNum,row, col)
                
                allBox.pop(i)
                allBox.insert(i,data[row][col])
                nameLogBox = eachBox.name
                swapData(eachBox.rowNum, eachBox.colNum, row, col, data)

                state = copy.deepcopy(data)
                states.append(state)
                
                estimatedTime += tempTime
                estimatedTimeEach.append(tempTime)
                mysequence.append(f'Move: [{eachBox.rowNum + 1},{eachBox.colNum + 1}] to [{row + 1},{col + 1}] ')
                writeLog(f'"{nameLogBox}" is moved to [{row},{col}]')
                
                crane_x = row
                crane_y = col

                # for e in allBox:
                #     print(f'qqq: {e.name}')
        
                
                


    return removedNames,allBox
        #need swap address in data
        
            flatten_box.append(each)
    allBox = sorted(flatten_box, key=lambda x: x.weight, reverse=True)  # sort weight heavy -> light

    while len(allBox) > 0:  # large weight front, pop after done loop

        for i in range(colSize):
            if leftNext:
                col = MID_LINE - offsetCol  # goal left
            else:
                col = MID_LINE + offsetCol + 1  # goal right
            row = currentRow  # goal col


def findGoal():  # sort and return
    print('find goal')


def balance(grid):
    left, right = checkBalance()
    if min(left, right) / max(left, right) > 0.9:  # ship is balanced when rate <= 10%
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

    weightArr1 = weightArr2 = 0
    for each in arr1:
        weightArr1 += each.weight

    for each in arr2:
        weightArr2 += each.weight

    if not (min(weightArr1, weightArr2) / max(weightArr1, weightArr2) > 0.9):
        SIFT()
        return
    choice = chooseSide(arr1, arr2)

    if choice == 1:  # arr1 need go left, arr2 need go right
        goLeft = arr1
        goRight = arr2
    else:  # choice == 2
        goLeft = arr2
        goRight = arr1

    goLeft.sort(key=lambda x: x.weight)
    goRight.sort(key=lambda x: x.weight)

    tLeft = []
    tRight = []
    for c in goLeft:
        tLeft.append(c.weight)
    for c in goRight:
        tRight.append(c.weight)

    # print(f'goleft: {tLeft}\ngoright: {tRight}\nchoice: {choice}')
    # ccccccccccccccccccccccccccccccccccccccccc
    goLeft, goRight = removeMin(goLeft, goRight)
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



def removeMin(goLeft, goRight):
    swapable = True  # not move min and still within 10%
    checkLeft = checkRight = True
    while (swapable):

        totalWeightLeft = sumWeight(goLeft)
        totalWeightRight = sumWeight(goRight)
        print(f'll:{totalWeightLeft} rr: {totalWeightRight}')
        tLeft = []
        tRight = []
        for c in goLeft:
            tLeft.append(c.weight)
        for c in goRight:
            tRight.append(c.weight)

        print(f'goleft: {tLeft}\ngoright: {tRight}\n')
        print(f'checkleft: {checkLeft} checkright: {checkRight} swapable: {swapable}')
        # print( f'{goLeft[0].weight} max {max(goLeft, key=attrgetter("weight")).weight}')
        if not checkLeft and not checkRight:
            swapable = False
        if goLeft[0].weight == max(goLeft, key=attrgetter('weight')).weight:
            checkLeft = False

        if goLeft[0].colNum > MID_LINE and checkLeft:  # if min is in wrong side/ need move

            minLeft = goLeft[0]
            # difference = (abs(totalWeightLeft - totalWeightRight) + (minLeft.weight * 2)) / (
            #         totalWeightLeft + totalWeightRight)
            tempGoLeft = totalWeightLeft + minLeft.weight
            tempGoRight = totalWeightRight - minLeft.weight
            difference = (min(tempGoLeft, tempGoRight)) / (max(tempGoLeft, tempGoRight))
            if difference > 0.9:  # keep min in right/not move to left still in 10%

                goRight.append(goLeft[0])
                goLeft.pop(0)
                goLeft = goLeft[1:] + [goLeft[0]]
                totalWeightLeft = sumWeight(goLeft)
                totalWeightRight = sumWeight(goRight)

            else:  # min is already in correct side
                print('no check left')
                checkLeft = False
        else:
            goLeft = goLeft[1:] + [goLeft[0]]

        if goRight[0].weight == max(goRight, key=attrgetter('weight')).weight:
            checkRight = False

        if goRight[0].colNum <= MID_LINE and checkRight:  # if currently on left
            # print(f"max {max(goRight, key=attrgetter('weight')).weight}, current: {goRight[0].weight} ")

            minRight = goRight[0]
            # difference = (abs(totalWeightRight - totalWeightLeft) + (minRight.weight * 2)) / (
            #         totalWeightRight + totalWeightLeft)
            tempGoLeft = totalWeightLeft + minRight.weight
            tempGoRight = totalWeightRight - minRight.weight
            difference = (min(tempGoLeft, tempGoRight)) / (max(tempGoLeft, tempGoRight))
            if difference > 0.9:  # keep min in Left/not move to Right still in 10%

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

    return goLeft, goRight


def BalanceBoxes(arr):
    targetBoxes = arr
    global crane_x
    global crane_y
    global estimatedTime
    needMove = findBox(data, targetBoxes)  # all box need move(target or tops)

    # for x in needMove:
    # print(f'neeeeeeee: {len(needMove)}')
    # print(f'findbox: {needMove[0].name}')
    while len(needMove) > 0:  # pop after move
        box = nearBox(data, needMove)
        # box = needMove[0]

        if box.target == False:  # need move but not wanted
            if box.colNum > MID_LINE:  # it's on right
                tempGrid = [row[MID_LINE + 1:] for row in data]  # index 0-5
                tempGrid = tempGrid[:-2]
                print_ship2(tempGrid)
                row, col, dist = nearspot(box.rowNum, box.colNum - (MID_LINE + 1), tempGrid)
                col += MID_LINE + 1  # offset for sliced grid
                print(f'right to right: {box.name} coord: {box.rowNum} , {box.colNum}')
                print(f'near: {row} , {col}')
                mysequence.append(f'Move: [{box.rowNum + 1},{box.colNum + 1}] to [{row + 1},{col + 1}]')
                writeLog(f'"{box.name}" is moved to [{row},{col}]')

                tempTime = getdistance(crane_x, crane_y, box.rowNum, box.colNum) + getdistance(box.rowNum, box.colNum,
                                                                                               row, col)
                estimatedTime += tempTime
                estimatedTimeEach.append(tempTime)
                crane_x = row
                crane_y = col

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
                writeLog(f'"{box.name}" is moved to [{row},{col}]')

                tempTime = getdistance(crane_x, crane_y, box.rowNum, box.colNum) + getdistance(box.rowNum, box.colNum,
                                                                                               row, col)
                estimatedTime += tempTime
                estimatedTimeEach.append(tempTime)
                crane_x = row
                crane_y = col
                swapData(box.rowNum, box.colNum, row, col, data)
                state = copy.deepcopy(data)
                states.append(state)
                print_ship2(data)
        else:  # is target box
            if box.colNum <= MID_LINE:  # it's on left
                tempGrid = [row[MID_LINE + 1:] for row in data]  # index for right
                tempGrid = tempGrid[:-2]
                print_ship2(tempGrid)
                row, col, dist = nearspot(box.rowNum, box.colNum - (MID_LINE + 1), tempGrid)
                col += MID_LINE + 1  # offset for sliced grid
                # mysequence.append("balance: ")
                print(f'left to right: {box.name} coord: {box.rowNum} , {box.colNum}')
                print(f'near: {row} , {col} dist:{dist}')
                mysequence.append(f'Move: [{box.rowNum + 1},{box.colNum + 1}] to [{row + 1},{col + 1}]')
                writeLog(f'"{box.name}" is moved to [{row},{col}]')
                tempTime = getdistance(crane_x, crane_y, box.rowNum, box.colNum) + getdistance(box.rowNum, box.colNum,
                                                                                               row, col)
                estimatedTime += tempTime
                estimatedTimeEach.append(tempTime)
                crane_x = row
                crane_y = col
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
                writeLog(f'"{box.name}" is moved to [{row},{col}]')
                tempTime = getdistance(crane_x, crane_y, box.rowNum, box.colNum) + getdistance(box.rowNum, box.colNum,
                                                                                               row, col)
                estimatedTime += tempTime
                estimatedTimeEach.append(tempTime)
                crane_x = row
                crane_y = col
                swapData(box.rowNum, box.colNum, row, col, data)
                state = copy.deepcopy(data)
                states.append(state)
                print_ship2(data)

        needMove.remove(box)


# def BalanceBoxes(arr):
#     targetBoxes = arr
#     while len(targetBoxes) > 0:  # pop after move
#         print("need write this ")

#         needMove = findBox(data, targetBoxes)

#         for i in needMove:
#             print(f'name: {i.name}')
#         mytarget = needMove[len(needMove) - 1]
#         # print(f'targetaaaaaaaaaaaaaaaaaa: {len(needMove)}')
#         if len(needMove) <= 0:
#             print('balance box index <=0')

#         for box in needMove:  # box in arr + others on top

#         targetBoxes.remove(mytarget)


def swapData(row1, col1, row2, col2, grid):
    # 2 is always unused before swap
    grid[row2][col2].weight, grid[row1][col1].weight = grid[row1][col1].weight, grid[row2][col2].weight
    grid[row2][col2].name, grid[row1][col1].name = grid[row1][col1].name, grid[row2][col2].name
    grid[row2][col2].target, grid[row1][col1].target = grid[row1][col1].target, grid[row2][col2].target


def findBox(grid, arr):
    names = []
    needMoves = []
    for target in arr:

        # print(f'hhhhhhhhhhhh {names}')
        for row in grid[::-1]:  # top row first
            for box in row:
                # print(f'ccccc: {row} col {col}')
                # box = grid[row][col]

                if box == target:  # found target box

                    temp = checkTop(grid, box)
                    for asd in temp[::-1]:
                        needMoves.append(asd)
                    box.target = True
                    needMoves.append(box)
    res = []
    [res.append(x) for x in needMoves if x not in res]
    return res


def nearBox(grid, needMove):  # return box close to crane position
    minDist = 999999  # some random large num
    minBox = needMove[0]  # assign random
    for box in needMove:
        temp = checkTop(grid, box)
        check = any(item in needMove for item in temp)  # if any tops also in needmove
        if check is True:
            continue
        dist = getdistance(crane_x, crane_y, box.rowNum, box.colNum)
        if dist < minDist:
            minDist = dist
            minBox = box
    return minBox


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
                # print("Available spot: ")
                # print([j, i, d])
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
    # global estimatedTime
    # estimatedTime += int(sorted_list[0][2])
    # print(f'time: {estimatedTime}')
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
    # choice = int(input("1. Load/offload \n2. Balance\n"))

    if decision == 1:
        # print('task 1 load offload\n')

        loadingUI()
    elif decision == 2:
        # print('task 2 balance\n')
        balance(data)
        balancePageUI()

    else:
        print('unknown choice, exit')


def getGrid(r):
    arrName = []
    arrWeight = []
    arrX = []
    arrY = []
    for i in range(9, -1, -1):
        col1 = []
        col2 = []
        col3 = []
        col4 = []
        for j in range(12):
            col1.append(states[r][i][j].name)
            col2.append(states[r][i][j].weight)
            col3.append(states[r][i][j].rowNum + 1)
            col4.append(states[r][i][j].colNum + 1)

        arrName.append(col1)
        arrWeight.append(col2)
        arrX.append(col3)
        arrY.append(col4)
    # print(arrName)
    return arrName, arrWeight, arrX, arrY


def creategrid(r):
    arr = getGrid(r)
    tip = Balloon()
    for i in range(10):
        for j in range(12):
            n = arr[0][i][j]
            w = arr[1][i][j]
            x = arr[2][i][j]
            y = arr[3][i][j]

            if (n == 'NAN'):
                b = Button(frame2, text=n, height=3, width=6, bg='black', fg='white')
                b.grid(row=i, column=j, ipadx=3, ipady=3)
                tip.bind_widget(b, balloonmsg="weight: " + str(w) + "\nlocation: [" + str(x) + "," + str(y) + "]")
            elif (n == 'UNUSED'):
                b = Button(frame2, text=n, height=3, width=6, bg='white', fg='black')
                b.grid(row=i, column=j, ipadx=3, ipady=3)
                tip.bind_widget(b, balloonmsg="weight: " + str(w) + "\nlocation: [" + str(x) + "," + str(y) + "]")
            else:
                temp = n[:5]
                if len(n) > 5:
                    temp += "..."
                b = Button(frame2, text=temp, height=3, width=6, bg='blue', fg='white')
                b.grid(row=i, column=j, ipadx=3, ipady=3)
                tip.bind_widget(b, balloonmsg="weight: " + str(w) + "\nlocation: [" + str(x) + "," + str(
                    y) + "]" + "\nName: " + n)
    # tip.bind_widget(my_button, balloonmsg="Python is an interpreted, high-level and general - purpose programming language")


def counter():
    global step
    global frame
    global ws
    global mysequence
    global estimatedTime
    global estimatedTimeEach
    frame.destroy()
    frame = Frame(ws)
    frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
    Button(frame, text="Next", height=3, width=6, bg='white', fg='black', command=counter).pack(ipadx=3, ipady=3)

    # print("here"+str(estimatedTimeEach))
    if len(states) - 1 == step:

        done_label = Label(frame, text="Congrats! Job is Done!\nNew manifest is saved")
        # done_label.place(relx=2, rely=2, anchor='ne')
        done_label.pack(ipadx=10, ipady=10)
    else:
        v = StringVar()

        estimatedTime -= estimatedTimeEach[step]
        v.set("Estimation Time: " + str(estimatedTime) + " minutes")

        estimate_label = Label(frame, textvariable=v)
        # estimate_label.update_idletasks()
        estimate_label.pack(ipadx=20, ipady=20)
        seq = mysequence[step]
        seq_label = Label(frame, text=seq)
        seq_label.pack(ipadx=10, ipady=10)

        step = step + 1
    creategrid(step)

def loadingUI():
    global loadws
    loadws = Tk()
    global append_boxes
    append_boxes =[]
    global f1, f2, f3
    loadws.title('Loading Page')
    loadws.geometry('1200x900')
    loadws.config(bg='#F2B33D')
    f1 = Frame(loadws)
    f2 = Frame(loadws)
    f3 = Frame(loadws)  
    f1.pack(side=TOP, fill=X)
    f2.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
    f3.pack(side=LEFT, fill=Y, padx=10, pady=10)
    #Button(f2, text="Name: ", height=3, width=6, bg='white', fg='black', command=counter).pack(ipadx=2, ipady=3)
    #Button(f2, text="Weight", height=3, width=6, bg='white', fg='black', command=counter).pack(ipadx=2, ipady=3)
    #Button(f2, text="F3Button", height=3, width=6, bg='white', fg='black', command=counter).pack(ipadx=3, ipady=3)

    r=0
    arrName = []
    arrWeight = []
    arrX = []
    arrY = []
    for i in range(9, -1, -1):
        col1 = []
        col2 = []
        col3 = []
        col4 = []
        for j in range(12):
            col1.append(states[r][i][j].name)
            col2.append(states[r][i][j].weight)
            col3.append(states[r][i][j].rowNum)
            col4.append(states[r][i][j].colNum)

        arrName.append(col1)
        arrWeight.append(col2)
        arrX.append(col3)
        arrY.append(col4)
    # print(arrName)
    arr=arrName, arrWeight, arrX, arrY
    #tip = Balloon(loadws)
    #tip = Balloon(tkWindow)
    for i in range(10):
        for j in range(12):
            n = arr[0][i][j]
            w = arr[1][i][j]
            x = arr[2][i][j]
            y = arr[3][i][j]
            if (n == 'NAN'):
                b = Button(f3, text=n, height=3, width=6, bg='black', fg='white')
                b.grid(row=i, column=j, ipadx=3, ipady=3)
            #   tip.bind_widget(b, balloonmsg="weight: "+str(w)+"\nlocation: ["+str(x)+","+str(y)+"]")
            elif (n == 'UNUSED'):
                b = Button(f3, text=n, height=3, width=6, bg='white', fg='black')
                b.grid(row=i, column=j, ipadx=3, ipady=3)
            #    tip.bind_widget(b, balloonmsg="weight: " + str(w) + "\nlocation: [" + str(x) + "," + str(y) + "]")
            else:
                b = Button(f3, text=n, height=3, width=6, bg='blue', fg='white')
                b.grid(row=i, column=j, ipadx=3, ipady=3)
            #    tip.bind_widget(b, balloonmsg="weight: " + str(w) + "\nlocation: [" + str(x) + "," + str(y) + "]")
    do_stuff()
def do_stuff():
    global nameEntry
    global weightEntry
    WeightLabel = Label(f2, text="Weight: ").grid(row=4, column=0)
    weight = IntVar()
    weightEntry = Entry(f2, textvariable=weight).grid(row=4, column=1) 
    nameLabel = Label(f2, text="Name: ").grid(row=6, column=0)
    name = StringVar()
    nameEntry = Entry(f2, textvariable=name).grid(row=6, column=1) 
    onloadfunction = partial(onloadfunc, weight, name) 
    offload_button = Button(f2,  text ='offload')
    offload_button.place(relx=0.1, rely=0.1, anchor=CENTER)
    onload_button = Button(f2,  text ='onload', command=onloadfunction)
    onload_button.place(relx=0.3, rely=0.1, anchor=CENTER)
    confirm_button = Button(f2,  text ='confirm', command=confirmfunc)
    confirm_button.place(relx=0.5, rely=0.1, anchor=CENTER)
   # clear_button = Button(f2,  text ='clear')
   # clear_button.place(relx=0.7, rely=0.1, anchor=CENTER, command=clearfunc)
    loadws.mainloop()

def onloadfunc(weight, name):
 
    print("name entered :", name.get())
    print("weight entered: ", weight.get())
    append_boxes.append([2,weight.get(),name.get()])
    print (append_boxes)
    do_stuff()
def confirmfunc():
    #load(append_boxes)
    task1()
def balancePageUI():

    global ws
    ws = Tk()
    global frame, frame1, frame2, estimatedTime

    ws.title('Balance Page')
    ws.geometry('1200x900')
    ws.config(bg='#F2B33D')
    frame1 = Frame(ws)
    frame2 = Frame(ws)
    frame = Frame(ws)  # parent of frame4 and frame5
    #balancePageUI()


    frame1.pack(side=TOP, fill=X)

    # frame3 = Frame(ws)
    # frame3.pack(side=BOTTOM, fill=X, pady=5)

    frame2.pack(side=LEFT, fill=Y, padx=10, pady=10)

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
    estimate_label = Label(frame, text="Estimation Time: " + str(estimatedTime) + " minutes")
    estimate_label.pack(ipadx=20, ipady=20)

    creategrid(0)
    # estimate_label.destroy()
    frame.pack(expand=True)
    ws.mainloop()


def validateLogin(username):
    print("username entered :", username.get())
    if username.get() != '':
        tkWindow.destroy()
        UploadPage()
    return


def balanceValidate():
    uploadWindow.destroy()
    # balancePageUI()
    global decision
    decision = 2


def onloadOffloadValidate():
    uploadWindow.destroy()
    
    global decision
    decision = 1

def UploadPage():
    global uploadWindow
    uploadWindow = Tk()
    uploadWindow.geometry('800x300')
    uploadWindow.title('Upload Page')
    upload_label = Label(uploadWindow, text="Upload a manifest:")
    upload_label.place(relx=0.5, rely=0.1, anchor=CENTER)
    upload_button = Button(uploadWindow, text='Choose File', command=lambda: open_file())
    upload_button.place(relx=0.5, rely=0.2, anchor=CENTER)
    load_button = Button(uploadWindow, text='Balance', command=balanceValidate)
    load_button.place(relx=0.4, rely=0.4, anchor=CENTER)
    balance_button = Button(uploadWindow, text='Offoad/Onload', command=onloadOffloadValidate)
    balance_button.place(relx=0.6, rely=0.4, anchor=CENTER)
    uploadWindow.mainloop()




def open_file():
    # file_path = askopenfile(mode='r', filetypes=[("Txt Files", "*txt")])
    global uploadWindow
    global filename
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    file_label = Label(uploadWindow, text=filename)
    file_label.place(relx=0.7, rely=0.1, anchor=CENTER)




def validateLogin(username):
    print("username entered :", username.get())
    if username.get() != '':
        writeLog(f'{username.get()} signed in')
        tkWindow.destroy()
        UploadPage()
    return


def balanceValidate():
    uploadWindow.destroy()
    # balancePageUI()
    global decision
    decision = 2


def onloadOffloadValidate():
    uploadWindow.destroy()
    # balancePageUI()
    global decision
    decision = 1

def UploadPage():
    global uploadWindow
    uploadWindow = Tk()
    uploadWindow.geometry('800x300')
    uploadWindow.title('Upload Page')
    upload_label = Label(uploadWindow, text="Upload a manifest:")
    upload_label.place(relx=0.5, rely=0.1, anchor=CENTER)
    upload_button = Button(uploadWindow, text='Choose File', command=lambda: open_file())
    upload_button.place(relx=0.5, rely=0.2, anchor=CENTER)
    load_button = Button(uploadWindow, text='Balance', command=balanceValidate)
    load_button.place(relx=0.7, rely=0.2, anchor=CENTER)
    # balance_button = Button(tkWindow, text='Offoad', command=validateUpload)
    # balance_button.place(relx=0.7, rely=0.4, anchor=CENTER)
    uploadWindow.mainloop()


    filename = ""
    decision = 0

    tkWindow = Tk()
    tkWindow.geometry('400x150')
    tkWindow.title('Login Page')

    # username label and text entry box
    usernameLabel = Label(tkWindow, text="User Name")
    usernameLabel.grid(row=0, column=0)
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username)
    usernameEntry.grid(row=0, column=1)
    validateLogin = partial(validateLogin, username)
    # login button
    loginButton = Button(tkWindow, text="Login", command=validateLogin)
    loginButton.grid(row=4, column=0)
    tkWindow.mainloop()

    # uploadWindow = Tk()



    # #a = [3044,1100,2020,10000,2011,2007,2000]
    # a =[9041,10001,500,600,100,10]
    # n = len(a)


def open_file():
    # file_path = askopenfile(mode='r', filetypes=[("Txt Files", "*txt")])
    global uploadWindow
    global filename
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    file_label = Label(uploadWindow, text=filename)
    file_label.place(relx=0.7, rely=0.1, anchor=CENTER)



def writeLog(message):
    curDateTime = datetime.now()
    dateTime = curDateTime.strftime("%m/%d/%Y: %H:%M:%S: ")
    f = open("logs.txt", "a")
    
    f.write(dateTime)
    f.write(message)

    f.write('\n')

    f.close()

    print("date and time:", dateTime)

def writeManifest():
    global tail
    filenameOUTBOUND = tail[:-4] + 'OUTBOUND' + tail[-4:]
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    f = open(desktop+ '\\' + filenameOUTBOUND, "w")
    for row in data[:-2]:
        for box in row:
            s = str(box.weight).zfill(5)
            f.write(f"[{str(box.rowNum + 1).zfill(2)},{str(box.colNum + 1).zfill(2)}], {{{s}}}, {box.name}\n")

    f.close()
    writeLog(f'Finished a cycle. Manifest "{filenameOUTBOUND}" was written to desktop, and reminder message to operator to send file was displayed')

def readManifest():
    global tail
    containerCounter = 0
    with open(filename, newline='') as csvfile:
        # read manifest and clean useless symbols, store to array of object"container"
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:

            for v in row[0].split():
                x = (row[0].split())[0][1:]
                y = (row[1].split())[0][:-1]
                weight = (row[2].split())[0][1:6]
                name = (",".join(row[3:]))
                name = name[1:]
                if name != 'UNUSED' and name != 'NAN':
                    containerCounter+=1
                ship.append(container(x, y, weight, name))
    writeLog(f'Manifest "{tail}" is opened, there are {containerCounter} containers on the ship')

def makeGrid():
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

if __name__ == '__main__':

    writeLog('Program opened')

    # global var here
    ship = [] # 1d list of 96 containers objects
    data = []  # 10x12 ship 2d grid
    buffer = []  # 4x24 buffer zone 2d grid
    todo = []  # load/offload todo list
    mysequence = []  # give instruction to operator to move
    states = [] # each grid to display
    step = 0
    estimatedTime = 0
    estimatedTimeEach = []
    crane_x = 8
    crane_y = 0
    filename = ""
    decision = 0 # 1 = load/offload, 2 = balance


    tkWindow = Tk()
    tkWindow.geometry('400x150')
    tkWindow.title('Login Page')

    # username label and text entry box
    usernameLabel = Label(tkWindow, text="User Name")
    usernameLabel.grid(row=0, column=0)
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username)
    usernameEntry.grid(row=0, column=1)
    validateLogin = partial(validateLogin, username)
    # login button
    loginButton = Button(tkWindow, text="Login", command=validateLogin)
    loginButton.grid(row=4, column=0)
    tkWindow.mainloop()



    head, tail = os.path.split(filename)
    readManifest()
    makeGrid() # construct data[][] buffer[][]

    menu()  # display BACKEND main menu, input choice
    print('moving sequence:\n')
    print(mysequence)
    print(f'estimated time: {estimatedTime}')
    print_ship2(data)

    writeManifest() # finish cycle, write OUTBOUND manifest


    ws = Tk()
    ws.title('Balance Page')
    ws.geometry('1200x900')
    ws.config(bg='#F2B33D')
    frame1 = Frame(ws)
    frame2 = Frame(ws)
    frame = Frame(ws)  # parent of frame4 and frame5
    balancePageUI()

    ws.mainloop()

