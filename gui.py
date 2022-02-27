from tkinter import *
from main import*
ws = Tk()
ws.title('PythonGuides')
ws.geometry('400x300')
ws.config(bg='#F2B33D')

frame = Frame(ws, bg='#F2B33D')


Button(frame, text="7").grid(row=8, column=12,ipadx=3, ipady=3)
Button(frame, text="6").grid(row=7, column=12,ipadx=3, ipady=3)

def creategrid():
    w =12
    h =8
    for i in range(h):
        for j in range(w):
            Button(frame, text="7").grid(row=i, column=j,ipadx=3, ipady=3)
#creategrid()
frame.pack(expand=True) 

ws.mainloop()