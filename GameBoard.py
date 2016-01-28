import pygame, sys
from pygame.locals import *
from players import *
import random

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
class Button:
    def __init__(self, screen_rect):
        self.image = pygame.Surface([100, 50]).convert()
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center=screen_rect.center)
    def render(self, surf):
        surf.blit(self.image, self.rect)

def strip_from_sheet(sheet, start, size, columns, rows=1):
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(sheet.subsurface(pygame.Rect(location, size)))
    return frames

pygame.init()
DISPLAYSURF = pygame.display.set_mode((850, 750))
screen_rect = DISPLAYSURF.get_rect()


dice_sheet = pygame.image.load('dice.png')
dice = strip_from_sheet(dice_sheet, (0,0), (36,36), 1, 6)



image = pygame.Surface([0, 0]).convert()
btn = Button(screen_rect)


midPic = pygame.image.load('Midden van bord.png')
backPic = pygame.image.load('Hout2.png')
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
DISPLAYSURF.blit(pygame.transform.scale(backPic, (750, 750)), (0, 0))
shade = pygame.image.load('zwart.png')
DISPLAYSURF.blit(pygame.transform.scale(shade, (550, 5)), (105, 650))
DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 550)), (650, 100))
fight = pygame.image.load('fight.png')
fightx1 = 350
fighty1 = 100
fightx2 = 100
fighty2 = 350
fightx3 = 600
fighty3 = 600

turn = 'playerOne'

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if btn.rect.collidepoint(pygame.mouse.get_pos()):
                list = [1,2,3,4,5,6]
                rand = random.randint(0,5)
                image = dice[rand]
                grand = rand + 1
                print(grand)

                if turn == 'playerOne':
                    if bDirection == 'right':
                        for i in list[:grand]:
                            bPx += 50
                            if bPx == 600:
                                bDirection = 'down'
                                break
                        turn = 'playerTwo'
                    elif bDirection == 'down':
                        for i in list[:grand]:
                            bPy += 50
                            if bPy == 600:
                                bDirection = 'left'
                                break
                        turn = 'playerTwo'
                    elif bDirection == 'left':
                        for i in list[:grand]:
                            bPx -= 50
                            if bPx == 100:
                                bDirection = 'up'
                                break
                        turn = 'playerTwo'
                    elif bDirection == 'up':
                        for i in list[:grand]:
                            bPy -= 50
                            if bPy == 100:
                                bDirection = 'right'
                                break
                        turn = 'playerTwo'


                elif turn == 'playerTwo':
                    if rDirection == 'right':
                        for i in list[:grand]:
                            rPx += 50
                            if rPx == 600:
                                rDirection = 'down'
                                break
                        turn = 'playerThree'
                    elif rDirection == 'down':
                        for i in list[:grand]:
                            rPy += 50
                            if rPy == 600:
                                rDirection = 'left'
                                break
                        turn = 'playerThree'
                    elif rDirection == 'left':
                        for i in list[:grand]:
                            rPx -= 50
                            if rPx == 100:
                                rDirection = 'up'
                                break
                        turn = 'playerThree'
                    elif rDirection == 'up':
                        for i in list[:grand]:
                            rPy -= 50
                            if rPy == 100:
                                rDirection = 'right'
                                break
                        turn = 'playerThree'


                elif turn == 'playerThree':
                    if gDirection == 'right':
                        for i in list[:grand]:
                            gPx += 50
                            if gPx == 600:
                                gDirection = 'down'
                                break
                        turn = 'playerFour'
                    elif gDirection == 'down':
                        for i in list[:grand]:
                            gPy += 50
                            if gPy == 600:
                                gDirection = 'left'
                                break
                        turn = 'playerFour'
                    elif gDirection == 'left':
                        for i in list[:grand]:
                            gPx -= 50
                            if gPx == 100:
                                gDirection = 'up'
                                break
                        turn = 'playerFour'
                    elif gDirection == 'up':
                        for i in list[:grand]:
                            gPy -= 50
                            if gPy == 100:
                                gDirection = 'right'
                                break
                        turn = 'playerFour'


                elif turn == 'playerFour':
                    if grDirection == 'right':
                        for i in list[:grand]:
                            grPx += 50
                            if grPx == 600:
                                grDirection = 'down'
                                break
                        turn = 'playerOne'
                    elif grDirection == 'down':
                        for i in list[:grand]:
                            grPy += 50
                            if grPy == 600:
                                grDirection = 'left'
                                break
                        turn = 'playerOne'
                    elif grDirection == 'left':
                        for i in list[:grand]:
                            grPx -= 50
                            if grPx == 100:
                                grDirection = 'up'
                                break
                        turn = 'playerOne'
                    elif grDirection == 'up':
                        for i in list[:grand]:
                            grPy -= 50
                            if grPy == 100:
                                grDirection = 'right'
                                break
                        turn = 'playerOne'

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


    DISPLAYSURF.blit(image, (781,680))
    btn.render(DISPLAYSURF)
    pygame.display.update()