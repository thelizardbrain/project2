import pygame, sys
from pygame.locals import *

#constants representing colours
YELLOW = (255, 255, 102)
ANDERSGEEL = (204, 204, 0)
RED = (201, 57, 57)
ANDERSROOD = (153, 0, 0)
GREEN = (102,   204, 0  )
ANDERSGROEN = (0, 102, 0)
BLUE  = (0,   102,   205)
ANDERSBLAUW = (0, 51, 102)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (224, 224, 224)



#constants representing the different resources
ROODVAK  = 0
GROENVAK = 1
BLAUWVAK = 2
GEELVAK  = 3
WITVAK = 4
GRIJSVAK = 5
ZWARTVAK = 6
ANDERSGROENVAK = 7
ANDERSGEELVAK = 8
ANDERSROODVAK = 9
ANDERSBLAUWVAK = 10


#a dictionary linking resources to colours
colours =   {
                ROODVAK  : RED,
                GROENVAK : GREEN,
                BLAUWVAK : BLUE,
                GEELVAK  : YELLOW,
                WITVAK : WHITE,
                GRIJSVAK : GREY,
                ZWARTVAK : BLACK,
                ANDERSGROENVAK : ANDERSGROEN,
                ANDERSGEELVAK : ANDERSGEEL,
                ANDERSROODVAK : ANDERSROOD,
                ANDERSBLAUWVAK : ANDERSBLAUW,
            }

#a list representing our tilemap
tilemap = [
            [ANDERSBLAUWVAK, BLAUWVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, ROODVAK, ANDERSROODVAK],
            [BLAUWVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ROODVAK],
            [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
            [WITVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, WITVAK],
            [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
            [WITVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, WITVAK],
            [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
            [WITVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, WITVAK],
            [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
            [GEELVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GROENVAK],
            [ANDERSGEELVAK, GEELVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, GROENVAK, ANDERSGROENVAK]
          ]

#useful game dimensions
TILESIZE  = 50
MAPWIDTH  = 11
MAPHEIGHT = 11

#set up the display
pygame.init()
# DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))
DISPLAYSURF = pygame.display.set_mode((675, 650))
backPic = pygame.image.load('Oak.jpg')
DISPLAYSURF.blit(pygame.transform.scale(backPic, (675, 650)), (0, 0))
fight = pygame.image.load('fight.png')
fightx1 = 250
fighty1 = 1
fightx2 = 0
fighty2 = 250
fightx3 = 500
fighty3 = 500
while True:
    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            #and the game and close the window
            pygame.quit()
            sys.exit()

    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            pygame.draw.rect(DISPLAYSURF, colours[tilemap[row][column]], (column*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))
            DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx1, fighty1))
            DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx2, fighty2))
            DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx1, fighty3))
            DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx3, fighty2))
    #update the display
    pygame.display.update()