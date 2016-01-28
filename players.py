import pygame
import random


class players:
    def __init__(self, playercolor):
        self.damage = []
        self.condition = []
        self.Color = playercolor
        self.number = " "

        if playercolor == "blue":
            self.scards = "mike tysen.png"
            self.number = 1
            self.position = " "
            self.hpoints = 100
            self.cpoints = 15

        elif playercolor == "red":
            self.scards = "manny pecquiao.png"
            self.number = 2
            self.position = " "
            self.hpoints = 100
            self.cpoints = 15

        elif playercolor == "green":
            self.scards = "rocky belboa.png"
            self.number = 3
            self.position = " "
            self.hpoints = 100
            self.cpoints = 1500

        elif playercolor == "yellow":
            self.scards = "bedr hari.png"
            self.number = 4
            self.position = " "
            self.hpoints = 100
            self.cpoints = 15

    def scards(self):
        self.playercolor = "yellow", pygame.image.load("bedr hari.png")
        self.playercolor = "blue", pygame.image.load("mike tysen.png")
        self.playercolor = "green", pygame.image.load("rocky belboa.png")
        self.playercolor = "red", pygame.image.load("manny pecquiao.png")

    def cpoints(self):
        self.image = "stamina.png"
        self.cpoints = 15


    def hpoints(self):
        self.image = "health points.png"
        self.hpoints = 100

    def changeHpoints(self, damage):
        self.hpoints -= damage

    def changeCpoins(self, condition):
        self.cpoints -= condition


