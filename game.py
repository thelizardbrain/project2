import pygame, sys
from pygame.locals import *
pygame.init()


display = pygame.display.set_mode((800,600)) # basis framework
caption = pygame.display.set_caption('Survivor')
fps = pygame.time.Clock()
logoIMG=pygame.image.load('logo.png')
black = (0,0,0)
white = (255,255,255)


def logo(x,y):
    display.blit(logoIMG,(x,y))

x = (800 * 0.22)
y = (600 * 0.2)


while True: # game loop
     for event in pygame.event.get():
         if event.type == QUIT:
           pygame.quit()
           sys.exit()
     display.fill (white)
     logo(x,y)
     pygame.display.flip()
     fps.tick()



pygame.quit()
quit()
