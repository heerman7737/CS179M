import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random

root = Tk()
linear_array = [i for i in range(1,26)]
random_array = []
removed_numbers=[]
number_to_send = None
num_to_recv = None

#Creating Frames
frame1 = Frame(root)
frame1.pack(side=TOP, fill=X)

frame3 = Frame(root)
frame3.pack(side=BOTTOM, fill=X, pady=5)

frame2 = Frame(root)
frame2.pack(side=LEFT, fill=Y, padx=10, pady=10)

frame = Frame(root) # parent of frame4 and frame5
frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
# make frame4 and frame5 use all the space
frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame4 = Frame(frame, bd=1, relief='solid')
frame4.grid(sticky='nsew', padx=5, pady=5)

frame4 = Frame(frame, bd=1, relief='solid')
frame4.grid(sticky='nsew', padx=5, pady=5)
#Button click function
def numberClick(num,btn):
    global number_to_send
    #messagebox.showinfo('Message',str(num)+' is removed')
    number_to_send = num
    removed_numbers.append(num)
    btn.configure(text='X')
    btn.configure(bg='red',fg='white')
    btn.configure(state="disabled")
    print(removed_numbers)
    stmnt = str(num)+" was removed!!"
    textBox.delete('1.0', END)
    textBox.insert(END,stmnt)
    textBox.tag_add("center", 1.0, "end")

#Generating linear array and a random array from the linear array
for i in range(1,26):
    temp = random.choice(linear_array)
    linear_array.remove(temp)
    random_array.append(temp) 

#Generating Title bar
title = Label(frame1,text='B . I . N . G . O !!!',fg='red',bg='yellow')
title.config(font=("Courier", 30))
title.pack(side=TOP,fill=X)

#Generating a 5x5 Button matrix
rows=5
columns=5
btns = [[None for i in range(rows)] for j in range(columns)]
button_mapping = {}
for i in range(rows):
    for j in range(columns):
        num = random.choice(random_array)
        random_array.remove(num)
        btns[i][j]=Button(frame2, text = num , fg ='red',height = 3, width = 5)
        btns[i][j]['command']=lambda btn=btns[i][j],num=num: numberClick(num,btn)
        btns[i][j]['borderwidth'] = 2
        btns[i][j]['relief'] = "groove"
        btns[i][j].grid(row=i,column=j)
        button_mapping[num]=btns[i][j]

#Printing numbers which are deleted 
textBox = Text(frame3, height = 1, width = 28)
textBox.tag_configure("center", justify='center')
textBox.insert("1.0","Recently Deleted Number")
textBox.tag_add("center", 1.0, "end")
textBox.pack(side=TOP)
   
root.mainloop()