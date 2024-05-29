import math
import os
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

shooting = False
playerMoveDown = False
playerMoveUp = False
playerMoveRight = False
playerMoveLeft = False
last_shot = 0
cooldown = 0
shipX = 400
shipY = 700
player_ship = c.create_rectangle(shipX, shipY, shipX + 6, shipY - 20, fill='black')


def mouse_is_clicked(event):
    global shooting
    shooting = True


def keyboardDown(event):
    global playerMoveDown
    global playerMoveUp
    global playerMoveRight
    global playerMoveLeft
    global shooting
    if event.char.lower() == 'a':
        playerMoveLeft = True
    if event.char.lower() == 'd':
        playerMoveRight = True
    if event.char.lower() == 'w':
        playerMoveUp = True
    if event.char.lower() == 's':
        playerMoveDown = True
    if event.char == ' ':
        shooting = True


def keyboardUp(event):
    global playerMoveDown
    global playerMoveUp
    global playerMoveRight
    global playerMoveLeft
    global shooting
    if event.char.lower() == 'a':
        playerMoveLeft = False
    if event.char.lower() == 'd':
        playerMoveRight = False
    if event.char.lower() == 'w':
        playerMoveUp = False
    if event.char.lower() == 's':
        playerMoveDown = False
    if event.char == ' ':
        shooting = False


def mouse_isnt_clicked(event):
    global shooting
    shooting = False


bullet_dict = []

while True:
    root.update_idletasks()
    root.update()

    # reinitialize the canvas object after deleting it below
    c = Canvas(root, width=root.winfo_width(), height=root.winfo_height())
    c.place(x=0)  # recreate canvas after deleting below

    mX, mY = mouse.get_position()
    xy = [(shipX, shipY), (shipX + 20, shipY + 10), (shipX, shipY - 40), (shipX - 20, shipY + 10)]

    c.bind("<ButtonPress-1>", mouse_is_clicked)
    c.bind("<ButtonRelease-1>", mouse_isnt_clicked)
    c.bind_all("<KeyPress>", keyboardDown)
    c.bind_all("<KeyRelease>", keyboardUp)

    if shooting:
        x1 = shipX - 3
        y1 = shipY
        if cooldown == 0:
            c.create_rectangle(x1, y1, x1 + 6, y1 - 20, fill='black')
            bullet_dict.append([x1, y1])
            cooldown = .25
            last_shot = time.time_ns()

    if cooldown != 0 and time.time_ns() - last_shot >= 250000000:
        cooldown -= .25

    if playerMoveUp:
        shipY -= 8
    if playerMoveDown:
        shipY += 8
    if playerMoveRight:
        shipX += 8
    if playerMoveLeft:
        shipX -= 8

    if len(bullet_dict) is not None:
        for n in bullet_dict:
            # print(bullet_dict)
            if n[1] <= 0:
                bullet_dict.remove(n)
            elif n[1] > 0:
                n[1] -= 25
                # print(bullet_dict)
                c.create_rectangle(n[0], n[1], n[0]+6, n[1]-20, fill='black')
            else:
                print("Something's wrong, where's the bullet?")

    player_ship = c.create_polygon(xy)
    debug_text = c.create_text(1, 1, anchor=tkinter.NW)

    time.sleep(.01)  # keeps frame rate at 60 fps (because all the physics and movement is based on the framerate)
    # clears the canvas to reset the frame for the next frame
    c.delete()
