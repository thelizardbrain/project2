import pygame,sys,time

pygame.init()
display = pygame.display.set_mode((1200,600))
white = (255,255,255)
black = (0,0,0)
red = (250,0,0)


def winningscreen_object(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

def winningscreen(text):

        largeText = pygame.font.Font('freesansbold.ttf',90)
        TextSurf, TextRect = winningscreen_object(text, largeText)
        TextRect.center = ((600),(350))
        display.fill(red)
        display.blit(TextSurf, TextRect)
        pygame.display.update()

        time.sleep(5)









#
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     display.fill(white)
#     pygame.display.update()