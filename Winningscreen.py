import pygame,sys,time

pygame.init()
display = pygame.display.set_mode((750,600))
white = (255,255,255)
black = (0,0,0)
red = (250,0,0)
RED = (201, 57, 57)
ANDERSROOD = (153, 0, 0)
dark_red = (150,0,0)
tekst = pygame.font.Font('freesansbold.ttf',20)

def text_object(text,font):
        textSurface = font.render(text, True, white)
        return textSurface, textSurface.get_rect()

def quitbutton_end():
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 550 + 100 > mouse[0] > 550 and 450 + 50 > mouse[1] > 450:
            pygame.draw.rect(display, RED, (550, 450, 100, 50))
            if click[0] == 1:
               quit()
        else:
            pygame.draw.rect(display, ANDERSROOD,(550, 450, 100, 50))

        textSurf, textRect = text_object("Quit",tekst)
        textRect.center= ((550+(100/2)), (450 + (50/2)))
        display.blit(textSurf, textRect)


def winningscreen_object(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

def winningscreen(text):
        largeText = pygame.font.Font('freesansbold.ttf',90)
        TextSurf, TextRect = winningscreen_object(text, largeText)
        TextRect.center = ((600),(350))
        display.fill(white)
        display.blit(TextSurf, TextRect)
        quitbutton_end()
        pygame.display.flip()
        time.sleep(0.01)






# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     winningscreen('You win!')
#     pygame.display.update()