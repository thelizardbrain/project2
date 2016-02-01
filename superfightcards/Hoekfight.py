import webbrowser, os
import pygame, sys
from pygame.locals import *
import time
import random
pygame.init()


if turn == "playerOne" and (bPy == 100 and 900 <= bPx <= 950) or (bPy == 150 and bPx == 950):
    hp_damage = hp2
elif turn == "playerOne" and (bPy == 600 and 900 <= bPx <= 950) or (bPy == 550 and bPx == 950):
    hp_damage = hp3
elif turn == "playerOne" and (bPy == 600 and 400 <= bPx <= 450) or (bPy == 550 and bPx == 450):
    hp_damage = hp4

def Hoekfight():
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