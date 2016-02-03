import pygame,sys,time

pygame.init()
display = pygame.display.set_mode((1000,600))
white = (255,255,255)
black = (0,0,0)
red = (250,0,0)
dark_red = (150,0,0)
tekst = pygame.font.Font('freesansbold.ttf',20)




def winningscreen_object(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

def winningscreen(text):
        largeText = pygame.font.Font('freesansbold.ttf',90)
        TextSurf, TextRect = winningscreen_object(text, largeText)
        TextRect.center = ((600),(350))
        display.fill(white)
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