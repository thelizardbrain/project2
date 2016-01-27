import pygame,sys,random

pygame.init()
display = pygame.display.set_mode((800,600)) # basis framework
tekst = pygame.font.Font('freesansbold.ttf',20)
dice_een= pygame.image.load('een.png')
dice_twee= pygame.image.load('twee.png')
dice_three= pygame.image.load('drie.png')
dice_four= pygame.image.load('vier.png')
dice_five= pygame.image.load('vijf.png')
dice_six= pygame.image.load('logo.png')

white = (255,255,255)
red = (255,20,0)
dark_red = (150,0,0)


def text_object(text,font):
    textSurface = font.render(text,True,white)
    return textSurface, textSurface.get_rect()


def dice():
    value = random.randint(1,1)
    if value == 1:
        display.blit(dice_een,(50,50))


def button_draw(msg,x,y,w,h,ic,ac,action=None):
 mouse = pygame.mouse.get_pos()
 click = pygame.mouse.get_pressed()
 if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(display, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
         dice()
 else:
        pygame.draw.rect(display, ic,(x,y,w,h))

 textSurf, textRect = text_object(msg,tekst)
 textRect.center= ((x+(w/2)), (y +(h/2)))
 display.blit(textSurf,textRect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    display.fill(white)
    button_draw('Dice!',500,200,100,50,red,dark_red,'action')
    pygame.display.update()

