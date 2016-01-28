import pygame as pygame, sys
import pygame.locals
import random



class Button:
    def __init__(self, screen_rect):
        self.image = pygame.Surface([130, 50]).convert()
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center=(500,500))# positie button
        self.font = pygame.font.Font('freesansbold.ttf',48)

    def render(self, surf):
        surf.blit(self.image, self.rect)
        screen.blit(self.font.render("DICE!",True,(0,0,0)),(self.rect))

def strip_from_sheet(sheet, start, size, columns, rows=1):
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(sheet.subsurface(pygame.Rect(location, size)))
    return frames

pygame.init()
screen = pygame.display.set_mode((800, 600))
screen_rect = screen.get_rect()


dice_sheet = pygame.image.load('dice.png')
dice = strip_from_sheet(dice_sheet, (0,0), (36,36), 1, 6)



image = pygame.Surface([0, 0]).convert()
btn = Button(screen_rect)
done = False
while not done:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if btn.rect.collidepoint(pygame.mouse.get_pos()):
                rand = random.randint(0,5)
                image = dice[rand]
                print(rand + 1)

    screen.blit(image, (300,100)) # positie dobbelsteen
    btn.render(screen)
    pygame.display.update()

