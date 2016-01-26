import pygame, sys
from pygame.locals import *
from players import *

#constants representing colours
YELLOW = (255, 255, 102)
ANDERSGEEL = (204, 204, 0)
RED = (201, 57, 57)
ANDERSROOD = (153, 0, 0)
GREEN = (102,   204, 0  )
ANDERSGROEN = (0, 102, 0)
BLUE = (0,   102,   205)
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
                ANDERSBLAUWVAK : ANDERSBLAUW
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
FPS = 5
MAINCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((750, 750))
midPic = pygame.image.load('Midden van bord.png').convert()
backPic = pygame.image.load('Hout2.png').convert()
DISPLAYSURF.blit(pygame.transform.scale(backPic, (750, 750)), (0, 0))
roodPion = pygame.image.load('glove_red.png')
rPx = 600
rPy = 100
rDirection = 'down'
blauwPion = pygame.image.load('glove_blue.png')
bPx = 100
bPy = 100
bDirection = 'right'
groenPion = pygame.image.load('glove_green.png')
grPx = 600
grPy = 600
grDirection = 'left'
geelPion = pygame.image.load('glove_yellow.png')
gPx = 100
gPy = 600
gDirection = 'up'
shade = pygame.image.load('zwart.png').convert()
DISPLAYSURF.blit(pygame.transform.scale(shade, (550, 5)), (105, 650))
DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 550)), (650, 100))
fight = pygame.image.load('fight.png').convert()
fightx1 = 350
fighty1 = 100
fightx2 = 100
fighty2 = 350
fightx3 = 600
fighty3 = 600

# turn = random.choice(['playerOne', 'playerTwo', 'playerThree', 'playerFour'])
turn = 'playerOne'

while True:
    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            pygame.draw.rect(DISPLAYSURF, colours[tilemap[row][column]], (100 + column*TILESIZE, 100 + row*TILESIZE, TILESIZE, TILESIZE))
            DISPLAYSURF.blit(pygame.transform.scale(midPic, (450, 450)), (150, 150))
            DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx1, fighty1))
            DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx2, fighty2))
            DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx1, fighty3))
            DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx3, fighty2))
            DISPLAYSURF.blit(pygame.transform.scale(roodPion, (50, 50)), (rPx, rPy))
            DISPLAYSURF.blit(pygame.transform.scale(blauwPion, (50, 50)), (bPx, bPy))
            DISPLAYSURF.blit(pygame.transform.scale(geelPion, (50, 50)), (gPx, gPy))
            DISPLAYSURF.blit(pygame.transform.scale(groenPion, (50, 50)), (grPx, grPy))

    if turn == 'playerOne':
        if bDirection == 'right':
            bPx += 50
            if bPx == 600:
                bDirection = 'down'
            turn = 'playerTwo'
        elif bDirection == 'down':
            bPy += 50
            if bPy == 600:
                bDirection = 'left'
            turn = 'playerTwo'
        elif bDirection == 'left':
            bPx -= 50
            if bPx == 100:
                bDirection = 'up'
            turn = 'playerTwo'
        elif bDirection == 'up':
            bPy -= 50
            if bPy == 100:
                bDirection = 'right'
            turn = 'playerTwo'


    elif turn == 'playerTwo':
        if rDirection == 'right':
            rPx += 50
            if rPx == 600:
                rDirection = 'down'
            turn = 'playerThree'
        elif rDirection == 'down':
            rPy += 50
            if rPy == 600:
                rDirection = 'left'
            turn = 'playerThree'
        elif rDirection == 'left':
            rPx -= 50
            if rPx == 100:
                rDirection = 'up'
            turn = 'playerThree'
        elif rDirection == 'up':
            rPy -= 50
            if rPy == 100:
                rDirection = 'right'
            turn = 'playerThree'


    elif turn == 'playerThree':
        if gDirection == 'right':
            gPx += 50
            if gPx == 600:
                gDirection = 'down'
            turn = 'playerFour'
        elif gDirection == 'down':
            gPy += 50
            if gPy == 600:
                gDirection = 'left'
            turn = 'playerFour'
        elif gDirection == 'left':
            gPx -= 50
            if gPx == 100:
                gDirection = 'up'
            turn = 'playerFour'
        elif gDirection == 'up':
            gPy -= 50
            if gPy == 100:
                gDirection = 'right'
            turn = 'playerFour'


    else:
        if grDirection == 'right':
            grPx += 50
            if grPx == 600:
                grDirection = 'down'
            turn = 'playerOne'
        elif grDirection == 'down':
            grPy += 50
            if grPy == 600:
                grDirection = 'left'
            turn = 'playerOne'
        elif grDirection == 'left':
            grPx -= 50
            if grPx == 100:
                grDirection = 'up'
            turn = 'playerOne'
        elif grDirection == 'up':
            grPy -= 50
            if grPy == 100:
                grDirection = 'right'
            turn = 'playerOne'


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    MAINCLOCK.tick(FPS)
    pygame.display.update()