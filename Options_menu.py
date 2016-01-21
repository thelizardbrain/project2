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
    #print(click)                        #print een stroom van (0, 0, 0) in de console, checkt of er een mousebutton wordt ingedrukt
                                        #linkermuisknop = (1, 0, 0)     rechtermuisknop = (0, 0, 1)     middlemuisknop = (0, 1, 0)

    if 400+100 > mouse[0] > 400 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red,(400,450,100,50))
        if click[0] == 1:
            print("window mode")
            pygame.display.set_mode((800,600),pygame.RESIZABLE)
    else:
        pygame.draw.rect(display, red,(400,450,100,50))


    if 550 + 100 > mouse[0] > 550 and 450 + 50 > mouse[1] > 450:  #Quit button
        pygame.draw.rect(display, dark_red, (550,450,100,50))
        if click[0] == 1:               #Checkt of linkermuisknop is ingedrukt op gegeven coordinaten
            quit()                      #Actie bij de if statement, kan ook verwijzen naar functies en loops(dus andere screens)
    else:
        pygame.draw.rect(display, red,(550, 450, 100, 50))

    if 150 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (150,450,100,50))
        if click[0] == 1:
            pygame.display.set_mode((800,600),pygame.FULLSCREEN)
            print("fullscreen mode")
            # pygame.display.set_mode((800,600),pygame.FULLSCREEN)
            # pygame.display.set_mode((800,600),pygame.RESIZABLE)
    else:
        pygame.draw.rect(display, red, (150,450,100,50))

    # if 100 + 100 > mouse[0] > 100 and 450 + 50 > mouse[1] > 450:
    #     pygame.draw.rect(display, dark_red,(100,450,100,50))
    #     if click[0] == 1:
    #         print("Starts a game with 2 players")
    # else:
    #     pygame.draw.rect(display, red, (100,450,100,50))


    textSurf, textRect = text_object("Return",tekst)
    textRect.center= ((550+(100/2)), (450 +(50/2)))
    display.blit(textSurf,textRect)

    textSurf, textRect = text_object("Windowed",tekst)
    textRect.center= ((400+(100/2)), (450 +(50/2)))
    display.blit(textSurf,textRect)

    textSurf, textRect = text_object("Fullscreen",tekst)
    textRect.center= ((150+(100/2)), (450 +(50/2)))
    display.blit(textSurf,textRect)

    # textSurf, textRect = text_object("2 Players",tekst)
    # textRect.center= ((100+(100/2)), (450 +(50/2)))
    # display.blit(textSurf,textRect)




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