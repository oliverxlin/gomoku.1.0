from tkinter import *
from tkinter.messagebox import *
import json
import requests
import re
import gomoku_alone
import gomoku_online
from tkinter import *
from PIL import Image ,ImageTk
filename = 'gomoku.png'
root = Tk()
img = PhotoImage(file=filename)
label = Label(root, image=img)
label.pack()
root.mainloop()