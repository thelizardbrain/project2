import webbrowser, os
import pygame, sys
from pygame.locals import *
import time
pygame.init()


display = pygame.display.set_mode((800, 600))   # basis framework
caption = pygame.display.set_caption('Survivor')
fps = pygame.time.Clock()
logoIMG = pygame.image.load('logo.png')
tekst = pygame.font.Font('freesansbold.ttf', 20)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 20, 0)
dark_red = (150, 0, 0)


def game():
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
                    ROODVAK:  RED,
                    GROENVAK: GREEN,
                    BLAUWVAK: BLUE,
                    GEELVAK: YELLOW,
                    WITVAK: WHITE,
                    GRIJSVAK: GREY,
                    ZWARTVAK: BLACK,
                    ANDERSGROENVAK: ANDERSGROEN,
                    ANDERSGEELVAK: ANDERSGEEL,
                    ANDERSROODVAK: ANDERSROOD,
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

    #set up the display
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((750, 750))
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

    #def game(rPx, rPy, bPx, bPy, gPx, gPy, grPx, grPy):
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
        if rDirection == 'right':
            rPx += 50
            if rPx == 600:
                rDirection = 'down'
        elif rDirection == 'down':
            rPy += 50
            if rPy == 600:
                rDirection = 'left'
        elif rDirection == 'left':
            rPx -= 50
            if rPx == 100:
                rDirection = 'up'
        elif rDirection == 'up':
            rPy -= 50
            if rPy == 100:
                rDirection = 'right'

        if bDirection == 'right':
            bPx += 50
            if bPx == 600:
                bDirection = 'down'
        elif bDirection == 'down':
            bPy += 50
            if bPy == 600:
                bDirection = 'left'
        elif bDirection == 'left':
            bPx -= 50
            if bPx == 100:
                bDirection = 'up'
        elif bDirection == 'up':
            bPy -= 50
            if bPy == 100:
                bDirection = 'right'

        if grDirection == 'right':
            grPx += 50
            if grPx == 600:
                grDirection = 'down'
        elif grDirection == 'down':
            grPy += 50
            if grPy == 600:
                grDirection = 'left'
        elif grDirection == 'left':
            grPx -= 50
            if grPx == 100:
                grDirection = 'up'
        elif grDirection == 'up':
            grPy -= 50
            if grPy == 100:
                grDirection = 'right'

        if gDirection == 'right':
            gPx += 50
            if gPx == 600:
                gDirection = 'down'
        elif gDirection == 'down':
            gPy += 50
            if gPy == 600:
                gDirection = 'left'
        elif gDirection == 'left':
            gPx -= 50
            if gPx == 100:
                gDirection = 'up'
        elif gDirection == 'up':
            gPy -= 50
            if gPy == 100:
                gDirection = 'right'
        print('MADE BY: \nMIKE KOUWENHOVEN')

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
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
    if 400+100 > mouse[0] > 400 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (400, 450, 100, 50))
        if click[0] == 1:
            print("window mode")
            pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    else:
        pygame.draw.rect(display, red, (400, 450, 100, 50))

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

    textsurf, textrect = text_object("Windowed", tekst)
    textrect.center = ((400+(100/2)), (450 + (50/2)))
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
            game()
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
            game()

    else:
        pygame.draw.rect(display, red, (250, 450, 100, 50))

    if 100 + 100 > mouse[0] > 100 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (100, 450, 100, 50))
        if click[0] == 1:
            game()
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
