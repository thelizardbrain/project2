import pygame
import random

class players:
    def __init__(self, playercolor):
        self.damage = []
        self.condition = []
        self.Color = playercolor
        self.number = " "


        if playercolor == "blue":
            self.scards = random.scards
            self.number = 1
            self.position = " "

        elif playercolor == "red":
            self.scards = random.scards
            self.number = 2
            self.position = " "

        elif playercolor == "green":
            self.scards = random.scards
            self.number = 3
            self.position = " "

        elif playercolor == "yellow":
            self.scards = random.scards
            self.number = 4
            self.position = " "

    def scards (self, scorecard):
        self.scorecard1 = "mike tysen.png"
        self.scorecard2 = "rocky belboa.png"
        self.scorecard3 = "bedr heri.png"
        self.scorecard4 = "manny pecquiao.png"
