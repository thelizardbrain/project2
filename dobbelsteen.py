import pygame as pg, sys
from pygame.locals import *
import random

class Button:
    def __init__(self, screen_rect):
        self.image = pg.Surface([100,50]).convert()
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center=screen_rect.center)
    def render(self, surf):
        surf.blit(self.image, self.rect)

def strip_from_sheet(sheet, start, size, columns, rows=1):
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(sheet.subsurface(pg.Rect(location, size)))
    return frames

pg.init()
screen = pg.display.set_mode((800,600))
screen_rect = screen.get_rect()


dice_sheet = pg.image.load('dice.png')
dice = strip_from_sheet(dice_sheet, (0,0), (36,36), 1, 6)



image = pg.Surface([0,0]).convert()
btn = Button(screen_rect)
done = False
while not done:
    screen.fill((0,0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if btn.rect.collidepoint(pg.mouse.get_pos()):
                rand = random.randint(0,5)
                image = dice[rand]
                print(rand + 1)

    screen.blit(image, (500,100))
    btn.render(screen)
    pg.display.update()

