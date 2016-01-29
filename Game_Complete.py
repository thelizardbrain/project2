import webbrowser, os
import pygame, sys
from pygame.locals import *
import time
import random
pygame.init()

#pygame.mixer.music.load("test1.mp4")
#pygame.mixer.music.play(-1, 0.0)
#pygame.mixer.music.set_volume(0.5)

display = pygame.display.set_mode((800, 600))   # basis framework
caption = pygame.display.set_caption('Survivor')
fps = pygame.time.Clock()
logoIMG = pygame.image.load('logo.png')
tekst = pygame.font.Font('freesansbold.ttf', 20)


hudpion1 = pygame.image.load("hud_glove_blue.png")
hudpion2 = pygame.image.load("hud_glove_green.png")
hudpion3 = pygame.image.load("hud_glove_red.png")
hudpion4 = pygame.image.load("hud_glove_yellow.png")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 20, 0)
dark_red = (150, 0, 0)

class Button:
        def __init__(self, screen_rect):
            self.image = pygame.Surface([100, 50]).convert()
            self.image.fill((150,0,0))
            self.rect = self.image.get_rect(center=(800,150))
            self.font = pygame.font.Font('freesansbold.ttf',40)
        def render(self, surf):
            surf.blit(self.image, self.rect)
            surf.blit(self.font.render("DICE!",True,(250,250,250)),(self.rect))

def strip_from_sheet(sheet, start, size, columns, rows=1):
        frames = []
        for j in range(rows):
            for i in range(columns):
                location = (start[0]+size[0]*i, start[1]+size[1]*j)
                frames.append(sheet.subsurface(pygame.Rect(location, size)))
        return frames

def gameboard_4():
#constants representing colours
    YELLOW = (255, 255, 102)
    ANDERSGEEL = (204, 204, 0)
    RED = (201, 57, 57)
    ANDERSROOD = (153, 0, 0)
    GREEN = (102,   204, 0)
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
    colours = {
                    ROODVAK:        RED,
                    GROENVAK:       GREEN,
                    BLAUWVAK:       BLUE,
                    GEELVAK:        YELLOW,
                    WITVAK:         WHITE,
                    GRIJSVAK:       GREY,
                    ZWARTVAK:       BLACK,
                    ANDERSGROENVAK: ANDERSGROEN,
                    ANDERSGEELVAK:  ANDERSGEEL,
                    ANDERSROODVAK:  ANDERSROOD,
                    ANDERSBLAUWVAK: ANDERSBLAUW
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

    DISPLAYSURF = pygame.display.set_mode((1200, 750))
    screen_rect = DISPLAYSURF.get_rect()

    dice_sheet = pygame.image.load('dice.png')
    dice = strip_from_sheet(dice_sheet, (0,0), (36,36), 1, 6)

    image = pygame.Surface([0, 0]).convert()
    btn = Button(screen_rect)

    #set up the display
    midPic = pygame.image.load('Midden van bord.png')
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
    shade = pygame.image.load('zwart.png').convert()
    DISPLAYSURF.blit(pygame.transform.scale(shade, (555, 5)), (450, 650))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (555, 5)), (450, 95))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 560)), (445, 95))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 550)), (1000, 100))
    fight = pygame.image.load('fight.png').convert()
    fightx1 = 700
    fighty1 = 100
    fightx2 = 450
    fighty2 = 350
    fightx3 = 950
    fighty3 = 600

    def text_object(text,font):
        textSurface = font.render(text,True,white)
        return textSurface, textSurface.get_rect()

    def quitbutton():
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 750 + 100 > mouse[0] > 750 and 520 + 50 > mouse[1] > 520:
            pygame.draw.rect(DISPLAYSURF, RED, (750,520,100,50))
            if click[0] == 1:
                quit()
        else:
            pygame.draw.rect(DISPLAYSURF, ANDERSROOD,(750, 520, 100, 50))

        if 750 + 100 > mouse[0] > 750 and 450 + 50 > mouse[1] > 450:
            pygame.draw.rect(DISPLAYSURF, RED, (750,450,100,50))
            if click[0] == 1:
                time.sleep(1)
                webbrowser.open_new("file://" + os.path.realpath("Manual.pdf"))
        else:
            pygame.draw.rect(DISPLAYSURF, ANDERSROOD, (750,450,100,50))


        textSurf, textRect = text_object("Info",tekst)
        textRect.center= ((750+(100/2)), (450 +(50/2)))
        display.blit(textSurf,textRect)

        textSurf, textRect = text_object("Quit",tekst)
        textRect.center= ((750+(100/2)), (520 +(50/2)))
        display.blit(textSurf,textRect)


    turn = 'playerOne'

    #def game(rPx, rPy, bPx, bPy, gPx, gPy, grPx, grPy):
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
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion3, (100, 100)), (750, 0))
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
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion2, (100, 100)), (750, 0))
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
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion1, (100, 100)), (750, 0))
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
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion4, (100, 100)), (750, 0))
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


        quitbutton()
        DISPLAYSURF.blit(image, (1121,180))
        btn.render(DISPLAYSURF)
        pygame.display.update()

