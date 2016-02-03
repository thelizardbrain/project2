import pygame, sys
from pygame.locals import *
from players import *
import random
import time

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
def fight_animation():
    fight_image1 = pygame.image.load('fight1.png')
    fight_image2 = pygame.image.load('fight2.png')
    fight_image3 = pygame.image.load('fight3.png')
    fightsound = pygame.mixer.Sound('fight.wav')


    fightsound.play()
    pygame.display.flip()
    DISPLAYSURF.blit(fight_image1,(500,250))
    pygame.display.flip()
    time.sleep(0.1)
    DISPLAYSURF.blit(fight_image2,(500,250))
    pygame.display.flip()
    time.sleep(0.1)
    DISPLAYSURF.blit(fight_image3,(500,250))
    time.sleep(5)
def tile_fight():
    if rPx == bPx and rPy == bPy or rPx == grPx and rPy == grPy  or rPx == gPx and rPy == gPy or bPx == grPx \
            and bPy == grPy or bPx == gPx and bPy == gPy or grPx == gPx and grPy == gPy:
        fight_animation()+

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
DISPLAYSURF = pygame.display.set_mode((1200, 750))
screen_rect = DISPLAYSURF.get_rect()

dice_sheet = pygame.image.load('dice.png')
dice = strip_from_sheet(dice_sheet, (0,0), (36,36), 1, 6)

image = pygame.Surface([0, 0]).convert()
btn = Button(screen_rect)


midPic = pygame.image.load('Midden van bord oud.png')
backPic = pygame.image.load('Hout2.png')
roodPion = pygame.image.load('glove_red.png')
roodscore = pygame.image.load('red_score.png')
rPx = 950
rPy = 100
rDirection = 'down'
blauwPion = pygame.image.load('glove_blue.png')
blauwscore = pygame.image.load('blue_score.png')
bPx = 450
bPy = 100
bDirection = 'right'
groenPion = pygame.image.load('glove_green.png')
groenscore = pygame.image.load('green_score.png')
grPx = 950
grPy = 600
grDirection = 'left'
geelPion = pygame.image.load('glove_yellow.png')
geelscore = pygame.image.load('yellow_score.png')
gPx = 450
gPy = 600
gDirection = 'up'
DISPLAYSURF.blit(pygame.transform.scale(backPic, (750, 750)), (350, 0))
shade = pygame.image.load('zwart.png')
DISPLAYSURF.blit(pygame.transform.scale(shade, (555, 5)), (450, 650))
DISPLAYSURF.blit(pygame.transform.scale(shade, (555, 5)), (450, 95))
DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 560)), (445, 95))
DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 550)), (1000, 100))
fight = pygame.image.load('fight.png')
fightx1 = 700
fighty1 = 100
fightx2 = 450
fighty2 = 350
fightx3 = 950
fighty3 = 600

