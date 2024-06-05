# Project: Space Invaders, by Alexa Culley
# Original program was created Monday, May 27th 2024 (05-27-2024)
# Original program was then forked into this file on 06-04-2024
# for purposes of following new criteria added to the project requirements.

import time
import random
from tkinter import *
import tkinter
import SpcInvFnct

# initialize the root and canvas,
root = Tk()
c = Canvas(width=800, height=800)
c.grid()
player_movement = SpcInvFnct.PlayerMovement()  # initialize our module's class to an object
ran = random.Random  # same for the random package

# technically this is unnecessary- this just ensures the player ship is drawn on the first frame of the game,
# but it looks cleaner if everything appears at the same time, instead of the ship appearing a split second after
shipX = 400
shipY = 700
player_ship = c.create_rectangle(shipX, shipY, shipX + 6, shipY - 20, fill='black')


class GameMngr:  # for anything that manages the game as a whole, like startup and quitting
    def initiate_game(self):  # self-explanatory, just a method to initialize (or re-initialize) the game's variables.
        global enemies
        global right_moves
        global moving_right
        global enemy_speed
        global bullet_list
        global move_time
        global shipX
        global shipY
        global lose_condition
        global cooldown
        global last_shot
        global last_enemy_shot
        global enemy_bullet_list
        global player_health
        player_health = 3
        last_enemy_shot = time.time_ns()
        enemy_bullet_list = []
        cooldown = 0
        last_shot = 0
        lose_condition = 0
        shipX = 400
        shipY = 700
        move_time = time.time_ns()
        bullet_list = []
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

    def restart_game(self):  # effectively just initialize_game(), except it also deletes the frame (see loop below)
        self.initiate_game()
        frame.destroy()

    def leave(self):  # deletes the root window, closing the application.
        root.destroy()

    def verify(self):
        quit_button = tkinter.Button(master=frame, text='are you sure?', command=game.leave).grid(column=3, row=4)

def gameover(text):
    global frame
    # frame needs to be global to allow the restart_game() function to delete it, as it's otherwise out of scope
    frame = tkinter.Frame(root, padx=3, pady=12)
    frame.grid(column=0, row=0)  # grid is just better than any sort of padding in my opinion, so I prefer it
    # create the game over text and buttons to quit or restart
    tkinter.Label(master=frame, text=text).grid(column=3, row=2)
    tkinter.Button(master=frame, text='restart', command=game.restart_game).grid(column=3, row=3)
    quit_button = tkinter.Button(master=frame, text='close', command=game.verify).grid(column=3, row=4)
    root.wait_window(frame)  # basically an "input()" function, forces the program to wait for one of the
    # buttons to be pressed before it continues. the leave method simply deletes the root window entirely,
    # so this is really mainly waiting to see if the user presses 'restart', as that only deletes the frame


def pause():
    global frame
    frame = tkinter.Frame(root, padx=3, pady=12)
    frame.grid(column=0, row=0)
    tkinter.Label(master=frame, text="Game Paused").grid(column=3, row=2)
    tkinter.Button(master=frame, text='resume', command=frame.destroy).grid(column=3, row=3)
    quit_button = tkinter.Button(master=frame, text='close', command=game.verify).grid(column=3, row=4)
    root.wait_window(frame)


# initialize the Game Manager class to an object
game = GameMngr()
game.initiate_game()  # sets up all the variables for the game to run on startup


