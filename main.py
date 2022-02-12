
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    ship=[]
    # change path below to target manifest location
    path = r'C:\Users\the\PycharmProjects\pythonProject14\CrisDeBurg.txt'
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




    print(ship[95].name)
    print(f"size: {len(ship)}\n")
    # col = index % 12
    # row = index // 8

    data = []
    for x in range (8):
        row = []
        for y in range (12):
            row.append(ship[y + (12*x)])
        data.append(row)

    print( f'x: {len(data)} y: {len(data[0])}')

    for x in range (int(len(data))):
        for y in range (int(len(data[0]))):
            print(data[x][y].name)

    # C:\Users\the\PycharmProjects\pythonProject14\CrisDeBurg.txt
