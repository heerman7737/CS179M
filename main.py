
import csv
class container:
    def __init__(self, x,y,w,n):
        self.coord_x = int(x)
        self.coord_y = int(y)
        self.weight = int(w)
        self.name = n


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def offload(todo_off):
    print('unload all needed containers first')
    for i in range(len(todo_off)):
        print(f'here: {len(todo_off)}')


    moves.append('unload all needed containers first')



def load(todo_on):
    print('load all new containers')
    moves.append('load all new containers')
    
def task1():
    print('task 1 load offload\n')
    # input format "on/off , x, y"
    todo_off = []
    todo_on = []
    userinput = input("input option as: 1/2 , x, y") #1 = off, 2 = on

    while userinput != "confirm":
        
        if userinput[0] =='1':
            todo_off.append(userinput)
        elif userinput[0] == '2':
            todo_on.append(userinput)
        
        userinput = input("input option as: 1/2 , x, y")

    print('running offload algorithm... \n')
    offload(todo_off);
    print('running load algorithm... \n')
    load(todo_on);

    



def task2():
    print('task 2 balance\n')



def menu():
    choice = int(input("1. Load/offload \n2. Balance\n"))
    
    if choice == 1:
        #print('task 1 load offload\n')
        task1()


    elif choice == 2:
        #print('task 2 balance\n')
        task2()

    else : 
        print('unknown choice, exit')




if __name__ == '__main__':

    ship=[]
    # change path below to target manifest location
    path = r"C:\Users\tongy\Desktop\CS179M\CS179M\manifests\CrisDeBurg.txt"
    with open(path, newline='') as csvfile:
        # read manifest and clean useless symbols, store to array of object"container"
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:

            for v in row[0].split():
                x = (row[0].split())[0][1:]
                y = (row[1].split())[0][:-1]
                weight = (row[2].split())[0][1:6]
                name = (",".join(row[3:]))
                ship.append(container(x,y,weight,name))
                #print(f'cord: ( {x}, {y} ) weight: {weight} name: {name} ')




    #print(ship[95].name)
    #print(f"size: {len(ship)}\n")

    # col = index % 12
    # row = index // 8

    #global var here
    data = [] # 10x12 ship 2d grid
    buffer = [] # 4x24 buffer zone 2d grid
    todo = [] # load/offload todo list
    moves = [] # give instruction to operator to move 
    
    for x in range (8): #store manifest to ship grid 8x12
        row = []
        for y in range (12):
            row.append(ship[y + (12*x)])
        data.append(row)

    for x in range (9,11): #use ship's row 9,10 as buffer
        row = []
        for y in range(12):
            row.append(container(x,y+1,0,"UNUSED")) 
        data.append(row)

    for x in range (4): #use ship's row 9,10 as buffer
        row = []
        for y in range(24):
            row.append(container(x+1,y+1,0,"UNUSED"))
        buffer.append(row)    

    print( f'size: x: {len(data)} y: {len(data[0])}')

    for x in range (int(len(data))):
        for y in range (int(len(data[0]))):
            print(f'[{data[x][y].coord_x} , {data[x][y].coord_y}] w: {data[x][y].weight} n: {data[x][y].name}')

    menu() #display main menu, input choice

    
