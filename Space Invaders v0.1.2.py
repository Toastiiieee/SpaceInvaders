import math
import time
from tkinter import *
import tkinter
import keyboard
import mouse
import asyncio

root = Tk()
c = Canvas(width=800, height=800)
c.pack()
c.pack_configure()

shipX = 400
shipY = 700
player_ship = c.create_rectangle(shipX, shipY, shipX + 6, shipY - 20, fill='black')
def movement(event):
    global text_val
    global shipX
    global shipY
    text_val = []
    x = event.keysym
    shipX = event.x
    shipY = event.y + 10
    newxy = [(shipX, shipY), (shipX + 20, shipY + 10), (shipX, shipY - 40), (shipX - 20, shipY + 10)]
    text_val = newxy
    c.coords(player_ship, *newxy)
    c.itemconfig(debug_text, text=text_val)
#root.event_generate()
def bullet(x1, y1):
    global bullet_dict
    c.create_rectangle(x1, y1, x1 + 6, y1 - 20, fill='black')
    bullet_dict.append([x1, y1])
    #print(bullet_dict)


def shoot(event):
    global bullet_dict
    x1 = event.x
    y1 = event.y
    c.create_rectangle(x1, y1, x1 + 6, y1 - 20, fill='black')
    bullet_dict.append([x1, y1])


#c.bind("<Motion>", movement)
bullet_dict = []

while True:
    root.update_idletasks()
    root.update()

    # reinitialize the canvas object after deleting it below
    c = Canvas(root, width=root.winfo_width(), height=root.winfo_height())
    c.place(x=0)  # recreate canvas after deleting below
    c.bind("<Button-1>", shoot)
    mX, mY = mouse.get_position()
    shipX = c.canvasx(screenx=mX) - root.winfo_x() - 8
    shipY = c.canvasy(screeny=mY) - root.winfo_y() - 17
    xy = [(shipX, shipY), (shipX + 20, shipY + 10), (shipX, shipY - 40), (shipX - 20, shipY + 10)]


    if len(bullet_dict) is not None:
        for n in bullet_dict:
            print(bullet_dict)
            if n[1] <= 0:
                bullet_dict.remove(n)
            elif n[1] > 0:
                n[1] -= 15
                print(bullet_dict)
                c.create_rectangle(n[0], n[1], n[0]+6, n[1]-20, fill='black')
            else:
                print("Something's wrong, where's the bullet?")

    player_ship = c.create_polygon(xy)
    debug_text = c.create_text(1, 1, anchor=tkinter.NW)

    #print(mouse.ButtonEvent)

    time.sleep(.01)  # keeps frame rate at 60 fps (because all the physics and movement is based on the framerate)
    # clears the canvas to reset the frame for the next frame
    c.delete()

