import pygame , sys
from pygame .locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1150, 700))
pygame.display.set_caption('Survivor')
backPic = pygame.image.load('Oak.jpg')
DISPLAYSURF.blit(pygame.transform.scale(backPic, (1150, 700)), (0, 0))
pic = pygame.image.load("Bord.png")
pygame.display.flip()

while True:
    DISPLAYSURF.blit(pygame.transform.scale(pic, (950, 575)), (0, 0))
# main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
