import webbrowser, os
import pygame, sys
from pygame.locals import *
pygame.init()


display = pygame.display.set_mode((800,600)) # basis framework
caption = pygame.display.set_caption('Survivor')
fps = pygame.time.Clock()
logoIMG=pygame.image.load('logo.png')
tekst= pygame.font.Font('freesansbold.ttf',20)


black = (0,0,0)
white = (255,255,255)
red = (255,20,0)
dark_red = (150,0,0)


def text_object(text,font):
    textSurface = font.render(text,True,white)
    return textSurface, textSurface.get_rect()


def logo(x,y):
    display.blit(logoIMG,(x,y))

x = (800 * 0.211)
y = (600 * 0.1)


def button(action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()  # nieuwe functie die erop let dat er een mousebutton wordt ingedrukt
    print(click)                        #print een stroom van (0, 0, 0) in de console, checkt of er een mousebutton wordt ingedrukt
                                        #linkermuisknop = (1, 0, 0)     rechtermuisknop = (0, 0, 1)     middlemuisknop = (0, 1, 0)

    if 400+100 > mouse[0] > 400 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red,(400,450,100,50))
        if click[0] == 1:
            webbrowser.open_new("file://" + os.path.realpath("Manual.pdf"))


    else:
        pygame.draw.rect(display, red,(400,450,100,50))


    if 550 + 100 > mouse[0] > 550 and 450 + 50 > mouse[1] > 450:  #Quit button
        pygame.draw.rect(display, dark_red, (550,450,100,50))
        if click[0] == 1:               #Checkt of linkermuisknop is ingedrukt op gegeven coordinaten
            quit()                      #Actie bij de if statement, kan ook verwijzen naar functies en loops(dus andere screens)
    else:
        pygame.draw.rect(display, red,(550, 450, 100, 50))

    if 250 + 100 > mouse[0] > 250 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (250,450,100,50))
    else:
        pygame.draw.rect(display, red, (250,450,100,50))

    if 100 + 100 > mouse[0] > 100 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red,(100,450,100,50))
    else:
        pygame.draw.rect(display, red, (100,450,100,50))


    textSurf, textRect = text_object("QUIT",tekst)
    textRect.center= ((550+(100/2)), (450 +(50/2)))
    display.blit(textSurf,textRect)

    textSurf, textRect = text_object("INFO",tekst)
    textRect.center= ((400+(100/2)), (450 +(50/2)))
    display.blit(textSurf,textRect)

    textSurf, textRect = text_object("OPTIONS",tekst)
    textRect.center= ((250+(100/2)), (450 +(50/2)))
    display.blit(textSurf,textRect)

    textSurf, textRect = text_object("PLAY",tekst)
    textRect.center= ((100+(100/2)), (450 +(50/2)))
    display.blit(textSurf,textRect)




while True: # game loop
    for event in pygame.event.get():
        if event.type == QUIT:
           pygame.quit()
           sys.exit()
    display.fill (white)
    logo(x,y)
    button()
    pygame.display.flip()
    fps.tick()

pygame.quit()
quit()
