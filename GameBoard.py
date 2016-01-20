import pygame, sys
from pygame .locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1150, 700))
pygame.display.set_caption('Survivor')
backPic = pygame.image.load('Oak.jpg')
DISPLAYSURF.blit(pygame.transform.scale(backPic, (1150, 700)), (0, 0))
pic = pygame.image.load("Bord.png")
pygame.display.flip()

Greensqr = pygame.image.load("BoardGame Greensquare")
Bluesquare = pygame.image.load("BoardGame Bluesquare")
yellowrect = pygame.image.load("BoardGame Yellowsquare")
redsquare = pygame.image.load("BoardGame Redsquare")
greyrect = pygame.image.load("BoardGame greyrect")
whiterect = pygame.image.load("BoardGame whiterect")
fightrect = pygame.image.load("BoardGame fightrect")
bluerect = pygame.image.load("BoardGame bluerect")
redrect = pygame.image.load("BoardGame redrect")
greenrect = pygame.image.load("BoardGame greenrect")
yellowrect = pygame.image.load("BoardGame yellowrect")




while True:
    DISPLAYSURF.blit(pygame.transform.scale(pic, (950, 575)), (0, 0))
# main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
