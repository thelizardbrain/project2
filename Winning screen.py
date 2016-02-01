import pygame,sys,time

pygame.init()
display = pygame.display.set_mode((800,600))
screen_rect = display.get_rect()
white = (255,255,255)
black = (0,0,0)


def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

def message_display(text):

        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((400),(300))
        display.blit(TextSurf, TextRect)

        pygame.display.update()

        time.sleep(5)










while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    message_display('Player Wins!')
    display.fill(white)
    pygame.display.update()
