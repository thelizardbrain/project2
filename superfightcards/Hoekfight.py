import webbrowser, os
import pygame, sys
from pygame.locals import *
import time
import random
pygame.init()


if (bPy == 100, 900 <= bPx <= 950) or (bPy == 150, bPx == 950):
    hp_damage = hp2
    cnd_cost = cnpt1
elif (bPy == 600, 900 <= bPx <= 950) or (bPy == 550, bPx == 950):
    hp_damage = hp3
    cnd_cost = cnpt1
elif (bPy == 600, 400 <= bPx <= 450) or (bPy == 550, bPx == 450):
    hp_damage = hp4
    cnd_cost = cnpt1
elif (bPy == 100, 450 <= bPx <= 500) or (bPy == 150, bPx == 450):
    cnpt1 = 15
    if hp1 < 91:
        hp1 += 10
    else:
        hp1 = 100

def Hoekfight1():
    if rand == 1:
        #button1
            if click[0] == 1:
                hp_damage -= 3
                cpnt1 -= 1
        #button2
            if click[0] == 1:
                hp_damage -= 9
                cpnt1 -= 2
        #button3
            if click[0] == 1:
                hp_damage -= 19
                cpnt1 -=3
    elif rand == 2:
        #button1
            if click[0] == 1:
                hp_damage -= 5
                cpnt1 -= 2
        #button2
            if click[0] == 1:
                hp_damage -= 11
                cpnt -= 3
        #button3
            if click[0] == 1:
                hp_damage -= 15
                cpnt1 -=5
    elif rand == 3:
        #button1
            if click[0] == 1:
                hp_damage -= 7
                cpnt1 -= 2
        #button2
            if click[0] == 1:
                hp_damage -= 12
                cpnt1 -= 3
        #button3
            if click[0] == 1:
                hp_damage -= 16
                cpnt1 -= 4
    elif rand == 4:
        #button1
            if click[0] == 1:
                hp_damage -= 2
                cpnt1 -= 1
        #button2
            if click[0] == 1:
                hp_damage -= 4
                cpnt1 -= 2
        #button3
            if click[0] == 1:
                hp_damage -= 6
                cpnt1 -= 3
    elif rand == 5:
        #button1
            if click[0] == 1:
                hp_damage -= 10
                cpnt1 -= 2
        #button2
            if click[0] == 1:
                hp_damage -= 20
                cpnt1 -= 5
        #button3
            if click[0] == 1:
                hp_damage -= 30
                cpnt -= 8
    elif rand == 6:
        #button1
            if click[0] == 1:
                hp_damage -= 8
                cpnt1 -= 3
        #button2
            if click[0] == 1:
                hp_damage -= 13
                cpnt1 -= 4
        #button3
            if click[0] == 1:
                hp_damage -= 17
                cpnt -= 5


if turn == "playerTwo" and (bPy == 100, 900 <= bPx <= 950) or (bPy == 150, bPx == 950):
    cnpt2 = 15
    if hp2 < 91:
        hp2 += 10
    else:
        hp2 = 100
elif (bPy == 600, 900 <= bPx <= 950) or (bPy == 550, bPx == 950):
    hp_damage = hp3
    cnd_cost = cnpt2
elif (bPy == 600, 450 <= bPx <= 500) or (bPy == 550, bPx == 450):
    hp_damage = hp4
    cnd_cost = cnpt2
elif (bPy == 100, 450 <= bPx <= 500) or (bPy == 150, bPx == 450):
    hp_damage = hp1
    cnd_cost = cnpt2
def Hoekfight2():
    if rand == 1:
        #button1
            if click[0] == 1:
                hp_damage -= 10
                cnd_cost -= 2
        #button2
            if click[0] == 1:
                hp_damage -= 20
                cnd_cost -= 5
        #button3
            if click[0] == 1:
                hp_damage -= 30
                cnd_cost -= 8
    elif rand == 2:
        #button1
            if click[0] == 1:
                hp_damage -= 8
                cnd_cost -= 3
        #button2
            if click[0] == 1:
                hp_damage -= 13
                cnd_cost -= 4
        #button3
            if click[0] == 1:
                hp_damage -= 13
                cnd_cost -= 17
    elif rand == 3:
        #button1
            if click[0] == 1:
                hp_damage -= 3
                cnd_cost -= 1
        #button2
            if click[0] == 1:
                hp_damage -= 9
                cnd_cost -= 2
        #button3
            if click[0] == 1:
                hp_damage -= 19
                cnd_cost -= 3
    elif rand == 4:
        #button1
            if click[0] == 1:
                hp_damage -= 5
                cnd_cost -= 2
        #button2
            if click[0] == 1:
                hp_damage -= 11
                cnd_cost -= 3
        #button3
            if click[0] == 1:
                hp_damage -= 15
                cnd_cost -= 5
    elif rand == 5:
        #button1
            if click[0] == 1:
                hp_damage -= 7
                cnd_cost -= 2
        #button2
            if click[0] == 1:
                hp_damage -= 12
                cnd_cost -= 3
        #button3
            if click[0] == 1:
                hp_damage -= 16
                cnd_cost -= 4
    elif rand == 6:
        #button1
            if click[0] == 1:
                hp_damage -= 2
                cnd_cost -= 1
        #button2
            if click[0] == 1:
                hp_damage -= 4
                cnd_cost -= 2
        #button3
            if click[0] == 1:
                hp_damage -= 6
                cnd_cost -= 3
