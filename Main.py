import math
import time
from tkinter import *
import keyboard
import mouse

root = Tk()
c = Canvas(width=800, height=800)
c.pack()
c.pack_configure()

is_there_a_bullet = False
shipX = 400
shipY = 700
xy = [(shipX, shipY), (shipX+20, shipY+10), (shipX, shipY-40), (shipX-20, shipY+10)]

player_ship = c.create_polygon(xy)
debug_text = c.create_text(1, 1, anchor='nw')

def movement(event):
    global text_val
    global shipX
    global shipY
    text_val = []
    shipX = event.x
    shipY = event.y + 10
    newxy = [(shipX, shipY), (shipX + 20, shipY + 10), (shipX, shipY - 40), (shipX - 20, shipY + 10)]
    text_val = newxy
    c.coords(player_ship, *newxy)
    c.itemconfig(debug_text, text=text_val)

def shoot(event):
    Xorigin = event.x - 3
    Yorigin = event.y - 1
    c.create_rectangle(Xorigin, Yorigin, Xorigin+6, Yorigin-20, fill='black')


c.bind("<Motion>", movement)
c.bind("<Button-1>", shoot)

mainloop()