def gameboard_3():
#constants representing colours
    YELLOW = (255, 255, 102)
    ANDERSGEEL = (204, 204, 0)
    RED = (201, 57, 57)
    ANDERSROOD = (153, 0, 0)
    GREEN = (102,   204, 0)
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
    colours = {
                    ROODVAK:        RED,
                    GROENVAK:       GREEN,
                    BLAUWVAK:       BLUE,
                    GEELVAK:        YELLOW,
                    WITVAK:         WHITE,
                    GRIJSVAK:       GREY,
                    ZWARTVAK:       BLACK,
                    ANDERSGROENVAK: ANDERSGROEN,
                    ANDERSGEELVAK:  ANDERSGEEL,
                    ANDERSROODVAK:  ANDERSROOD,
                    ANDERSBLAUWVAK: ANDERSBLAUW
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

    DISPLAYSURF = pygame.display.set_mode((1200, 750))
    screen_rect = DISPLAYSURF.get_rect()

    dice_sheet = pygame.image.load('dice.png')
    dice = strip_from_sheet(dice_sheet, (0,0), (36,36), 1, 6)

    image = pygame.Surface([0, 0]).convert()
    btn = Button(screen_rect)

    #set up the display
    midPic = pygame.image.load('Midden van bord.png')
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

    def text_object(text,font):
        textSurface = font.render(text,True,white)
        return textSurface, textSurface.get_rect()

    def quitbutton():
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 750 + 100 > mouse[0] > 750 and 520 + 50 > mouse[1] > 520:
            pygame.draw.rect(DISPLAYSURF, RED, (750,520,100,50))
            if click[0] == 1:
                quit()
        else:
            pygame.draw.rect(DISPLAYSURF, ANDERSROOD,(750, 520, 100, 50))

        if 750 + 100 > mouse[0] > 750 and 450 + 50 > mouse[1] > 450:
            pygame.draw.rect(DISPLAYSURF, RED, (750,450,100,50))
            if click[0] == 1:
                time.sleep(1)
                webbrowser.open_new("file://" + os.path.realpath("Manual.pdf"))
        else:
            pygame.draw.rect(DISPLAYSURF, ANDERSROOD, (750,450,100,50))


        textSurf, textRect = text_object("Info",tekst)
        textRect.center= ((750+(100/2)), (450 +(50/2)))
        display.blit(textSurf,textRect)

        textSurf, textRect = text_object("Quit",tekst)
        textRect.center= ((750+(100/2)), (520 +(50/2)))
        display.blit(textSurf,textRect)

    turn = 'playerOne'

    #def game(rPx, rPy, bPx, bPy, gPx, gPy, grPx, grPy):
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

                    elif turn == 'playerThree':
                        DISPLAYSURF.blit(pygame.transform.scale(groenscore, (350, 450)), (0, 300))
                        if grDirection == 'right':
                            for i in list[:grand]:
                                if grPx == 950:
                                    grDirection = 'down'
                                    for n in list[i:ggrand]:
                                        grPy += 50
                                    break
                                else:
                                    grPx += 50
                            turn = 'playerOne'
                        elif grDirection == 'down':
                            for i in list[:grand]:
                                if grPy == 600:
                                    grDirection = 'left'
                                    for n in list[i:ggrand]:
                                        grPx -= 50
                                    break
                                else:
                                    grPy += 50
                            turn = 'playerOne'
                        elif grDirection == 'left':
                            for i in list[:grand]:
                                if grPx == 450:
                                    grDirection = 'up'
                                    for n in list[i:ggrand]:
                                        grPy -= 50
                                    break
                                else:
                                    grPx -= 50
                            turn = 'playerOne'
                        elif grDirection == 'up':
                            for i in list[:grand]:
                                if grPy == 100:
                                    grDirection = 'right'
                                    for n in list[i:ggrand]:
                                        grPx += 50
                                    break
                                else:
                                    grPy -= 50
                            turn = 'playerOne'

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
        DISPLAYSURF.blit(pygame.transform.scale(groenPion, (50, 50)), (grPx, grPy))

        quitbutton()
        DISPLAYSURF.blit(image, (1121,683))
        btn.render(DISPLAYSURF)
        pygame.display.update()

def gameboard_2():
#constants representing colours
    YELLOW = (255, 255, 102)
    ANDERSGEEL = (204, 204, 0)
    RED = (201, 57, 57)
    ANDERSROOD = (153, 0, 0)
    GREEN = (102,   204, 0)
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
    colours = {
                    ROODVAK:        RED,
                    GROENVAK:       GREEN,
                    BLAUWVAK:       BLUE,
                    GEELVAK:        YELLOW,
                    WITVAK:         WHITE,
                    GRIJSVAK:       GREY,
                    ZWARTVAK:       BLACK,
                    ANDERSGROENVAK: ANDERSGROEN,
                    ANDERSGEELVAK:  ANDERSGEEL,
                    ANDERSROODVAK:  ANDERSROOD,
                    ANDERSBLAUWVAK: ANDERSBLAUW
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

    DISPLAYSURF = pygame.display.set_mode((1200, 750))
    screen_rect = DISPLAYSURF.get_rect()

    dice_sheet = pygame.image.load('dice.png')
    dice = strip_from_sheet(dice_sheet, (0,0), (36,36), 1, 6)

    image = pygame.Surface([0, 0]).convert()
    btn = Button(screen_rect)

    #set up the display
    midPic = pygame.image.load('Midden van bord.png')
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
    DISPLAYSURF.blit(pygame.transform.scale(backPic, (750, 750)), (350, 0))
    shade = pygame.image.load('zwart.png').convert()
    DISPLAYSURF.blit(pygame.transform.scale(shade, (555, 5)), (450, 650))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (555, 5)), (450, 95))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 560)), (445, 95))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 550)), (1000, 100))
    fight = pygame.image.load('fight.png').convert()
    fightx1 = 700
    fighty1 = 100
    fightx2 = 450
    fighty2 = 350
    fightx3 = 950
    fighty3 = 600

    def text_object(text,font):
        textSurface = font.render(text,True,white)
        return textSurface, textSurface.get_rect()

    def quitbutton():
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 750 + 100 > mouse[0] > 750 and 520 + 50 > mouse[1] > 520:
            pygame.draw.rect(DISPLAYSURF, RED, (750,520,100,50))
            if click[0] == 1:
                quit()
        else:
            pygame.draw.rect(DISPLAYSURF, ANDERSROOD,(750, 520, 100, 50))

        if 750 + 100 > mouse[0] > 750 and 450 + 50 > mouse[1] > 450:
            pygame.draw.rect(DISPLAYSURF, RED, (750,450,100,50))
            if click[0] == 1:
                time.sleep(1)
                webbrowser.open_new("file://" + os.path.realpath("Manual.pdf"))
        else:
            pygame.draw.rect(DISPLAYSURF, ANDERSROOD, (750,450,100,50))


        textSurf, textRect = text_object("Info",tekst)
        textRect.center= ((750+(100/2)), (450 +(50/2)))
        display.blit(textSurf,textRect)

        textSurf, textRect = text_object("Quit",tekst)
        textRect.center= ((750+(100/2)), (520 +(50/2)))
        display.blit(textSurf,textRect)


    turn = 'playerOne'

    #def game(rPx, rPy, bPx, bPy, gPx, gPy, grPx, grPy):
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
                        if rDirection == 'right':
                            for i in list[:grand]:
                                if rPx == 950:
                                    rDirection = 'down'
                                    for n in list[i:ggrand]:
                                        rPy += 50
                                    break
                                else:
                                    rPx += 50
                            turn = 'playerOne'
                        elif rDirection == 'down':
                            for i in list[:grand]:
                                if rPy == 600:
                                    rDirection = 'left'
                                    for n in list[i:ggrand]:
                                        rPx -= 50
                                    break
                                else:
                                    rPy += 50
                            turn = 'playerOne'
                        elif rDirection == 'left':
                            for i in list[:grand]:
                                if rPx == 450:
                                    rDirection = 'up'
                                    for n in list[i:ggrand]:
                                        rPy -= 50
                                    break
                                else:
                                    rPx -= 50
                            turn = 'playerOne'
                        elif rDirection == 'up':
                            for i in list[:grand]:
                                if rPy == 100:
                                    rDirection = 'right'
                                    for n in list[i:ggrand]:
                                        rPx += 50
                                    break
                                else:
                                    rPy -= 50
                            turn = 'playerOne'


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

        quitbutton()
        DISPLAYSURF.blit(image, (781,680))
        btn.render(DISPLAYSURF)
        pygame.display.update()


