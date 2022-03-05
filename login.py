from tkinter import *
from functools import partial
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfile


def validateLogin(username):
    print("username entered :", username.get())
    if username.get() != '':
        tkWindow.destroy()
        UploadPage()
    return

def BalancePage():
    tkWindow = Tk()
    tkWindow.geometry('800x300')
    tkWindow.title('BalancePage')


def UploadPage():
    global uploadWindow
    uploadWindow = Tk()
    uploadWindow.geometry('800x300')
    uploadWindow.title('UploadPage')
    upload_label = Label(uploadWindow, text="Upload a pdf:")
    upload_label.place(relx=0.5, rely=0.1, anchor=CENTER)
    upload_button = Button(uploadWindow, text='Choose File', command=lambda: open_file())
    upload_button.place(relx=0.5, rely=0.2, anchor=CENTER)



def open_file():
    # file_path = askopenfile(mode='r', filetypes=[("Txt Files", "*txt")])
    global uploadWindow
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    file_label = Label(uploadWindow, text=filename)
    file_label.place(relx=0.7, rely=0.1, anchor=CENTER)


def OptionPage():
    tkWindow = Tk()
    tkWindow.geometry('800x300')
    tkWindow.title('Option Page')
    load_button = Button(tkWindow, text='Offload, Onload')
    load_button.place(relx=0.3, rely=0.2, anchor=CENTER)
    balance_button = Button(tkWindow, text='Balance')
    balance_button.place(relx=0.7, rely=0.2, anchor=CENTER)


if __name__ == '__main__':
    tkWindow = Tk()
    tkWindow.geometry('400x150')
    tkWindow.title('Tkinter Login Form - pythonexamples.org')

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

    uploadWindow = Tk()

    uploadWindow.mainloop()




