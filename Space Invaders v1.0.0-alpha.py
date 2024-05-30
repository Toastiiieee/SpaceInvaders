import time
from tkinter import *
import tkinter

root = Tk()
c = Canvas(width=800, height=800)
c.grid()

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


def initiate_game():
    global enemies
    global right_moves
    global moving_right
    global enemy_speed
    global bullet_dict
    global move_time
    global shipX
    global shipY
    shipX = 400
    shipY = 700
    move_time = time.time_ns()
    bullet_dict = []
    right_moves = 0
    moving_right = True
    enemy_speed = 1000000000
    enemies = [[140, 100],
               [220, 100],
               [300, 100],
               [380, 100],
               [460, 100],
               [540, 100],
               [620, 100],
               [140, 160],
               [220, 160],
               [300, 160],
               [380, 160],
               [460, 160],
               [540, 160],
               [620, 160],
               [140, 220],
               [220, 220],
               [300, 220],
               [380, 220],
               [460, 220],
               [540, 220],
               [620, 220]]
    frame.destroy()


def leave():
    root.destroy()


def spawn_enemy(x, y):
    c.create_rectangle(x, y, x + 40, y - 40)
    c.create_line(x + 10, y - 30, x + 10, y - 20)
    c.create_line(x + 8, y - 32, x + 13, y - 27)
    c.create_line(x + 30, y - 30, x + 30, y - 20)
    c.create_line(x + 32, y - 32, x + 27, y - 27)
    c.create_line(x + 15, y - 15, x + 26, y - 15)


move_time = time.time_ns()
bullet_dict = []
enemies = [[140, 100],
           [220, 100],
           [300, 100],
           [380, 100],
           [460, 100],
           [540, 100],
           [620, 100],
           [140, 160],
           [220, 160],
           [300, 160],
           [380, 160],
           [460, 160],
           [540, 160],
           [620, 160],
           [140, 220],
           [220, 220],
           [300, 220],
           [380, 220],
           [460, 220],
           [540, 220],
           [620, 220]]


right_moves = 0
moving_right = True
enemy_speed = 1000000000

while True:
    root.update_idletasks()
    root.update()

    # reinitialize the canvas object after deleting it below
    c = Canvas(root, width=root.winfo_width(), height=root.winfo_height())
    c.place(x=0)  # recreate canvas after deleting below

    xy = [(shipX, shipY), (shipX + 20, shipY + 10), (shipX, shipY - 40), (shipX - 20, shipY + 10)]

    c.bind("<ButtonPress-1>", mouse_is_clicked)
    c.bind("<ButtonRelease-1>", mouse_isnt_clicked)
    c.bind_all("<KeyPress>", keyboardDown)
    c.bind_all("<KeyRelease>", keyboardUp)

    if len(enemies) != 0:
        for p in enemies:
            spawn_enemy(p[0], p[1])
        if time.time_ns() - move_time >= enemy_speed:
            if right_moves == 6:
                moving_right = False
            if right_moves == -6:
                moving_right = True
            for p in enemies:
                if right_moves < 6 and moving_right:
                    if right_moves == -6:
                        p[1] += 15
                        enemy_speed -= 5000000
                    else:
                        p[0] += 5
                elif right_moves > -6 and moving_right is not True:
                    if right_moves == 6:
                        p[1] += 15
                        enemy_speed -= 5000000
                    else:
                        p[0] -= 5
            move_time = time.time_ns()
            print(right_moves)
            if moving_right:
                right_moves += 1
            else:
                right_moves -= 1
    else:
        frame = tkinter.Frame(root, padx=3, pady=12)
        frame.grid(column=0, row=0)
        tkinter.Label(master=frame, text="Game Over!").grid(column=3, row=2)
        tkinter.Button(master=frame, text='restart', command=initiate_game).grid(column=3, row=3)
        tkinter.Button(master=frame, text='close', command=leave).grid(column=3, row=4)
        root.wait_window(frame)

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
        shipY -= 7
    if playerMoveDown:
        shipY += 7
    if playerMoveRight:
        shipX += 7
    if playerMoveLeft:
        shipX -= 7

    if len(bullet_dict) is not None:
        for n in bullet_dict:
            bullet_hit = False
            if len(enemies) is not None:
                for e in enemies:
                    if n[1] in range(e[1] - 40, e[1]) and n[0] in range(e[0], e[0] + 40):
                        bullet_dict.remove(n)
                        enemies.remove(e)
                        bullet_hit = True
            if n[1] <= 0:
                bullet_dict.remove(n)
            elif n[1] > 0 and bullet_hit is not True:
                n[1] -= 20
                c.create_rectangle(n[0], n[1], n[0]+6, n[1]-20, fill='black')

    player_ship = c.create_polygon(xy)
    debug_text = c.create_text(1, 1, anchor=tkinter.NW)

    time.sleep(.01)  # keeps frame rate at 60 fps (because all the physics and movement is based on the framerate)
    # clears the canvas to reset the frame for the next frame
    c.delete()