def text_object(text, font):
    textsurface = font.render(text, True, white)
    return textsurface, textsurface.get_rect()


def logo(x, y):
    display.blit(logoIMG, (x, y))

x = (800 * 0.211)
y = (600 * 0.1)


def button_main():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if 400+100 > mouse[0] > 400 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (400, 450, 100, 50))
        if click[0] == 1:
            time.sleep(1)
            webbrowser.open_new("file://" + os.path.realpath("Manual.pdf"))

    else:
        pygame.draw.rect(display, red, (400, 450, 100, 50))

    if 550 + 100 > mouse[0] > 550 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (550, 450, 100, 50))
        if click[0] == 1:
            time.sleep(1)
            quit()
    else:
        pygame.draw.rect(display, red, (550, 450, 100, 50))

    if 250 + 100 > mouse[0] > 250 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (250, 450, 100, 50))
        if click[0] == 1:
            time.sleep(1)
            options()
    else:
        pygame.draw.rect(display, red, (250, 450, 100, 50))

    if 100 + 100 > mouse[0] > 100 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (100, 450, 100, 50))
        if click[0] == 1:
            time.sleep(1)
            player_select()
    else:
        pygame.draw.rect(display, red, (100, 450, 100, 50))

    textsurf, textrect = text_object("QUIT", tekst)
    textrect.center = ((550+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("INFO", tekst)
    textrect.center = ((400+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("OPTIONS", tekst)
    textrect.center = ((250+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("PLAY", tekst)
    textrect.center = ((100+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)


def button_options():

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if 390+100 > mouse[0] > 390 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (390, 450, 100, 50))
        if click[0] == 1:
            pygame.mixer.music.set_volume(0.1)
    else:
        pygame.draw.rect(display, red, (390, 450, 100, 50))

    if 510+100 > mouse[0] > 510 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (510, 450, 100, 50))
        if click[0] == 1:
            pygame.mixer.music.set_volume(0.9)
    else:
        pygame.draw.rect(display, red, (510, 450, 100, 50))





    if 270+100 > mouse[0] > 270 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (270, 450, 100, 50))
        if click[0] == 1:
            print("window mode")
            pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    else:
        pygame.draw.rect(display, red, (270, 450, 100, 50))

    if 650 + 100 > mouse[0] > 650 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (650, 450, 100, 50))
        if click[0] == 1:
            main_menu()
    else:
        pygame.draw.rect(display, red, (650, 450, 100, 50))

    if 150 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (150, 450, 100, 50))
        if click[0] == 1:
            pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
            print("fullscreen mode")
    else:
        pygame.draw.rect(display, red, (150, 450, 100, 50))

    textsurf, textrect = text_object("Return", tekst)
    textrect.center = ((650+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object(" Sound +", tekst)
    textrect.center = ((510 +(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object(" Sound -", tekst)
    textrect.center = ((390+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("Windowed", tekst)
    textrect.center = ((270+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("Fullscreen", tekst)
    textrect.center = ((150+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)


def button_player():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if 400+100 > mouse[0] > 400 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (400, 450, 100, 50))
        if click[0] == 1:
            gameboard_4()
    else:
        pygame.draw.rect(display, red, (400, 450, 100, 50))

    if 650 + 100 > mouse[0] > 650 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (650, 450, 100, 50))
        if click[0] == 1:
            main_menu()
    else:
        pygame.draw.rect(display, red, (650, 450, 100, 50))

    if 250 + 100 > mouse[0] > 250 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (250, 450, 100, 50))
        if click[0] == 1:
            gameboard_3()

    else:
        pygame.draw.rect(display, red, (250, 450, 100, 50))

    if 100 + 100 > mouse[0] > 100 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (100, 450, 100, 50))
        if click[0] == 1:
            gameboard_2()
    else:
        pygame.draw.rect(display, red, (100, 450, 100, 50))
    textsurf, textrect = text_object("Return", tekst)
    textrect.center = ((650+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("4 Players", tekst)
    textrect.center = ((400+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("3 Players", tekst)
    textrect.center = ((250+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("2 Players", tekst)
    textrect.center = ((100+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)


def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        display.fill(white)
        logo(x, y)
        button_main()
        pygame.display.flip()
        fps.tick()


def player_select():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        display.fill(white)
        logo(x, y)
        button_player()
        pygame.display.flip()
        fps.tick()


def options():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        display.fill(white)
        logo(x, y)
        button_options()
        pygame.display.flip()
        fps.tick()

main_menu()
pygame.quit()
quit()
