import pygame,sys,time

pygame.init()
display = pygame.display.set_mode((800,600))
screen_rect = display.get_rect()
white = (255,255,255)
black = (0,0,0)
red = (250,0,0)


def winningscreen_object(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

def winningscreen(text):

        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = winningscreen_object(text, largeText)
        TextRect.center = ((400),(300))
        display.fill(red)
        display.blit(TextSurf, TextRect)
        pygame.display.update()

        time.sleep(5)











while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    winningscreen('Player Wins!')
    display.fill(white)
    pygame.display.update()
