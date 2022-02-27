from tkinter import *
from main import*
ws = Tk()
ws.title('PythonGuides')
ws.geometry('1200x900')
ws.config(bg='#F2B33D')

frame = Frame(ws, bg='#F2B33D')


Button(frame, text="7").grid(row=8, column=12,ipadx=3, ipady=3)
Button(frame, text="6").grid(row=7, column=12,ipadx=3, ipady=3)
Button(frame, text="5").grid(row=6, column=12,ipadx=3, ipady=3)
Button(frame, text="4").grid(row=5, column=12,ipadx=3, ipady=3)
Button(frame, text="3").grid(row=4, column=12,ipadx=3, ipady=3)
Button(frame, text="2").grid(row=3, column=12,ipadx=3, ipady=3)

Button(frame, text="7").grid(row=8, column=11,ipadx=3, ipady=3)
Button(frame, text="6").grid(row=7, column=10,ipadx=3, ipady=3)
Button(frame, text="5").grid(row=6, column=9,ipadx=3, ipady=3)
Button(frame, text="4").grid(row=5, column=8,ipadx=3, ipady=3)
Button(frame, text="3").grid(row=4, column=7,ipadx=3, ipady=3)
Button(frame, text="2").grid(row=3, column=6,ipadx=3, ipady=3)

def creategrid():
    w =12
    h =8
    for i in range(h):
        for j in range(w):
            Button(frame, text="7").grid(row=i, column=j,ipadx=3, ipady=3)
#creategrid()
frame.pack(expand=True) 

ws.mainloop()