def main():
    # initialize all the global variables
    global enemies
    global right_moves
    global moving_right
    global enemy_speed
    global bullet_list
    global move_time
    global shipX
    global shipY
    global lose_condition
    global cooldown
    global last_shot
    global last_enemy_shot
    global enemy_bullet_list
    global player_health

    while True:
        root.update_idletasks()
        root.update()
        # in a regular tkinter program, you'd end with the mainloop() function. All that function is, however, is the 3
        # lines above- a simple while True loop to keep the whole process updating. What I've done is hijack that loop
        # so that everything remains updating, while also allowing me to draw and redraw frames for the game.

        c = Canvas(root, width=root.winfo_width(), height=root.winfo_height())  # overwrite the canvas to draw the next frame
        c.place(x=0)  # recreate canvas after overwriting it above

        MOVE_SPEED = 7  # constant variable to streamline the movement speed of the player's ship
        xy = [(shipX, shipY), (shipX + 20, shipY + 10), (shipX, shipY - 40), (shipX - 20, shipY + 10)]
        # list of all the vertex coordinates for the polygon that makes up the player's ship

        # bind keyboard and mouse inputs to their respective functions
        c.bind("<ButtonPress-1>", player_movement.mouse_is_down)
        c.bind("<ButtonRelease-1>", player_movement.mouse_is_up)
        c.bind_all("<KeyPress>", player_movement.keyboardDown)
        c.bind_all("<KeyRelease>", player_movement.keyboardUp)

        # iterate over all the remaining enemies and move them left, right, or down, similar to the original Space Invaders
        if len(enemies) > 0 and lose_condition < 15:
            for p in enemies:
                SpcInvFnct.spawn_enemy(c, p[0], p[1])  # draw the enemy at its current location
            if time.time_ns() - move_time >= enemy_speed:  # ensures the enemies only move based on an increment of time, not frames
                # determine if the enemies need to start moving in the other direction
                if right_moves == 4:
                    moving_right = False
                    lose_condition += 1
                if right_moves == -4:
                    moving_right = True
                    lose_condition += 1
                for p in enemies:  # iterate over every enemy and move them left, right, or down
                    if right_moves < 4 and moving_right:
                        if right_moves == -4:  # enemies only move down after a certain number of horizontal movements
                            p[1] += 15  # moves enemies down by 15 pixels
                            enemy_speed -= 5000000  # whenever the enemies move down, they speed up slightly
                        else:
                            p[0] += 5
                    elif right_moves > -4 and moving_right is not True:
                        if right_moves == 4:
                            p[1] += 15
                            enemy_speed -= 5000000
                        else:
                            p[0] -= 5
                move_time = time.time_ns()  # reset the move_time variable to keep track of movement intervals
                print(right_moves)  # print-checking for any logic errors
                if moving_right:  # keep track of the number of moves in either direction
                    right_moves += 1
                else:
                    right_moves -= 1
        elif len(enemies) == 0:
            gameover("You won!")  # call the end screen
        else:
            gameover("You lost!")

        if len(enemies) > 0:
            for p in enemies:
                if ((p[1] in range(shipY - 30, shipY) or (p[1] - 40) in range(shipY - 30, shipY))
                        and (p[0] in range(shipX - 20, shipX + 20) or (p[0] + 40) in range(shipX - 20, shipX + 20))):
                    enemies.remove(p)
                    player_health -= 1
                    print("you have", player_health, "HP remaining!")
                    if player_health == 0:
                        gameover("You died!")

        if player_movement.shooting:  # check if the player is shooting (holding down space bar or left mouse)
            # if they are, grab the ship's current position (with slight offset to keep the bullet centered)
            x1 = shipX - 3
            y1 = shipY

            # check if the weapon is on cooldown or not
            # (to limit the rate of fire, and allow the user to hold down their shoot button)
            if cooldown == 0:
                c.create_rectangle(x1, y1, x1 + 6, y1 - 20, fill='black')  # draw the bullet
                bullet_list.append([x1, y1])  # add the bullet to the bullet list to make sure its movement is tracked
                cooldown = .25  # reset the cooldown
                last_shot = time.time_ns()  # reset the last_shot variable for below

        if cooldown != 0 and time.time_ns() - last_shot >= 250000000:  # simple statement to reduce the weapon cooldown
            cooldown -= .25

        # the keyboard binding from above simplifies this step, so we just have to check what direction the player wants
        # to move (if any), and move the ship around respectively at the previously determined movespeed
        if player_movement.playerMoveUp and (shipY - 30) > 0:
            shipY -= MOVE_SPEED
        if player_movement.playerMoveDown and shipY < root.winfo_height():
            shipY += MOVE_SPEED
        if player_movement.playerMoveRight and (shipX + 15) < root.winfo_width():
            shipX += MOVE_SPEED
        if player_movement.playerMoveLeft and (shipX - 15) > 0:
            shipX -= MOVE_SPEED

        # if there's a bullet on the screen, this is meant to keep track of its movement.
        # additionally, this will also detect if a bullet has hit an enemy, and deal with it appropriately
        if len(bullet_list) > 0:
            for n in bullet_list:  # iterate over every bullet on screen
                bullet_hit = False  # effectively a Sentinel
                if len(enemies) > 0:
                    # to summarize this bit, we're just comparing the coordinates of the bullet with the coordinates
                    # of the enemies. If any overlap, it's a hit, and we kill the enemy and bullet. All the extra
                    # numbers are just to apply this idea to the full bullet, not just the bottom left corner of it
                    for e in enemies:
                        if ((n[1] in range(e[1] - 40, e[1]) or (n[1] - 20) in range(e[1] - 40, e[1]))
                                and (n[0] in range(e[0], e[0] + 40) or (n[0] + 6) in range(e[0], e[0] + 40))):
                            bullet_list.remove(n)
                            enemies.remove(e)
                            bullet_hit = True
                if n[1] <= 0:  # if the bullet misses all the enemies and travels off the screen, we delete it here
                    bullet_list.remove(n)
                # If the bullet is still on the map, and not hitting an enemy, then we deal with it here.
                # If the bullet *did* hit an enemy, though, bullet_hit would be true, and we would skip this step
                # to avoid trying to modify a nonexistent list element
                elif n[1] > 0 and bullet_hit is not True:
                    n[1] -= 20
                    c.create_rectangle(n[0], n[1], n[0]+6, n[1]-20, fill='black')

        if time.time_ns() - last_enemy_shot >= 2500000000:
            if len(enemies) > 0:
                shooter = random.choice(enemies)
                enemy_bullet = [shooter[0] + 18, shooter[1]]
                c.create_rectangle(enemy_bullet[0], enemy_bullet[1], enemy_bullet[0] + 5, enemy_bullet[1] + 20, fill='black')
                enemy_bullet_list.append(enemy_bullet)
                last_enemy_shot = time.time_ns()

        if len(enemy_bullet_list) > 0:
            for n in enemy_bullet_list:  # shipX +/- 20, shipY to shipY - 30
                if ((n[1] in range(shipY - 30, shipY) or (n[1] + 20) in range(shipY - 30, shipY))
                        and (n[0] in range(shipX - 20, shipX + 20) or (n[0] + 5) in range(shipX - 20, shipX + 20))):
                    enemy_bullet_list.remove(n)
                    player_health -= 1
                    print("you have", player_health, "HP remaining!")
                    if player_health == 0:
                        gameover("You died!")
                elif n[1] >= root.winfo_height():
                    enemy_bullet_list.remove(n)
                else:
                    n[1] += 10
                    c.create_rectangle(n[0], n[1], n[0] + 5, n[1] + 20, fill='black')

        c.create_polygon(xy)  # draw the player ship at its current position

        if player_movement.escapePressed:
            pause()

        time.sleep(.01)  # keeps frame rate at 60 fps (because all the physics and movement is based on the framerate)


if __name__ == '__main__':  # where dreams shatter and errors scream at you for missing a comma
    main()
