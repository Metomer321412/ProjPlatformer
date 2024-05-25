import tkinter as tk
from tkinter import *
import database

master = Tk()
master.title("Color Options in Tkinter")
w = Canvas(master, width=500, height=500)
w.pack()

def get_button(t):
    t.destroy()

def get_data():
    save = entry.get()
    print(save)
    words = save.split(",")
    username = words[0]
    password = words[1]
    add_user(username,password)
    print(username)
    print(password)
entry = Entry(master, width= 42)
entry.place(relx= .5, rely= .5, anchor= CENTER)

label= Label(master, text="", font=('Helvetica 13'))
label.pack()

tk.Button(master, text= "sign in: username,password", command= get_data).place(relx= .7, rely= .5, anchor= CENTER)

buttonS = tk.Button(master, text="START", activebackground="blue", activeforeground="white",command= lambda t= "Button-1 Clicked": get_button(master))
buttonR = tk.Button(master, text="RULES", activebackground="blue", activeforeground="white")
buttonB = tk.Button(master, text="KEYS", activebackground="blue", activeforeground="white")
buttonSign = tk.Button(master, text="Sign in", activebackground="blue", activeforeground="white",command= lambda t= "Button-1 Clicked": retrieve_input())

buttonB.place(x=180, y=50)
buttonR.place(x=230, y=50)
buttonS.place(x=280, y=50)
buttonSign.place(x=230,y=20)
mainloop()


