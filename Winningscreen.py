import pygame,sys,time

pygame.init()
display = pygame.display.set_mode((1000,600))
white = (255,255,255)
black = (0,0,0)
red = (250,0,0)
dark_red = (150,0,0)
tekst = pygame.font.Font('freesansbold.ttf',20)

def button(action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()


    if 400+100 > mouse[0] > 400 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red,(400,450,100,50))
        if click[0] == 1:
                pygame.quit()
    else:
        pygame.draw.rect(display, red,(400,450,100,50))


    if 600+100 > mouse[0] > 600 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red,(600,450,100,50))
        if click[0] == 1:
                pygame.quit()
    else:
        pygame.draw.rect(display, red,(600,450,100,50))



    textSurf, textRect = text_object("QUIT",tekst)
    textRect.center= ((400+(100/2)), (450 +(50/2)))
    display.blit(textSurf,textRect)


    textSurf, textRect = text_object("Return",tekst)
    textRect.center= ((600+(100/2)), (450 +(50/2)))
    display.blit(textSurf,textRect)


def text_object(text,font):
    textSurface = font.render(text,True,white)
    return textSurface, textSurface.get_rect()





def winningscreen_object(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

def winningscreen(text):
        largeText = pygame.font.Font('freesansbold.ttf',90)
        TextSurf, TextRect = winningscreen_object(text, largeText)
        TextRect.center = ((600),(350))
        display.fill(white)
        button()
        display.blit(TextSurf, TextRect)
        pygame.display.flip()
        time.sleep(3)






# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     winningscreen('You win!')
#     pygame.display.update()