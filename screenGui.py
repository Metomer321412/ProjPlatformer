import tkinter as tk
from tkinter import *
master = Tk()
master.title("Color Options in Tkinter")
w = Canvas(master, width=500, height=500)
w.pack()

def get_button(t):
    t.destroy()

buttonS = tk.Button(master, text="START", activebackground="blue", activeforeground="white",command= lambda t= "Button-1 Clicked": get_button(master))
buttonR = tk.Button(master, text="RULES", activebackground="blue", activeforeground="white")
buttonB = tk.Button(master, text="KEYS", activebackground="blue", activeforeground="white")

buttonB.place(x=180, y=50)
buttonR.place(x=230, y=50)
buttonS.place(x=280, y=50)

mainloop()