turn = 'playerOne'

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if btn.rect.collidepoint(pygame.mouse.get_pos()):
                list = [1,2,3,4,5,6,7]
                rand = random.randint(0,5)
                image = dice[rand]
                grand = rand + 1
                ggrand = grand + 1

                if turn == 'playerOne':
                    DISPLAYSURF.blit(pygame.transform.scale(blauwscore, (350, 450)), (0, 300))
                    tile_fight()
                    if bDirection == 'right':
                        for i in list[:grand]:
                            if bPx == 950:
                                bDirection = 'down'
                                for n in list[i:ggrand]:
                                    bPy += 50
                                break
                            else:
                                bPx += 50
                        turn = 'playerTwo'
                    elif bDirection == 'down':
                        for i in list[:grand]:
                            if bPy == 600:
                                bDirection = 'left'
                                for n in list[i:ggrand]:
                                    bPx -= 50
                                break
                            else:
                                bPy += 50
                        turn = 'playerTwo'
                    elif bDirection == 'left':
                        for i in list[:grand]:
                            if bPx == 450:
                                bDirection = 'up'
                                for n in list[i:ggrand]:
                                    bPy -= 50
                                break
                            else:
                                bPx -= 50
                        turn = 'playerTwo'
                    elif bDirection == 'up':
                        for i in list[:grand]:
                            if bPy == 100:
                                bDirection = 'right'
                                for n in list[i:ggrand]:
                                    bPx += 50
                                break
                            else:
                                bPy -= 50
                        turn = 'playerTwo'


                elif turn == 'playerTwo':
                    DISPLAYSURF.blit(pygame.transform.scale(roodscore, (350, 450)), (0, 300))
                    tile_fight()
                    if rDirection == 'right':
                        for i in list[:grand]:
                            if rPx == 950:
                                rDirection = 'down'
                                for n in list[i:ggrand]:
                                    rPy += 50
                                break
                            else:
                                rPx += 50
                        turn = 'playerThree'
                    elif rDirection == 'down':
                        for i in list[:grand]:
                            if rPy == 600:
                                rDirection = 'left'
                                for n in list[i:ggrand]:
                                    rPx -= 50
                                break
                            else:
                                rPy += 50
                        turn = 'playerThree'
                    elif rDirection == 'left':
                        for i in list[:grand]:
                            if rPx == 450:
                                rDirection = 'up'
                                for n in list[i:ggrand]:
                                    rPy -= 50
                                break
                            else:
                                rPx -= 50
                        turn = 'playerThree'
                    elif rDirection == 'up':
                        for i in list[:grand]:
                            if rPy == 100:
                                rDirection = 'right'
                                for n in list[i:ggrand]:
                                    rPx += 50
                                break
                            else:
                                rPy -= 50
                        turn = 'playerThree'


                elif turn == 'playerFour':
                    DISPLAYSURF.blit(pygame.transform.scale(geelscore, (350, 450)), (0, 300))
                    tile_fight()
                    if gDirection == 'right':
                        for i in list[:grand]:
                            if gPx == 950:
                                gDirection = 'down'
                                for n in list[i:ggrand]:
                                    gPy += 50
                                break
                            else:
                               gPx += 50
                        turn = 'playerOne'
                    elif gDirection == 'down':
                        for i in list[:grand]:
                            if gPy == 600:
                                gDirection = 'left'
                                for n in list[i:ggrand]:
                                    gPx -= 50
                                break
                            else:
                                gPy += 50
                        turn = 'playerOne'
                    elif gDirection == 'left':
                        for i in list[:grand]:
                            if gPx == 450:
                                gDirection = 'up'
                                for n in list[i:ggrand]:
                                    gPy -= 50
                                break
                            else:
                                gPx -= 50
                        turn = 'playerOne'
                    elif gDirection == 'up':
                        for i in list[:grand]:
                            if gPy == 100:
                                gDirection = 'right'
                                for n in list[i:ggrand]:
                                    gPx += 50
                                break
                            else:
                                gPy -= 50
                        turn = 'playerOne'


                elif turn == 'playerThree':
                    DISPLAYSURF.blit(pygame.transform.scale(groenscore, (350, 450)), (0, 300))
                    tile_fight()
                    if grDirection == 'right':
                        for i in list[:grand]:
                            if grPx == 950:
                                grDirection = 'down'
                                for n in list[i:ggrand]:
                                    grPy += 50
                                break
                            else:
                                grPx += 50
                        turn = 'playerFour'
                    elif grDirection == 'down':
                        for i in list[:grand]:
                            if grPy == 600:
                                grDirection = 'left'
                                for n in list[i:ggrand]:
                                    grPx -= 50
                                break
                            else:
                                grPy += 50
                        turn = 'playerFour'
                    elif grDirection == 'left':
                        for i in list[:grand]:
                            if grPx == 450:
                                grDirection = 'up'
                                for n in list[i:ggrand]:
                                    grPy -= 50
                                break
                            else:
                                grPx -= 50
                        turn = 'playerFour'
                    elif grDirection == 'up':
                        for i in list[:grand]:
                            if grPy == 100:
                                grDirection = 'right'
                                for n in list[i:ggrand]:
                                    grPx += 50
                                break
                            else:
                                grPy -= 50
                        turn = 'playerFour'

    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            pygame.draw.rect(DISPLAYSURF, colours[tilemap[row][column]], (450 + column*TILESIZE, 100 + row*TILESIZE, TILESIZE, TILESIZE))
    DISPLAYSURF.blit(pygame.transform.scale(midPic, (450, 450)), (500, 150))
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