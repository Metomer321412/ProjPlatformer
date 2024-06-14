import tkinter as tk
from tkinter import *
from database import DATABASE
from pathlib import Path
import sqlite3

PATH = Path(__file__).parent / "data.db"

master = Tk()
master.title("Color Options in Tkinter")
w = Canvas(master, width=500, height=500)
w.pack()

def get_button(t):
    t.destroy()

def get_sign():
    save1 = entry.get()
    words1 = save1.split(",")
    username1 = words1[0]
    password1 = words1[1]
    DATABASE.add_user(username1,password1)
    DATABASE.printall()

#def get_sign(sock):

   #     save1 = entry.get()
   #     sndsng = "sign" + save1
  #      print("snding" + sndsng)
   #     sock.send(sndsng.encode())
#def get_log(sock):


#      save2 = entry2.get()
#      sndlog = "log" + save2
#      print("snding" + sndlog)
#      sock.send(sndlog.encode())
#     if my_socket.recv(1024).decode()== "true":
#         print('yes')
#         get_button(w)
#         secondscreen()
def get_log():
    save2 = entry2.get()
    words2 = save2.split(",")
    username2 = words2[0]
    password2 = words2[1]
    if DATABASE.authenticate_user(username2, password2):
        get_button(w)
        secondscreen()

def Back(w):
    w.destroy()
    secondscreen()

def get_Rules(w):
    print("x")
    w.destroy()
    w = Canvas(master, width=500, height=500)
    w.pack()
    Rules=tk.Button(master, text="There is only one rule - Push the enemy player out of the map to win",activebackground="blue", activeforeground="white")
    Rules.place(x=100, y=50)
    buttonB = tk.Button(master, text="BACK", activebackground="blue", activeforeground="white",
                        command=lambda t="Button-1 Clicked": Back(w))
    buttonB.place(x=280, y=100,anchor= CENTER)

def get_Keys(w):
    w.destroy()
    w = Canvas(master, width=500, height=500)
    w.pack()
 #   Keys = tk.Button(master, text="There is only one rule - Push the enemy player out of the map to win",
     #                 activebackground="blue", activeforeground="white")
  #  Rules.place(x=100, y=50)
    buttonB = tk.Button(master, text="BACK", activebackground="blue", activeforeground="white",
                        command=lambda t="Button-1 Clicked": Back(w))
    buttonB.place(x=280, y=100, anchor=CENTER)


def secondscreen():
    w = Canvas(master, width=500, height=500)
    w.pack()
    print("y")
    buttonS = tk.Button(master, text="START", activebackground="blue", activeforeground="white",
                        command=lambda t="Button-1 Clicked": get_button(master))
    buttonR = tk.Button(master, text="RULES", activebackground="blue", activeforeground="white",command=lambda t="Button-2 Clicked": get_Rules(w))
    buttonB = tk.Button(master, text="KEYS", activebackground="blue", activeforeground="white")
    # buttonSign = tk.Button(master, text="Sign in", activebackground="blue", activeforeground="white",command= lambda t= "Button-1 Clicked": retrieve_input())

    buttonB.place(x=180, y=50)
    buttonR.place(x=230, y=50)
    buttonS.place(x=280, y=50)

entry = Entry(master, width= 42)
entry.place(relx= .5, rely= .5, anchor= CENTER)

label= Label(master, text="", font=('Helvetica 13'))
label.pack()
tk.Button(master, text= "sign in: username,password", command= get_sign).place(relx= .7, rely= .5, anchor= CENTER)


entry2 = Entry(master, width= 42)
entry2.place(relx= .5, rely= .6, anchor= CENTER)

label2= Label(master, text="", font=('Helvetica 13'))
label2.pack()
tk.Button(master, text= "log in: username,password", command= get_log).place(relx= .7, rely= .6, anchor= CENTER)

print("yasda")
#buttonSign.place(x=230,y=20)
mainloop()


