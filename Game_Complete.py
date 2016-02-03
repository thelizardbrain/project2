import webbrowser, os
import pygame, sys
from pygame.locals import *
import time
import random
from supercards import *
from Winningscreen import *

pygame.init()

#pygame.mixer.music.load("test1.mp4")
#pygame.mixer.music.play(-1, 0.0)
#pygame.mixer.music.set_volume(0.5)

display = pygame.display.set_mode((800, 600))   # basis framework
caption = pygame.display.set_caption('Survivor')
fps = pygame.time.Clock()
logoIMG = pygame.image.load('logo.png')
tekst = pygame.font.Font('freesansbold.ttf', 20)

hudpion_blauw = pygame.image.load("hud_glove_blue.png")
hudpion_groen = pygame.image.load("hud_glove_green.png")
hudpion_rood = pygame.image.load("hud_glove_red.png")
hudpion_geel = pygame.image.load("hud_glove_yellow.png")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 20, 0)
dark_red = (150, 0, 0)

class Button:
        def __init__(self, screen_rect):
            self.image = pygame.Surface([100, 50]).convert()
            self.image.fill((150, 0, 0))
            self.rect = self.image.get_rect(center=(1150, 150))
            self.font = pygame.font.Font('freesansbold.ttf', 40)
        def render(self, surf):
            surf.blit(self.image, self.rect)
            surf.blit(self.font.render("DICE!", True, (250, 250, 250)), (self.rect))


class Player:
    def __init__(self, id, hp):
        self.id = id
        self.hp = hp

    def __str__(self):
        return " {} {} ".format(self.id, self.hp)

    def damage(self, amount):
        self.hp -= amount
        return self.hp

    def heal(self):
        self.hp += 5
        return self.hp


def strip_from_sheet(sheet, start, size, columns, rows=1):
        frames = []
        for j in range(rows):
            for i in range(columns):
                location = (start[0]+size[0]*i, start[1]+size[1]*j)
                frames.append(sheet.subsurface(pygame.Rect(location, size)))
        return frames

def gameboard_4():
#constants representing colours
    YELLOW = (255, 255, 102)
    ANDERSGEEL = (204, 204, 0)
    RED = (201, 57, 57)
    ANDERSROOD = (153, 0, 0)
    GREEN = (102,   204, 0)
    ANDERSGROEN = (0, 102, 0)
    BLUE = (0,   102,   205)
    ANDERSBLAUW = (0, 51, 102)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (224, 224, 224)

    #constants representing the different resources
    ROODVAK  = 0
    GROENVAK = 1
    BLAUWVAK = 2
    GEELVAK  = 3
    WITVAK = 4
    GRIJSVAK = 5
    ZWARTVAK = 6
    ANDERSGROENVAK = 7
    ANDERSGEELVAK = 8
    ANDERSROODVAK = 9
    ANDERSBLAUWVAK = 10
    #a dictionary linking resources to colours
    colours = {
                    ROODVAK:        RED,
                    GROENVAK:       GREEN,
                    BLAUWVAK:       BLUE,
                    GEELVAK:        YELLOW,
                    WITVAK:         WHITE,
                    GRIJSVAK:       GREY,
                    ZWARTVAK:       BLACK,
                    ANDERSGROENVAK: ANDERSGROEN,
                    ANDERSGEELVAK:  ANDERSGEEL,
                    ANDERSROODVAK:  ANDERSROOD,
                    ANDERSBLAUWVAK: ANDERSBLAUW
                }

    #a list representing our tilemap
    tilemap = [
                [ANDERSBLAUWVAK, BLAUWVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, ROODVAK, ANDERSROODVAK],
                [BLAUWVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ROODVAK],
                [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
                [WITVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, WITVAK],
                [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
                [WITVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, WITVAK],
                [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
                [WITVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, WITVAK],
                [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
                [GEELVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GROENVAK],
                [ANDERSGEELVAK, GEELVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, GROENVAK, ANDERSGROENVAK]
              ]

    #useful game dimensions
    TILESIZE  = 50
    MAPWIDTH  = 11
    MAPHEIGHT = 11

    DISPLAYSURF = pygame.display.set_mode((1200, 750))
    screen_rect = DISPLAYSURF.get_rect()

    dice_sheet = pygame.image.load('dice.png')
    dice = strip_from_sheet(dice_sheet, (0, 0), (36, 36), 1, 6)

    image = pygame.Surface([0, 0]).convert()
    btn = Button(screen_rect)

    #set up the display
    midPic = pygame.image.load('Midden_van_bord.png')
    #centerPic = pygame.image.load('superfight.png')
    cPx = 700
    cPy = 300
    backPic = pygame.image.load('Hout2.png')
    roodPion = pygame.image.load('glove_red.png')
    roodscore = pygame.image.load('red_score.png')
    rPx = 950
    rPy = 100
    rDirection = 'down'
    blauwPion = pygame.image.load('glove_blue.png')
    blauwscore = pygame.image.load('blue_score.png')
    bPx = 450
    bPy = 100
    bDirection = 'right'
    groenPion = pygame.image.load('glove_green.png')
    groenscore = pygame.image.load('green_score.png')
    grPx = 950
    grPy = 600
    grDirection = 'left'
    geelPion = pygame.image.load('glove_yellow.png')
    geelscore = pygame.image.load('yellow_score.png')
    gPx = 450
    gPy = 600
    gDirection = 'up'
    DISPLAYSURF.blit(pygame.transform.scale(backPic, (750, 750)), (350, 0))
    shade = pygame.image.load('zwart.png').convert()
    DISPLAYSURF.blit(pygame.transform.scale(shade, (555, 5)), (450, 650))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (555, 5)), (450, 95))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 560)), (445, 95))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 550)), (1000, 100))
    fight = pygame.image.load('fight.png').convert()
    fightx1 = 700
    fighty1 = 100
    fightx2 = 450
    fighty2 = 350
    fightx3 = 950
    fighty3 = 600

    def text(text, textc, size, x, y):
        font = pygame.font.Font(None, size)
        text = font.render(text, 1, (textc))
        textpos = text.get_rect()
        textpos.x = x
        textpos.y = y
        DISPLAYSURF.blit(text, textpos)

    def text_object(text,font):
        textSurface = font.render(text, True, white)
        return textSurface, textSurface.get_rect()

    def quitbutton():
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 1100 + 100 > mouse[0] > 1100 and 520 + 50 > mouse[1] > 520:
            pygame.draw.rect(DISPLAYSURF, RED, (1100, 520, 100, 50))
            if click[0] == 1:
               quit()
        else:
            pygame.draw.rect(DISPLAYSURF, ANDERSROOD,(1100, 520, 100, 50))

        if 1100 + 100 > mouse[0] > 1100 and 450 + 50 > mouse[1] > 450:
            pygame.draw.rect(DISPLAYSURF, RED, (1100, 450, 100, 50))
            if click[0] == 1:
                time.sleep(1)
                webbrowser.open_new("file://" + os.path.realpath("Manual.pdf"))
        else:
            pygame.draw.rect(DISPLAYSURF, ANDERSROOD, (1100, 450, 100, 50))


        textSurf, textRect = text_object("Info",tekst)
        textRect.center= ((1100+(100/2)), (450 +(50/2)))
        display.blit(textSurf, textRect)

        textSurf, textRect = text_object("Quit",tekst)
        textRect.center= ((1100+(100/2)), (520 + (50/2)))
        display.blit(textSurf, textRect)


    turn = 'playerOne'
    DISPLAYSURF.blit(pygame.transform.scale(hudpion_blauw, (100, 100)), (200, 0))

    P1color = (0,   102,   205)
    player1 = Player(1, 50)
    text("Mike Tysen ", P1color, 30, 20, 20)
    text("HP:       " + str(player1.hp), white, 30, 20, 40)


    player2 = Player(2, 50)
    P2color = (201, 57, 57)
    text("Rocky Belboa ", P2color, 30, 20, 90)
    text("HP:       " + str(player2.hp), white, 30, 20, 110)


    player3 = Player(3, 50)
    P3color = (102, 204, 0)
    text("Badr Heri ", P3color, 30, 20, 160)
    text("HP:       " + str(player3.hp), white, 30, 20, 180)


    player4 = Player(4, 50)
    P4color = (255, 255, 102)
    text("Manny Pecquiao ", P4color, 30, 20, 230)
    text("HP:       " + str(player4.hp), white, 30, 20, 250)

    def Hoekfight(attacker, defender):
            damage = random.randint(1, 6)
            defense = random.randint(1, 6)
            if damage > defense:
                defender.hp -= damage
                if defender.hp == player1:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                elif defender.hp == player2:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                elif defender.hp == player3:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                elif defender.hp == player4:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
            elif damage < defense:
                attacker.hp -= defense
                if attacker.hp == player1:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                elif attacker.hp == player2:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                elif attacker.hp == player3:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                elif attacker.hp == player4:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
            elif damage == defense:
                Hoekfight(attacker, defender)

    #def game(rPx, rPy, bPx, bPy, gPx, gPy, grPx, grPy):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if player1.hp > 0 and player2.hp <= 0 and player3.hp <=0 and player4.hp <= 0:
                winningscreen('P1 Mike Tysen WINS')
            if player1.hp <= 0 and player2.hp > 0 and player3.hp <= 0 and player4.hp <= 0:
                winningscreen('P2 Rocky Belboa WINS')
            if player1.hp <= 0 and player2.hp <= 0 and player3.hp > 0 and player4.hp <= 0:
                winningscreen('P3 Badr Heri WINS')
            if player1.hp <= 0 and player2.hp <= 0 and player3.hp <= 0 and player4.hp > 0:
                winningscreen('P4 Manny Pecquiao WINS')
            if turn == 'playerOne':
                if player1.hp <= 0:
                    bPx = 1500
                    bPy = 1500
                    DISPLAYSURF.blit(pygame.transform.scale(hudpion_rood, (100, 100)), (200, 80))
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 80)), (0, 0))
                    turn = 'playerTwo'
            if turn == 'playerTwo':
                if player2.hp <= 0:
                    rPx = 1500
                    rPy = 1500
                    DISPLAYSURF.blit(pygame.transform.scale(hudpion_groen, (100, 100)), (200, 160))
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 80)), (0, 80))
                    turn = 'playerThree'
            if turn == 'playerThree':
                if player3.hp <= 0:
                    grPx = 1500
                    grPy = 1500
                    DISPLAYSURF.blit(pygame.transform.scale(hudpion_geel, (100, 100)), (200, 220))
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 70)), (0, 160))
                    turn = 'playerFour'
            if turn =='playerFour':
                if player4.hp <= 0:
                    gPx = 1500
                    gPy = 1500
                    DISPLAYSURF.blit(pygame.transform.scale(hudpion_blauw, (100, 100)), (200, 0))
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 80)), (0, 220))
                    turn = 'playerOne'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                    list = [1,2,3,4,5,6,7]
                    rand = random.randint(0, 5)
                    image = dice[rand]
                    grand = rand + 1
                    ggrand = grand + 1

                    if turn == 'playerOne':
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 0))
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 450)), (0, 300))
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion_rood, (100, 100)), (200, 80))
                        if player2.hp <= 0:
                            DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 160))
                        if bDirection == 'right':
                            for i in list[:grand]:
                                if bPx == 950:
                                    bDirection = 'down'
                                    for n in list[i:ggrand]:
                                        bPy += 50
                                    break
                                else:
                                    bPx += 50
                            if (bPx == fightx1 and bPy == fighty1) or (bPx == fightx3 and bPy == fighty2) or (bPx == fightx1 and bPy == fighty3) or (bPx == fightx2 and bPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 6
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 17
                                    elif rand == 2:
                                        player1.hp -= 19
                                    elif rand == 3:
                                        player1.hp -= 21
                                    elif rand == 4:
                                        player1.hp -= 23
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 5
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 9
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 9
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 7
                                    elif rand == 5:
                                        player1.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 9
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 5
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 20
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 13
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 17
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 27
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 29
                                    elif rand == 5:
                                        player1.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 30
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 25
                                    elif rand == 5:
                                        player1.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 30
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 12
                                    elif rand == 2:
                                        player1.hp -= 14
                                    elif rand == 3:
                                        player1.hp -= 16
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 20
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       "+ str(player1.hp), white, 30, 20, 40)
                            turn = 'playerTwo'
                        elif bDirection == 'down':
                            for i in list[:grand]:
                                if bPy == 600:
                                    bDirection = 'left'
                                    for n in list[i:ggrand]:
                                        bPx -= 50
                                    break
                                else:
                                    bPy += 50
                            if (bPx == fightx1 and bPy == fighty1) or (bPx == fightx3 and bPy == fighty2) or (bPx == fightx1 and bPy == fighty3) or (bPx == fightx2 and bPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 6
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 17
                                    elif rand == 2:
                                        player1.hp -= 19
                                    elif rand == 3:
                                        player1.hp -= 21
                                    elif rand == 4:
                                        player1.hp -= 23
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 5
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 9
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 9
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 7
                                    elif rand == 5:
                                        player1.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 9
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 5
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 20
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 13
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 17
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 27
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 29
                                    elif rand == 5:
                                        player1.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 30
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 25
                                    elif rand == 5:
                                        player1.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 30
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 12
                                    elif rand == 2:
                                        player1.hp -= 14
                                    elif rand == 3:
                                        player1.hp -= 16
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 20
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                            turn = 'playerTwo'
                        elif bDirection == 'left':
                            for i in list[:grand]:
                                if bPx == 450:
                                    bDirection = 'up'
                                    for n in list[i:ggrand]:
                                        bPy -= 50
                                    break
                                else:
                                    bPx -= 50
                            if (bPx == fightx1 and bPy == fighty1) or (bPx == fightx3 and bPy == fighty2) or (bPx == fightx1 and bPy == fighty3) or (bPx == fightx2 and bPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 6
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 17
                                    elif rand == 2:
                                        player1.hp -= 19
                                    elif rand == 3:
                                        player1.hp -= 21
                                    elif rand == 4:
                                        player1.hp -= 23
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 5
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 9
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 9
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 7
                                    elif rand == 5:
                                        player1.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 9
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 5
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 20
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 13
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 17
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 27
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 29
                                    elif rand == 5:
                                        player1.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 30
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 25
                                    elif rand == 5:
                                        player1.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 30
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 12
                                    elif rand == 2:
                                        player1.hp -= 14
                                    elif rand == 3:
                                        player1.hp -= 16
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 20
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                            turn = 'playerTwo'
                        elif bDirection == 'up':
                            for i in list[:grand]:
                                if bPy == 100:
                                    bDirection = 'right'
                                    for n in list[i:ggrand]:
                                        bPx += 50
                                    break
                                else:
                                    bPy -= 50
                            if (bPx == fightx1 and bPy == fighty1) or (bPx == fightx3 and bPy == fighty2) or (bPx == fightx1 and bPy == fighty3) or (bPx == fightx2 and bPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 6
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 17
                                    elif rand == 2:
                                        player1.hp -= 19
                                    elif rand == 3:
                                        player1.hp -= 21
                                    elif rand == 4:
                                        player1.hp -= 23
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 5
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 9
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 9
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 7
                                    elif rand == 5:
                                        player1.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 9
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 5
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 20
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 13
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 17
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 27
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 29
                                    elif rand == 5:
                                        player1.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 30
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 25
                                    elif rand == 5:
                                        player1.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 30
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 12
                                    elif rand == 2:
                                        player1.hp -= 14
                                    elif rand == 3:
                                        player1.hp -= 16
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 20
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                            turn = 'playerTwo'
                        if 100 <= bPy <= 200 and 900 <= bPx <= 1000:
                            Hoekfight(player1, player2)
                        elif 900 <= bPx <= 1000 and 550 <= bPy <= 650:
                            Hoekfight(player1, player3)
                        elif 550 <= bPy <= 650 and 450 <= bPx <= 550:
                            Hoekfight(player1, player4)
                        elif 100 <= bPy <= 200 and 450 <= bPx <= 550:
                            if player1.hp < 46:
                                player1.hp += 5
                            else:
                                player1.hp = 50
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                        text("HP:       " + str(player1.hp), white, 30, 20, 40)
                        turn = "playerTwo"

                    elif turn == 'playerTwo':
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 450)), (0, 300))
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 80))
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion_groen, (100, 100)), (200, 160))
                        if player3.hp <= 0:
                            DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 160))
                        if rDirection == 'right':
                            for i in list[:grand]:
                                if rPx == 950:
                                    rDirection = 'down'
                                    for n in list[i:ggrand]:
                                        rPy += 50
                                    break
                                else:
                                    rPx += 50
                            if (rPx == fightx1 and rPy == fighty1) or (rPx == fightx3 and rPy == fighty2) or (rPx == fightx1 and rPy == fighty3) or (rPx == fightx2 and rPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", " Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 6
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 17
                                    elif rand == 2:
                                        player2.hp -= 19
                                    elif rand == 3:
                                        player2.hp -= 21
                                    elif rand == 4:
                                        player2.hp -= 23
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 5
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 9
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 9
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 7
                                    elif rand == 5:
                                        player2.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 9
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 5
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 20
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 13
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 17
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 27
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 29
                                    elif rand == 5:
                                        player2.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 30
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 25
                                    elif rand == 5:
                                        player2.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 30
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 12
                                    elif rand == 2:
                                        player2.hp -= 14
                                    elif rand == 3:
                                        player2.hp -= 16
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 20
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                            turn = 'playerThree'
                        elif rDirection == 'down':
                            for i in list[:grand]:
                                if rPy == 600:
                                    rDirection = 'left'
                                    for n in list[i:ggrand]:
                                        rPx -= 50
                                    break
                                else:
                                    rPy += 50
                            if (rPx == fightx1 and rPy == fighty1) or (rPx == fightx3 and rPy == fighty2) or (rPx == fightx1 and rPy == fighty3) or (rPx == fightx2 and rPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 6
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 17
                                    elif rand == 2:
                                        player2.hp -= 19
                                    elif rand == 3:
                                        player2.hp -= 21
                                    elif rand == 4:
                                        player2.hp -= 23
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 5
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 9
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 9
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 7
                                    elif rand == 5:
                                        player2.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 9
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 5
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 20
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 13
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 17
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 27
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 29
                                    elif rand == 5:
                                        player2.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 30
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 25
                                    elif rand == 5:
                                        player2.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 30
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 12
                                    elif rand == 2:
                                        player2.hp -= 14
                                    elif rand == 3:
                                        player2.hp -= 16
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 20
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                            turn = 'playerThree'
                        elif rDirection == 'left':
                            for i in list[:grand]:
                                if rPx == 450:
                                    rDirection = 'up'
                                    for n in list[i:ggrand]:
                                        rPy -= 50
                                    break
                                else:
                                    rPx -= 50
                            if (rPx == fightx1 and rPy == fighty1) or (rPx == fightx3 and rPy == fighty2) or (rPx == fightx1 and rPy == fighty3) or (rPx == fightx2 and rPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 6
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 17
                                    elif rand == 2:
                                        player2.hp -= 19
                                    elif rand == 3:
                                        player2.hp -= 21
                                    elif rand == 4:
                                        player2.hp -= 23
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 5
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 9
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 9
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 7
                                    elif rand == 5:
                                        player2.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 9
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 5
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 20
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 13
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 17
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 27
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 29
                                    elif rand == 5:
                                        player2.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 30
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 25
                                    elif rand == 5:
                                        player2.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 30
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 12
                                    elif rand == 2:
                                        player2.hp -= 14
                                    elif rand == 3:
                                        player2.hp -= 16
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 20
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                            turn = 'playerThree'
                        elif rDirection == 'up':
                            for i in list[:grand]:
                                if rPy == 100:
                                    rDirection = 'right'
                                    for n in list[i:ggrand]:
                                        rPx += 50
                                    break
                                else:
                                    rPy -= 50
                            if (rPx == fightx1 and rPy == fighty1) or (rPx == fightx3 and rPy == fighty2) or (rPx == fightx1 and rPy == fighty3) or (rPx == fightx2 and rPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 6
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 17
                                    elif rand == 2:
                                        player2.hp -= 19
                                    elif rand == 3:
                                        player2.hp -= 21
                                    elif rand == 4:
                                        player2.hp -= 23
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 5
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 9
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 9
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 7
                                    elif rand == 5:
                                        player2.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 9
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 5
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 20
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 13
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 17
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 27
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 29
                                    elif rand == 5:
                                        player2.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 30
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 25
                                    elif rand == 5:
                                        player2.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 30
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 12
                                    elif rand == 2:
                                        player2.hp -= 14
                                    elif rand == 3:
                                        player2.hp -= 16
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 20
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                            turn = 'playerThree'
                        if 100 <= rPy <= 200 and 900 <= rPx <= 1000:
                            if player2.hp < 46:
                                player2.hp += 5
                            else:
                                player2.hp = 50
                        elif 550 <= rPy <= 650 and 900 <= rPx <= 1000:
                            Hoekfight(player2, player3)
                        elif 550 <= rPy <= 650 and 450 <= rPx <= 550:
                            Hoekfight(player2, player4)
                        elif 100 <= rPy <= 200 and 450 <= rPx <= 550:
                            Hoekfight(player2, player1)
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                        text("HP:       " + str(player2.hp), white, 30, 20, 110)
                        turn = 'playerThree'



                    elif turn == 'playerThree':
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 450)), (0, 300))
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 160))
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion_geel, (100, 100)), (200, 220))
                        if player4.hp <= 0:
                            DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 220))
                        if grDirection == 'right':
                            for i in list[:grand]:
                                if grPx == 950:
                                    grDirection = 'down'
                                    for n in list[i:ggrand]:
                                        grPy += 50
                                    break
                                else:
                                    grPx += 50
                            if (grPx == fightx1 and grPy == fighty1) or (grPx == fightx3 and grPy == fighty2) or (grPx == fightx1 and grPy == fighty3) or (grPx == fightx2 and grPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 6
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 17
                                    elif rand == 2:
                                        player3.hp -= 19
                                    elif rand == 3:
                                        player3.hp -= 21
                                    elif rand == 4:
                                        player3.hp -= 23
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 5
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 9
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 9
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 7
                                    elif rand == 5:
                                        player3.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 9
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 5
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 20
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 13
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 17
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 27
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 29
                                    elif rand == 5:
                                        player3.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 30
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 25
                                    elif rand == 5:
                                        player3.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 30
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 12
                                    elif rand == 2:
                                        player3.hp -= 14
                                    elif rand == 3:
                                        player3.hp -= 16
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 20
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                            turn = 'playerFour'

                        elif grDirection == 'down':
                            for i in list[:grand]:
                                if grPy == 600:
                                    grDirection = 'left'
                                    for n in list[i:ggrand]:
                                        grPx -= 50
                                    break
                                else:
                                    grPy += 50
                            if (grPx == fightx1 and grPy == fighty1) or (grPx == fightx3 and grPy == fighty2) or (grPx == fightx1 and grPy == fighty3) or (grPx == fightx2 and grPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 6
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 17
                                    elif rand == 2:
                                        player3.hp -= 19
                                    elif rand == 3:
                                        player3.hp -= 21
                                    elif rand == 4:
                                        player3.hp -= 23
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 5
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 9
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 9
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 7
                                    elif rand == 5:
                                        player3.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 9
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 5
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 20
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 13
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 17
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 27
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 29
                                    elif rand == 5:
                                        player3.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 30
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 25
                                    elif rand == 5:
                                        player3.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 30
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 12
                                    elif rand == 2:
                                        player3.hp -= 14
                                    elif rand == 3:
                                        player3.hp -= 16
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 20
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                            turn = 'playerFour'

                        elif grDirection == 'left':
                            for i in list[:grand]:
                                if grPx == 450:
                                    grDirection = 'up'
                                    for n in list[i:ggrand]:
                                        grPy -= 50
                                    break
                                else:
                                    grPx -= 50
                            if (grPx == fightx1 and grPy == fighty1) or (grPx == fightx3 and grPy == fighty2) or (grPx == fightx1 and grPy == fighty3) or (grPx == fightx2 and grPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 6
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 17
                                    elif rand == 2:
                                        player3.hp -= 19
                                    elif rand == 3:
                                        player3.hp -= 21
                                    elif rand == 4:
                                        player3.hp -= 23
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 5
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 9
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 9
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 7
                                    elif rand == 5:
                                        player3.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 9
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 5
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 20
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 13
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 17
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 27
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 29
                                    elif rand == 5:
                                        player3.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 30
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 25
                                    elif rand == 5:
                                        player3.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 30
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 12
                                    elif rand == 2:
                                        player3.hp -= 14
                                    elif rand == 3:
                                        player3.hp -= 16
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 20
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                            turn = 'playerFour'

                        elif grDirection == 'up':
                            for i in list[:grand]:
                                if grPy == 100:
                                    grDirection = 'right'
                                    for n in list[i:ggrand]:
                                        grPx += 50
                                    break
                                else:
                                    grPy -= 50
                            if (grPx == fightx1 and grPy == fighty1) or (grPx == fightx3 and grPy == fighty2) or (grPx == fightx1 and grPy == fighty3) or (grPx == fightx2 and grPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 6
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 17
                                    elif rand == 2:
                                        player3.hp -= 19
                                    elif rand == 3:
                                        player3.hp -= 21
                                    elif rand == 4:
                                        player3.hp -= 23
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 5
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 9
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 9
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 7
                                    elif rand == 5:
                                        player3.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 9
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 5
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 20
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 13
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 17
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 27
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 29
                                    elif rand == 5:
                                        player3.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 30
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 25
                                    elif rand == 5:
                                        player3.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 30
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 12
                                    elif rand == 2:
                                        player3.hp -= 14
                                    elif rand == 3:
                                        player3.hp -= 16
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 20
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                            turn = 'playerFour'
                        if 100 <= grPy <= 200 and 900 <= grPx <= 1000:
                            Hoekfight(player3, player2)
                        elif 550 <= grPy <= 650 and 900 <= grPx <= 1000:
                            if player3.hp < 46:
                                player3.hp += 5
                            else:
                                player3.hp = 50
                        elif 550 <= grPy <= 650 and 450 <= grPx <= 550:
                            Hoekfight(player3, player4)
                        elif 100 <= grPy <= 200 and 450 <= grPx <= 550:
                            Hoekfight(player3, player1)
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                        text("HP:       " + str(player3.hp), white, 30, 20, 180)
                        turn = 'playerFour'


                    elif turn == 'playerFour':
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 450)), (0, 300))
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 220))
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion_blauw, (100, 100)), (200, 0))
                        if player1.hp <= 0:
                            DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 0))
                        if gDirection == 'right':
                            for i in list[:grand]:
                                if gPx == 950:
                                    gDirection = 'down'
                                    for n in list[i:ggrand]:
                                        gPy += 50
                                    break
                                else:
                                   gPx += 50
                            if (gPx == fightx1 and gPy == fighty1) or (gPx == fightx3 and gPy == fighty2) or (gPx == fightx1 and gPy == fighty3) or (gPx == fightx2 and gPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 6
                                    elif rand == 2:
                                        player4.hp -= 25
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 8
                                    elif rand == 5:
                                        player4.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 15
                                    elif rand == 1:
                                        player4.hp -= 17
                                    elif rand == 2:
                                        player4.hp -= 19
                                    elif rand == 3:
                                        player4.hp -= 21
                                    elif rand == 4:
                                        player4.hp -= 23
                                    elif rand == 5:
                                        player4.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 20
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 5
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 8
                                    elif rand == 5:
                                        player4.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 12
                                    elif rand == 1:
                                        player4.hp -= 10
                                    elif rand == 2:
                                        player4.hp -= 15
                                    elif rand == 3:
                                        player4.hp -= 9
                                    elif rand == 4:
                                        player4.hp -= 10
                                    elif rand == 5:
                                        player4.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 12
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 9
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 7
                                    elif rand == 5:
                                        player4.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 12
                                    elif rand == 1:
                                        player4.hp -= 8
                                    elif rand == 2:
                                        player4.hp -= 7
                                    elif rand == 3:
                                        player4.hp -= 15
                                    elif rand == 4:
                                        player4.hp -= 13
                                    elif rand == 5:
                                        player4.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 9
                                    elif rand == 1:
                                        player4.hp -= 8
                                    elif rand == 2:
                                        player4.hp -= 7
                                    elif rand == 3:
                                        player4.hp -= 15
                                    elif rand == 4:
                                        player4.hp -= 13
                                    elif rand == 5:
                                        player4.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 5
                                    elif rand == 2:
                                        player4.hp -= 12
                                    elif rand == 3:
                                        player4.hp -= 11
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 25
                                    elif rand == 1:
                                        player4.hp -= 25
                                    elif rand == 2:
                                        player4.hp -= 20
                                    elif rand == 3:
                                        player4.hp -= 15
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 25
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 15
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 20
                                    elif rand == 5:
                                        player4.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 13
                                    elif rand == 1:
                                        player4.hp -= 28
                                    elif rand == 2:
                                        player4.hp -= 30
                                    elif rand == 3:
                                        player4.hp -= 17
                                    elif rand == 4:
                                        player4.hp -= 10
                                    elif rand == 5:
                                        player4.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 15
                                    elif rand == 1:
                                        player4.hp -= 28
                                    elif rand == 2:
                                        player4.hp -= 27
                                    elif rand == 3:
                                        player4.hp -= 25
                                    elif rand == 4:
                                        player4.hp -= 29
                                    elif rand == 5:
                                        player4.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 20
                                    elif rand == 1:
                                        player4.hp -= 25
                                    elif rand == 2:
                                        player4.hp -= 30
                                    elif rand == 3:
                                        player4.hp -= 25
                                    elif rand == 4:
                                        player4.hp -= 20
                                    elif rand == 5:
                                        player4.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 10
                                    elif rand == 2:
                                        player4.hp -= 30
                                    elif rand == 3:
                                        player4.hp -= 30
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 12
                                    elif rand == 3:
                                        player4.hp -= 11
                                    elif rand == 4:
                                        player4.hp -= 25
                                    elif rand == 5:
                                        player4.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 30
                                    elif rand == 2:
                                        player4.hp -= 12
                                    elif rand == 3:
                                        player4.hp -= 25
                                    elif rand == 4:
                                        player4.hp -= 14
                                    elif rand == 5:
                                        player4.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 12
                                    elif rand == 2:
                                        player4.hp -= 14
                                    elif rand == 3:
                                        player4.hp -= 16
                                    elif rand == 4:
                                        player4.hp -= 14
                                    elif rand == 5:
                                        player4.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 25
                                    elif rand == 3:
                                        player4.hp -= 20
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                            turn = 'playerOne'

                        elif gDirection == 'down':
                            for i in list[:grand]:
                                if gPy == 600:
                                    gDirection = 'left'
                                    for n in list[i:ggrand]:
                                        gPx -= 50
                                    break
                                else:
                                    gPy += 50
                            if (gPx == fightx1 and gPy == fighty1) or (gPx == fightx3 and gPy == fighty2) or (gPx == fightx1 and gPy == fighty3) or (gPx == fightx2 and gPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 6
                                    elif rand == 2:
                                        player4.hp -= 25
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 8
                                    elif rand == 5:
                                        player4.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 15
                                    elif rand == 1:
                                        player4.hp -= 17
                                    elif rand == 2:
                                        player4.hp -= 19
                                    elif rand == 3:
                                        player4.hp -= 21
                                    elif rand == 4:
                                        player4.hp -= 23
                                    elif rand == 5:
                                        player4.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 20
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 5
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 8
                                    elif rand == 5:
                                        player4.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 12
                                    elif rand == 1:
                                        player4.hp -= 10
                                    elif rand == 2:
                                        player4.hp -= 15
                                    elif rand == 3:
                                        player4.hp -= 9
                                    elif rand == 4:
                                        player4.hp -= 10
                                    elif rand == 5:
                                        player4.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 12
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 9
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 7
                                    elif rand == 5:
                                        player4.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 12
                                    elif rand == 1:
                                        player4.hp -= 8
                                    elif rand == 2:
                                        player4.hp -= 7
                                    elif rand == 3:
                                        player4.hp -= 15
                                    elif rand == 4:
                                        player4.hp -= 13
                                    elif rand == 5:
                                        player4.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 9
                                    elif rand == 1:
                                        player4.hp -= 8
                                    elif rand == 2:
                                        player4.hp -= 7
                                    elif rand == 3:
                                        player4.hp -= 15
                                    elif rand == 4:
                                        player4.hp -= 13
                                    elif rand == 5:
                                        player4.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 5
                                    elif rand == 2:
                                        player4.hp -= 12
                                    elif rand == 3:
                                        player4.hp -= 11
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 25
                                    elif rand == 1:
                                        player4.hp -= 25
                                    elif rand == 2:
                                        player4.hp -= 20
                                    elif rand == 3:
                                        player4.hp -= 15
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 25
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 15
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 20
                                    elif rand == 5:
                                        player4.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 13
                                    elif rand == 1:
                                        player4.hp -= 28
                                    elif rand == 2:
                                        player4.hp -= 30
                                    elif rand == 3:
                                        player4.hp -= 17
                                    elif rand == 4:
                                        player4.hp -= 10
                                    elif rand == 5:
                                        player4.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 15
                                    elif rand == 1:
                                        player4.hp -= 28
                                    elif rand == 2:
                                        player4.hp -= 27
                                    elif rand == 3:
                                        player4.hp -= 25
                                    elif rand == 4:
                                        player4.hp -= 29
                                    elif rand == 5:
                                        player4.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 20
                                    elif rand == 1:
                                        player4.hp -= 25
                                    elif rand == 2:
                                        player4.hp -= 30
                                    elif rand == 3:
                                        player4.hp -= 25
                                    elif rand == 4:
                                        player4.hp -= 20
                                    elif rand == 5:
                                        player4.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 10
                                    elif rand == 2:
                                        player4.hp -= 30
                                    elif rand == 3:
                                        player4.hp -= 30
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 12
                                    elif rand == 3:
                                        player4.hp -= 11
                                    elif rand == 4:
                                        player4.hp -= 25
                                    elif rand == 5:
                                        player4.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 30
                                    elif rand == 2:
                                        player4.hp -= 12
                                    elif rand == 3:
                                        player4.hp -= 25
                                    elif rand == 4:
                                        player4.hp -= 14
                                    elif rand == 5:
                                        player4.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 12
                                    elif rand == 2:
                                        player4.hp -= 14
                                    elif rand == 3:
                                        player4.hp -= 16
                                    elif rand == 4:
                                        player4.hp -= 14
                                    elif rand == 5:
                                        player4.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 25
                                    elif rand == 3:
                                        player4.hp -= 20
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                            turn = 'playerOne'

                        elif gDirection == 'left':
                            for i in list[:grand]:
                                if gPx == 450:
                                    gDirection = 'up'
                                    for n in list[i:ggrand]:
                                        gPy -= 50
                                    break
                                else:
                                    gPx -= 50
                            if (gPx == fightx1 and gPy == fighty1) or (gPx == fightx3 and gPy == fighty2) or (gPx == fightx1 and gPy == fighty3) or (gPx == fightx2 and gPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 6
                                    elif rand == 2:
                                        player4.hp -= 25
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 8
                                    elif rand == 5:
                                        player4.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 15
                                    elif rand == 1:
                                        player4.hp -= 17
                                    elif rand == 2:
                                        player4.hp -= 19
                                    elif rand == 3:
                                        player4.hp -= 21
                                    elif rand == 4:
                                        player4.hp -= 23
                                    elif rand == 5:
                                        player4.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 20
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 5
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 8
                                    elif rand == 5:
                                        player4.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 12
                                    elif rand == 1:
                                        player4.hp -= 10
                                    elif rand == 2:
                                        player4.hp -= 15
                                    elif rand == 3:
                                        player4.hp -= 9
                                    elif rand == 4:
                                        player4.hp -= 10
                                    elif rand == 5:
                                        player4.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 12
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 9
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 7
                                    elif rand == 5:
                                        player4.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 12
                                    elif rand == 1:
                                        player4.hp -= 8
                                    elif rand == 2:
                                        player4.hp -= 7
                                    elif rand == 3:
                                        player4.hp -= 15
                                    elif rand == 4:
                                        player4.hp -= 13
                                    elif rand == 5:
                                        player4.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 9
                                    elif rand == 1:
                                        player4.hp -= 8
                                    elif rand == 2:
                                        player4.hp -= 7
                                    elif rand == 3:
                                        player4.hp -= 15
                                    elif rand == 4:
                                        player4.hp -= 13
                                    elif rand == 5:
                                        player4.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 5
                                    elif rand == 2:
                                        player4.hp -= 12
                                    elif rand == 3:
                                        player4.hp -= 11
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 25
                                    elif rand == 1:
                                        player4.hp -= 25
                                    elif rand == 2:
                                        player4.hp -= 20
                                    elif rand == 3:
                                        player4.hp -= 15
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 25
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 15
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 20
                                    elif rand == 5:
                                        player4.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 13
                                    elif rand == 1:
                                        player4.hp -= 28
                                    elif rand == 2:
                                        player4.hp -= 30
                                    elif rand == 3:
                                        player4.hp -= 17
                                    elif rand == 4:
                                        player4.hp -= 10
                                    elif rand == 5:
                                        player4.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 15
                                    elif rand == 1:
                                        player4.hp -= 28
                                    elif rand == 2:
                                        player4.hp -= 27
                                    elif rand == 3:
                                        player4.hp -= 25
                                    elif rand == 4:
                                        player4.hp -= 29
                                    elif rand == 5:
                                        player4.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 20
                                    elif rand == 1:
                                        player4.hp -= 25
                                    elif rand == 2:
                                        player4.hp -= 30
                                    elif rand == 3:
                                        player4.hp -= 25
                                    elif rand == 4:
                                        player4.hp -= 20
                                    elif rand == 5:
                                        player4.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 10
                                    elif rand == 2:
                                        player4.hp -= 30
                                    elif rand == 3:
                                        player4.hp -= 30
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 12
                                    elif rand == 3:
                                        player4.hp -= 11
                                    elif rand == 4:
                                        player4.hp -= 25
                                    elif rand == 5:
                                        player4.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 30
                                    elif rand == 2:
                                        player4.hp -= 12
                                    elif rand == 3:
                                        player4.hp -= 25
                                    elif rand == 4:
                                        player4.hp -= 14
                                    elif rand == 5:
                                        player4.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 12
                                    elif rand == 2:
                                        player4.hp -= 14
                                    elif rand == 3:
                                        player4.hp -= 16
                                    elif rand == 4:
                                        player4.hp -= 14
                                    elif rand == 5:
                                        player4.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 25
                                    elif rand == 3:
                                        player4.hp -= 20
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                            turn = 'playerOne'

                        elif gDirection == 'up':
                            for i in list[:grand]:
                                if gPy == 100:
                                    gDirection = 'right'
                                    for n in list[i:ggrand]:
                                        gPx += 50
                                    break
                                else:
                                    gPy -= 50
                            if (gPx == fightx1 and gPy == fighty1) or (gPx == fightx3 and gPy == fighty2) or (gPx == fightx1 and gPy == fighty3) or (gPx == fightx2 and gPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 6
                                    elif rand == 2:
                                        player4.hp -= 25
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 8
                                    elif rand == 5:
                                        player4.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 15
                                    elif rand == 1:
                                        player4.hp -= 17
                                    elif rand == 2:
                                        player4.hp -= 19
                                    elif rand == 3:
                                        player4.hp -= 21
                                    elif rand == 4:
                                        player4.hp -= 23
                                    elif rand == 5:
                                        player4.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 20
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 5
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 8
                                    elif rand == 5:
                                        player4.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 12
                                    elif rand == 1:
                                        player4.hp -= 10
                                    elif rand == 2:
                                        player4.hp -= 15
                                    elif rand == 3:
                                        player4.hp -= 9
                                    elif rand == 4:
                                        player4.hp -= 10
                                    elif rand == 5:
                                        player4.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 12
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 9
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 7
                                    elif rand == 5:
                                        player4.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 12
                                    elif rand == 1:
                                        player4.hp -= 8
                                    elif rand == 2:
                                        player4.hp -= 7
                                    elif rand == 3:
                                        player4.hp -= 15
                                    elif rand == 4:
                                        player4.hp -= 13
                                    elif rand == 5:
                                        player4.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 9
                                    elif rand == 1:
                                        player4.hp -= 8
                                    elif rand == 2:
                                        player4.hp -= 7
                                    elif rand == 3:
                                        player4.hp -= 15
                                    elif rand == 4:
                                        player4.hp -= 13
                                    elif rand == 5:
                                        player4.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 5
                                    elif rand == 2:
                                        player4.hp -= 12
                                    elif rand == 3:
                                        player4.hp -= 11
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 25
                                    elif rand == 1:
                                        player4.hp -= 25
                                    elif rand == 2:
                                        player4.hp -= 20
                                    elif rand == 3:
                                        player4.hp -= 15
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 25
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 15
                                    elif rand == 3:
                                        player4.hp -= 7
                                    elif rand == 4:
                                        player4.hp -= 20
                                    elif rand == 5:
                                        player4.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 13
                                    elif rand == 1:
                                        player4.hp -= 28
                                    elif rand == 2:
                                        player4.hp -= 30
                                    elif rand == 3:
                                        player4.hp -= 17
                                    elif rand == 4:
                                        player4.hp -= 10
                                    elif rand == 5:
                                        player4.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 15
                                    elif rand == 1:
                                        player4.hp -= 28
                                    elif rand == 2:
                                        player4.hp -= 27
                                    elif rand == 3:
                                        player4.hp -= 25
                                    elif rand == 4:
                                        player4.hp -= 29
                                    elif rand == 5:
                                        player4.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 20
                                    elif rand == 1:
                                        player4.hp -= 25
                                    elif rand == 2:
                                        player4.hp -= 30
                                    elif rand == 3:
                                        player4.hp -= 25
                                    elif rand == 4:
                                        player4.hp -= 20
                                    elif rand == 5:
                                        player4.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 10
                                    elif rand == 2:
                                        player4.hp -= 30
                                    elif rand == 3:
                                        player4.hp -= 30
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 12
                                    elif rand == 3:
                                        player4.hp -= 11
                                    elif rand == 4:
                                        player4.hp -= 25
                                    elif rand == 5:
                                        player4.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 30
                                    elif rand == 2:
                                        player4.hp -= 12
                                    elif rand == 3:
                                        player4.hp -= 25
                                    elif rand == 4:
                                        player4.hp -= 14
                                    elif rand == 5:
                                        player4.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 12
                                    elif rand == 2:
                                        player4.hp -= 14
                                    elif rand == 3:
                                        player4.hp -= 16
                                    elif rand == 4:
                                        player4.hp -= 14
                                    elif rand == 5:
                                        player4.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player4.hp -= 10
                                    elif rand == 1:
                                        player4.hp -= 15
                                    elif rand == 2:
                                        player4.hp -= 25
                                    elif rand == 3:
                                        player4.hp -= 20
                                    elif rand == 4:
                                        player4.hp -= 15
                                    elif rand == 5:
                                        player4.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                    text("HP:       " + str(player4.hp), white, 30, 20, 250)
                            turn = 'playerOne'
                        if 100 <= gPy <= 200 and 900 <= gPx <= 1000:
                            Hoekfight(player4, player2)
                        elif 550 <= gPy <= 650 and 900 <= gPx <= 1000:
                            Hoekfight(player4, player3)
                        elif 550 <= gPy <= 650 and 450 <= gPx <= 550:
                            if player4.hp < 46:
                                player4.hp += 5
                            else:
                                player4.hp = 50
                        elif 100 <= gPy <= 200 and 450 <= gPx <= 550:
                            Hoekfight(player4, player1)
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                        text("HP:       " + str(player4.hp), white, 30, 20, 250)
                        turn = 'playerOne'



        #loop through each row
        for row in range(MAPHEIGHT):
            #loop through each column in the row
            for column in range(MAPWIDTH):
                #draw the resource at that position in the tilemap, using the correct colour
                pygame.draw.rect(DISPLAYSURF, colours[tilemap[row][column]], (450 + column*TILESIZE, 100 + row*TILESIZE, TILESIZE, TILESIZE))
        DISPLAYSURF.blit(pygame.transform.scale(midPic, (450, 450)), (500, 150))
        DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx1, fighty1))
        DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx2, fighty2))
        DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx1, fighty3))
        DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx3, fighty2))
        DISPLAYSURF.blit(pygame.transform.scale(roodPion, (50, 50)), (rPx, rPy))
        DISPLAYSURF.blit(pygame.transform.scale(blauwPion, (50, 50)), (bPx, bPy))
        DISPLAYSURF.blit(pygame.transform.scale(geelPion, (50, 50)), (gPx, gPy))
        DISPLAYSURF.blit(pygame.transform.scale(groenPion, (50, 50)), (grPx, grPy))
        #DISPLAYSURF.blit(pygame.transform.scale(centerPic, (100, 150)), (cPx, cPy))


        quitbutton()
        DISPLAYSURF.blit(image, (1130,200))
        btn.render(DISPLAYSURF)
        pygame.display.update()

def gameboard_3():
#constants representing colours
    YELLOW = (255, 255, 102)
    ANDERSGEEL = (204, 204, 0)
    RED = (201, 57, 57)
    ANDERSROOD = (153, 0, 0)
    GREEN = (102,   204, 0)
    ANDERSGROEN = (0, 102, 0)
    BLUE = (0,   102,   205)
    ANDERSBLAUW = (0, 51, 102)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (224, 224, 224)

    #constants representing the different resources
    ROODVAK  = 0
    GROENVAK = 1
    BLAUWVAK = 2
    GEELVAK  = 3
    WITVAK = 4
    GRIJSVAK = 5
    ZWARTVAK = 6
    ANDERSGROENVAK = 7
    ANDERSGEELVAK = 8
    ANDERSROODVAK = 9
    ANDERSBLAUWVAK = 10

    #a dictionary linking resources to colours
    colours = {
                    ROODVAK:        RED,
                    GROENVAK:       GREEN,
                    BLAUWVAK:       BLUE,
                    GEELVAK:        YELLOW,
                    WITVAK:         WHITE,
                    GRIJSVAK:       GREY,
                    ZWARTVAK:       BLACK,
                    ANDERSGROENVAK: ANDERSGROEN,
                    ANDERSGEELVAK:  ANDERSGEEL,
                    ANDERSROODVAK:  ANDERSROOD,
                    ANDERSBLAUWVAK: ANDERSBLAUW
                }

    #a list representing our tilemap
    tilemap = [
                [ANDERSBLAUWVAK, BLAUWVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, ROODVAK, ANDERSROODVAK],
                [BLAUWVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ROODVAK],
                [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
                [WITVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, WITVAK],
                [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
                [WITVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, WITVAK],
                [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
                [WITVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, WITVAK],
                [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
                [GEELVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GROENVAK],
                [ANDERSGEELVAK, GEELVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, GROENVAK, ANDERSGROENVAK]
              ]

    #useful game dimensions
    TILESIZE  = 50
    MAPWIDTH  = 11
    MAPHEIGHT = 11

    DISPLAYSURF = pygame.display.set_mode((1200, 750))
    screen_rect = DISPLAYSURF.get_rect()

    dice_sheet = pygame.image.load('dice.png')
    dice = strip_from_sheet(dice_sheet, (0,0), (36,36), 1, 6)

    image = pygame.Surface([0, 0]).convert()
    btn = Button(screen_rect)

    #set up the display
    midPic = pygame.image.load('Midden_van_bord.png')
    backPic = pygame.image.load('Hout2.png')
    roodPion = pygame.image.load('glove_red.png')
    roodscore = pygame.image.load('red_score.png')
    rPx = 950
    rPy = 100
    rDirection = 'down'
    blauwPion = pygame.image.load('glove_blue.png')
    blauwscore = pygame.image.load('blue_score.png')
    bPx = 450
    bPy = 100
    bDirection = 'right'
    groenPion = pygame.image.load('glove_green.png')
    groenscore = pygame.image.load('green_score.png')
    grPx = 950
    grPy = 600
    grDirection = 'left'
    DISPLAYSURF.blit(pygame.transform.scale(backPic, (750, 750)), (350, 0))
    shade = pygame.image.load('zwart.png')
    DISPLAYSURF.blit(pygame.transform.scale(shade, (555, 5)), (450, 650))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (555, 5)), (450, 95))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 560)), (445, 95))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 550)), (1000, 100))
    fight = pygame.image.load('fight.png')
    fightx1 = 700
    fighty1 = 100
    fightx2 = 450
    fighty2 = 350
    fightx3 = 950
    fighty3 = 600

    def text(text, textc, size, x, y):
        font = pygame.font.Font(None, size)
        text = font.render(text, 1, (textc))
        textpos = text.get_rect()
        textpos.x = x
        textpos.y = y
        DISPLAYSURF.blit(text, textpos)

    def text_object(text,font):
        textSurface = font.render(text,True,white)
        return textSurface, textSurface.get_rect()

    def quitbutton():
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 1100 + 100 > mouse[0] > 1100 and 520 + 50 > mouse[1] > 520:
            pygame.draw.rect(DISPLAYSURF, RED, (1100,520,100,50))
            if click[0] == 1:
                quit()
        else:
            pygame.draw.rect(DISPLAYSURF, ANDERSROOD,(1100, 520, 100, 50))

        if 1100 + 100 > mouse[0] > 1100 and 450 + 50 > mouse[1] > 450:
            pygame.draw.rect(DISPLAYSURF, RED, (1100,450,100,50))
            if click[0] == 1:
                time.sleep(1)
                webbrowser.open_new("file://" + os.path.realpath("Manual.pdf"))
        else:
            pygame.draw.rect(DISPLAYSURF, ANDERSROOD, (1100,450,100,50))


        textSurf, textRect = text_object("Info",tekst)
        textRect.center = ((1100+(100/2)), (450 + (50/2)))
        display.blit(textSurf,textRect)

        textSurf, textRect = text_object("Quit",tekst)
        textRect.center = ((1100+(100/2)), (520 + (50/2)))
        display.blit(textSurf, textRect)

    turn = 'playerOne'
    DISPLAYSURF.blit(pygame.transform.scale(hudpion_blauw, (100, 100)), (200, 0))

    P1color = (0,   102,   205)
    player1 = Player(1, 50)
    text("Mike Tysen ", P1color, 30, 20, 20)
    text("HP:       "+ str(player1.hp), white, 30, 20, 40)

    player2 = Player(2, 50)
    P2color = (201, 57, 57)
    text("Rocky Belboa ", P2color, 30, 20, 90)
    text("HP:       " + str(player2.hp), white, 30, 20, 110)

    player3 = Player(3, 50)
    P3color = (102, 204, 0)
    text("Badr Heri ", P3color, 30, 20, 160)
    text("HP:       " + str(player3.hp), white, 30, 20, 180)

    def Hoekfight(attacker, defender):
            damage = random.randint(1, 6)
            defense = random.randint(1, 6)
            if damage > defense:
                defender.hp -= damage
                if defender.hp == player1:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                elif defender.hp == player2:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                elif defender.hp == player3:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
            elif damage < defense:
                attacker.hp -= defense
                if attacker.hp == player1:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                elif attacker.hp == player2:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                elif attacker.hp == player3:
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
            elif damage == defense:
                Hoekfight(attacker, defender)

    #def game(rPx, rPy, bPx, bPy, gPx, gPy, grPx, grPy):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if player1.hp > 0 and player2.hp <= 0 and player3.hp <=0:
                winningscreen('P1 Mike Tysen WINS')
            if player1.hp <= 0 and player2.hp > 0 and player3.hp <= 0:
                winningscreen('P2 Rocky Belboa WINS')
            if player1.hp <= 0 and player2.hp <= 0 and player3.hp > 0:
                winningscreen('P3 Badr Heri WINS')
            if turn == 'playerOne':
                if player1.hp <= 0:
                    bPx = 1500
                    bPy = 1500
                    DISPLAYSURF.blit(pygame.transform.scale(hudpion_rood, (100, 100)), (200, 80))
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 80)), (0, 0))
                    turn = 'playerTwo'
            if turn == 'playerTwo':
                if player2.hp <= 0:
                    rPx = 1500
                    rPy = 1500
                    DISPLAYSURF.blit(pygame.transform.scale(hudpion_groen, (100, 100)), (200, 160))
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 80)), (0, 80))
                    turn = 'playerThree'
            if turn == 'playerThree':
                if player3.hp <= 0:
                    grPx = 1500
                    grPy = 1500
                    DISPLAYSURF.blit(pygame.transform.scale(hudpion_blauw, (100, 100)), (200, 0))
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 70)), (0, 160))
                    turn = 'playerOne'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                    list = [1,2,3,4,5,6,7]
                    rand = random.randint(0,5)
                    image = dice[rand]
                    grand = rand + 1
                    ggrand = grand + 1


                    if turn == 'playerOne':
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 0))
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 450)), (0, 300))
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion_rood, (100, 100)), (200, 80))
                        if player2.hp <= 0:
                            DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 160))
                        if bDirection == 'right':
                            for i in list[:grand]:
                                if bPx == 950:
                                    bDirection = 'down'
                                    for n in list[i:ggrand]:
                                        bPy += 50
                                    break
                                else:
                                    bPx += 50
                            if (bPx == fightx1 and bPy == fighty1) or (bPx == fightx3 and bPy == fighty2) or (bPx == fightx1 and bPy == fighty3) or (bPx == fightx2 and bPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 6
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 17
                                    elif rand == 2:
                                        player1.hp -= 19
                                    elif rand == 3:
                                        player1.hp -= 21
                                    elif rand == 4:
                                        player1.hp -= 23
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 5
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 9
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 9
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 7
                                    elif rand == 5:
                                        player1.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 9
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 5
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 20
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 13
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 17
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 27
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 29
                                    elif rand == 5:
                                        player1.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 30
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 25
                                    elif rand == 5:
                                        player1.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 30
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 12
                                    elif rand == 2:
                                        player1.hp -= 14
                                    elif rand == 3:
                                        player1.hp -= 16
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 20
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                            turn = 'playerTwo'
                        elif bDirection == 'down':
                            for i in list[:grand]:
                                if bPy == 600:
                                    bDirection = 'left'
                                    for n in list[i:ggrand]:
                                        bPx -= 50
                                    break
                                else:
                                    bPy += 50
                            if (bPx == fightx1 and bPy == fighty1) or (bPx == fightx3 and bPy == fighty2) or (bPx == fightx1 and bPy == fighty3) or (bPx == fightx2 and bPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 6
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 17
                                    elif rand == 2:
                                        player1.hp -= 19
                                    elif rand == 3:
                                        player1.hp -= 21
                                    elif rand == 4:
                                        player1.hp -= 23
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 5
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 9
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 9
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 7
                                    elif rand == 5:
                                        player1.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 9
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 5
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 20
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 13
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 17
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 27
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 29
                                    elif rand == 5:
                                        player1.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 30
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 25
                                    elif rand == 5:
                                        player1.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 30
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 12
                                    elif rand == 2:
                                        player1.hp -= 14
                                    elif rand == 3:
                                        player1.hp -= 16
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 20
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                            turn = 'playerTwo'
                        elif bDirection == 'left':
                            for i in list[:grand]:
                                if bPx == 450:
                                    bDirection = 'up'
                                    for n in list[i:ggrand]:
                                        bPy -= 50
                                    break
                                else:
                                    bPx -= 50
                            if (bPx == fightx1 and bPy == fighty1) or (bPx == fightx3 and bPy == fighty2) or (bPx == fightx1 and bPy == fighty3) or (bPx == fightx2 and bPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 6
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 17
                                    elif rand == 2:
                                        player1.hp -= 19
                                    elif rand == 3:
                                        player1.hp -= 21
                                    elif rand == 4:
                                        player1.hp -= 23
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 5
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 9
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 9
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 7
                                    elif rand == 5:
                                        player1.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 9
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 5
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 20
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 13
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 17
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 27
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 29
                                    elif rand == 5:
                                        player1.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 30
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 25
                                    elif rand == 5:
                                        player1.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 30
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 12
                                    elif rand == 2:
                                        player1.hp -= 14
                                    elif rand == 3:
                                        player1.hp -= 16
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 20
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                            turn = 'playerTwo'
                        elif bDirection == 'up':
                            for i in list[:grand]:
                                if bPy == 100:
                                    bDirection = 'right'
                                    for n in list[i:ggrand]:
                                        bPx += 50
                                    break
                                else:
                                    bPy -= 50
                            if (bPx == fightx1 and bPy == fighty1) or (bPx == fightx3 and bPy == fighty2) or (bPx == fightx1 and bPy == fighty3) or (bPx == fightx2 and bPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 6
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 17
                                    elif rand == 2:
                                        player1.hp -= 19
                                    elif rand == 3:
                                        player1.hp -= 21
                                    elif rand == 4:
                                        player1.hp -= 23
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 5
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 9
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 9
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 7
                                    elif rand == 5:
                                        player1.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 9
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 5
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 20
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 13
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 17
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 27
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 29
                                    elif rand == 5:
                                        player1.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 30
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 25
                                    elif rand == 5:
                                        player1.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 30
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 12
                                    elif rand == 2:
                                        player1.hp -= 14
                                    elif rand == 3:
                                        player1.hp -= 16
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 20
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                            turn = 'playerTwo'
                        if 100 <= bPy <= 200 and 900 <= bPx <= 1000:
                            Hoekfight(player1, player2)
                        elif 900 <= bPx <= 1000 and 550 <= bPy <= 650:
                            Hoekfight(player1, player3)
                        elif 100 <= bPy <= 200 and 450 <= bPx <= 550:
                            if player1.hp < 46:
                                player1.hp += 5
                            else:
                                player1.hp = 50
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                        text("HP:       " + str(player1.hp), white, 30, 20, 40)
                        turn = 'playerTwo'


                    elif turn == 'playerTwo':
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 450)), (0, 300))
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 80))
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion_groen, (100, 100)), (200, 160))
                        if player3.hp <= 0:
                            DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 160))
                        if rDirection == 'right':
                            for i in list[:grand]:
                                if rPx == 950:
                                    rDirection = 'down'
                                    for n in list[i:ggrand]:
                                        rPy += 50
                                    break
                                else:
                                    rPx += 50
                            if (rPx == fightx1 and rPy == fighty1) or (rPx == fightx3 and rPy == fighty2) or (rPx == fightx1 and rPy == fighty3) or (rPx == fightx2 and rPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", " Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 6
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 17
                                    elif rand == 2:
                                        player2.hp -= 19
                                    elif rand == 3:
                                        player2.hp -= 21
                                    elif rand == 4:
                                        player2.hp -= 23
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 5
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 9
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 9
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 7
                                    elif rand == 5:
                                        player2.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 9
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 5
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 20
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 13
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 17
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 27
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 29
                                    elif rand == 5:
                                        player2.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 30
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 25
                                    elif rand == 5:
                                        player2.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 30
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 12
                                    elif rand == 2:
                                        player2.hp -= 14
                                    elif rand == 3:
                                        player2.hp -= 16
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 20
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                            turn = 'playerThree'
                        elif rDirection == 'down':
                            for i in list[:grand]:
                                if rPy == 600:
                                    rDirection = 'left'
                                    for n in list[i:ggrand]:
                                        rPx -= 50
                                    break
                                else:
                                    rPy += 50
                            if (rPx == fightx1 and rPy == fighty1) or (rPx == fightx3 and rPy == fighty2) or (rPx == fightx1 and rPy == fighty3) or (rPx == fightx2 and rPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 6
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 17
                                    elif rand == 2:
                                        player2.hp -= 19
                                    elif rand == 3:
                                        player2.hp -= 21
                                    elif rand == 4:
                                        player2.hp -= 23
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 5
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 9
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 9
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 7
                                    elif rand == 5:
                                        player2.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 9
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 5
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 20
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 13
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 17
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 27
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 29
                                    elif rand == 5:
                                        player2.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 30
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 25
                                    elif rand == 5:
                                        player2.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 30
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 12
                                    elif rand == 2:
                                        player2.hp -= 14
                                    elif rand == 3:
                                        player2.hp -= 16
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 20
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                            turn = 'playerThree'
                        elif rDirection == 'left':
                            for i in list[:grand]:
                                if rPx == 450:
                                    rDirection = 'up'
                                    for n in list[i:ggrand]:
                                        rPy -= 50
                                    break
                                else:
                                    rPx -= 50
                            if (rPx == fightx1 and rPy == fighty1) or (rPx == fightx3 and rPy == fighty2) or (rPx == fightx1 and rPy == fighty3) or (rPx == fightx2 and rPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 6
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 17
                                    elif rand == 2:
                                        player2.hp -= 19
                                    elif rand == 3:
                                        player2.hp -= 21
                                    elif rand == 4:
                                        player2.hp -= 23
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 5
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 9
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 9
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 7
                                    elif rand == 5:
                                        player2.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 9
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 5
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 20
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 13
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 17
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 27
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 29
                                    elif rand == 5:
                                        player2.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 30
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 25
                                    elif rand == 5:
                                        player2.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 30
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 12
                                    elif rand == 2:
                                        player2.hp -= 14
                                    elif rand == 3:
                                        player2.hp -= 16
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 20
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                            turn = 'playerThree'
                        elif rDirection == 'up':
                            for i in list[:grand]:
                                if rPy == 100:
                                    rDirection = 'right'
                                    for n in list[i:ggrand]:
                                        rPx += 50
                                    break
                                else:
                                    rPy -= 50
                            if (rPx == fightx1 and rPy == fighty1) or (rPx == fightx3 and rPy == fighty2) or (rPx == fightx1 and rPy == fighty3) or (rPx == fightx2 and rPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 6
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 17
                                    elif rand == 2:
                                        player2.hp -= 19
                                    elif rand == 3:
                                        player2.hp -= 21
                                    elif rand == 4:
                                        player2.hp -= 23
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 5
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 9
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 9
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 7
                                    elif rand == 5:
                                        player2.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 9
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 5
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 20
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 13
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 17
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 27
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 29
                                    elif rand == 5:
                                        player2.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 30
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 25
                                    elif rand == 5:
                                        player2.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 30
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 12
                                    elif rand == 2:
                                        player2.hp -= 14
                                    elif rand == 3:
                                        player2.hp -= 16
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 20
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       " + str(player2.hp), white, 30, 20, 110)
                            turn = 'playerThree'
                        if 100 <= rPy <= 200 and 900 <= rPx <= 1000:
                            if player2.hp < 46:
                                player2.hp += 5
                            else:
                                player2.hp = 50
                        elif 550 <= rPy <= 650 and 900 <= rPx <= 1000:
                            Hoekfight(player2, player3)
                        elif 100 <= rPy <= 200 and 450 <= rPx <= 550:
                            Hoekfight(player2, player1)
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                        text("HP:       " + str(player2.hp), white, 30, 20, 110)
                        turn = 'playerThree'

                    elif turn == 'playerThree':
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 450)), (0, 300))
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 160))
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion_blauw, (100, 100)), (200, 0))
                        if player1.hp <= 0:
                            DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 0))
                        if grDirection == 'right':
                            for i in list[:grand]:
                                if grPx == 950:
                                    grDirection = 'down'
                                    for n in list[i:ggrand]:
                                        grPy += 50
                                    break
                                else:
                                    grPx += 50
                            if (grPx == fightx1 and grPy == fighty1) or (grPx == fightx3 and grPy == fighty2) or (grPx == fightx1 and grPy == fighty3) or (grPx == fightx2 and grPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 6
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 17
                                    elif rand == 2:
                                        player3.hp -= 19
                                    elif rand == 3:
                                        player3.hp -= 21
                                    elif rand == 4:
                                        player3.hp -= 23
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 5
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 9
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 9
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 7
                                    elif rand == 5:
                                        player3.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 9
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 5
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 20
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 13
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 17
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 27
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 29
                                    elif rand == 5:
                                        player3.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 30
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 25
                                    elif rand == 5:
                                        player3.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 30
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 12
                                    elif rand == 2:
                                        player3.hp -= 14
                                    elif rand == 3:
                                        player3.hp -= 16
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 20
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                            turn = 'playerOne'

                        elif grDirection == 'down':
                            for i in list[:grand]:
                                if grPy == 600:
                                    grDirection = 'left'
                                    for n in list[i:ggrand]:
                                        grPx -= 50
                                    break
                                else:
                                    grPy += 50
                            if (grPx == fightx1 and grPy == fighty1) or (grPx == fightx3 and grPy == fighty2) or (grPx == fightx1 and grPy == fighty3) or (grPx == fightx2 and grPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 6
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 17
                                    elif rand == 2:
                                        player3.hp -= 19
                                    elif rand == 3:
                                        player3.hp -= 21
                                    elif rand == 4:
                                        player3.hp -= 23
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 5
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 9
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 9
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 7
                                    elif rand == 5:
                                        player3.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 9
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 5
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 20
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 13
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 17
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 27
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 29
                                    elif rand == 5:
                                        player3.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 30
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 25
                                    elif rand == 5:
                                        player3.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 30
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 12
                                    elif rand == 2:
                                        player3.hp -= 14
                                    elif rand == 3:
                                        player3.hp -= 16
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 20
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                            turn = 'playerOne'

                        elif grDirection == 'left':
                            for i in list[:grand]:
                                if grPx == 450:
                                    grDirection = 'up'
                                    for n in list[i:ggrand]:
                                        grPy -= 50
                                    break
                                else:
                                    grPx -= 50
                            if (grPx == fightx1 and grPy == fighty1) or (grPx == fightx3 and grPy == fighty2) or (grPx == fightx1 and grPy == fighty3) or (grPx == fightx2 and grPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 6
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 17
                                    elif rand == 2:
                                        player3.hp -= 19
                                    elif rand == 3:
                                        player3.hp -= 21
                                    elif rand == 4:
                                        player3.hp -= 23
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 5
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 9
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 9
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 7
                                    elif rand == 5:
                                        player3.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 9
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 5
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 20
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 13
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 17
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 27
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 29
                                    elif rand == 5:
                                        player3.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 30
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 25
                                    elif rand == 5:
                                        player3.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 30
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 12
                                    elif rand == 2:
                                        player3.hp -= 14
                                    elif rand == 3:
                                        player3.hp -= 16
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 20
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                            turn = 'playerOne'

                        elif grDirection == 'up':
                            for i in list[:grand]:
                                if grPy == 100:
                                    grDirection = 'right'
                                    for n in list[i:ggrand]:
                                        grPx += 50
                                    break
                                else:
                                    grPy -= 50
                            if (grPx == fightx1 and grPy == fighty1) or (grPx == fightx3 and grPy == fighty2) or (grPx == fightx1 and grPy == fighty3) or (grPx == fightx2 and grPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 6
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 17
                                    elif rand == 2:
                                        player3.hp -= 19
                                    elif rand == 3:
                                        player3.hp -= 21
                                    elif rand == 4:
                                        player3.hp -= 23
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 5
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 8
                                    elif rand == 5:
                                        player3.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 9
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 9
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 7
                                    elif rand == 5:
                                        player3.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 12
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 9
                                    elif rand == 1:
                                        player3.hp -= 8
                                    elif rand == 2:
                                        player3.hp -= 7
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 13
                                    elif rand == 5:
                                        player3.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 5
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 20
                                    elif rand == 3:
                                        player3.hp -= 15
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 25
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 15
                                    elif rand == 3:
                                        player3.hp -= 7
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 13
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 17
                                    elif rand == 4:
                                        player3.hp -= 10
                                    elif rand == 5:
                                        player3.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 15
                                    elif rand == 1:
                                        player3.hp -= 28
                                    elif rand == 2:
                                        player3.hp -= 27
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 29
                                    elif rand == 5:
                                        player3.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 20
                                    elif rand == 1:
                                        player3.hp -= 25
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 20
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 10
                                    elif rand == 2:
                                        player3.hp -= 30
                                    elif rand == 3:
                                        player3.hp -= 30
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 11
                                    elif rand == 4:
                                        player3.hp -= 25
                                    elif rand == 5:
                                        player3.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 30
                                    elif rand == 2:
                                        player3.hp -= 12
                                    elif rand == 3:
                                        player3.hp -= 25
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 12
                                    elif rand == 2:
                                        player3.hp -= 14
                                    elif rand == 3:
                                        player3.hp -= 16
                                    elif rand == 4:
                                        player3.hp -= 14
                                    elif rand == 5:
                                        player3.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player3.hp -= 10
                                    elif rand == 1:
                                        player3.hp -= 15
                                    elif rand == 2:
                                        player3.hp -= 25
                                    elif rand == 3:
                                        player3.hp -= 20
                                    elif rand == 4:
                                        player3.hp -= 15
                                    elif rand == 5:
                                        player3.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                                    text("HP:       " + str(player3.hp), white, 30, 20, 180)
                            turn = 'playerOne'
                        if 100 <= grPy <= 200 and 900 <= grPx <= 1000:
                            Hoekfight(player3, player2)
                        elif 550 <= grPy <= 650 and 900 <= grPx <= 1000:
                            if player3.hp < 46:
                                player3.hp += 5
                            else:
                                player3.hp = 50
                        elif 100 <= grPy <= 200 and 450 <= grPx <= 550:
                            Hoekfight(player3, player1)
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 180))
                        text("HP:       " + str(player3.hp), white, 30, 20, 180)
                        turn = 'playerOne'

    #loop through each row
        for row in range(MAPHEIGHT):
            #loop through each column in the row
            for column in range(MAPWIDTH):
                #draw the resource at that position in the tilemap, using the correct colour
                pygame.draw.rect(DISPLAYSURF, colours[tilemap[row][column]], (450 + column*TILESIZE, 100 + row*TILESIZE, TILESIZE, TILESIZE))
        DISPLAYSURF.blit(pygame.transform.scale(midPic, (450, 450)), (500, 150))
        DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx1, fighty1))
        DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx2, fighty2))
        DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx1, fighty3))
        DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx3, fighty2))
        DISPLAYSURF.blit(pygame.transform.scale(roodPion, (50, 50)), (rPx, rPy))
        DISPLAYSURF.blit(pygame.transform.scale(blauwPion, (50, 50)), (bPx, bPy))
        DISPLAYSURF.blit(pygame.transform.scale(groenPion, (50, 50)), (grPx, grPy))

        quitbutton()
        DISPLAYSURF.blit(image, (1130, 200))
        btn.render(DISPLAYSURF)
        pygame.display.update()

def gameboard_2():
#constants representing colours
    YELLOW = (255, 255, 102)
    ANDERSGEEL = (204, 204, 0)
    RED = (201, 57, 57)
    ANDERSROOD = (153, 0, 0)
    GREEN = (102,   204, 0)
    ANDERSGROEN = (0, 102, 0)
    BLUE = (0,   102,   205)
    ANDERSBLAUW = (0, 51, 102)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (224, 224, 224)

    #constants representing the different resources
    ROODVAK  = 0
    GROENVAK = 1
    BLAUWVAK = 2
    GEELVAK  = 3
    WITVAK = 4
    GRIJSVAK = 5
    ZWARTVAK = 6
    ANDERSGROENVAK = 7
    ANDERSGEELVAK = 8
    ANDERSROODVAK = 9
    ANDERSBLAUWVAK = 10

    #a dictionary linking resources to colours
    colours = {
                    ROODVAK:        RED,
                    GROENVAK:       GREEN,
                    BLAUWVAK:       BLUE,
                    GEELVAK:        YELLOW,
                    WITVAK:         WHITE,
                    GRIJSVAK:       GREY,
                    ZWARTVAK:       BLACK,
                    ANDERSGROENVAK: ANDERSGROEN,
                    ANDERSGEELVAK:  ANDERSGEEL,
                    ANDERSROODVAK:  ANDERSROOD,
                    ANDERSBLAUWVAK: ANDERSBLAUW
                }

    #a list representing our tilemap
    tilemap = [
                [ANDERSBLAUWVAK, BLAUWVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, ROODVAK, ANDERSROODVAK],
                [BLAUWVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ROODVAK],
                [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
                [WITVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, WITVAK],
                [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
                [WITVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, WITVAK],
                [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
                [WITVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, WITVAK],
                [GRIJSVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GRIJSVAK],
                [GEELVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, ZWARTVAK, GROENVAK],
                [ANDERSGEELVAK, GEELVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, WITVAK, GRIJSVAK, GROENVAK, ANDERSGROENVAK]
              ]

    #useful game dimensions
    TILESIZE  = 50
    MAPWIDTH  = 11
    MAPHEIGHT = 11

    DISPLAYSURF = pygame.display.set_mode((1200, 750))
    screen_rect = DISPLAYSURF.get_rect()

    dice_sheet = pygame.image.load('dice.png')
    dice = strip_from_sheet(dice_sheet, (0,0), (36,36), 1, 6)

    image = pygame.Surface([0, 0]).convert()
    btn = Button(screen_rect)

    #set up the display
    midPic = pygame.image.load('Midden_van_bord.png')
    backPic = pygame.image.load('Hout2.png')
    roodPion = pygame.image.load('glove_red.png')
    roodscore = pygame.image.load('red_score.png')
    rPx = 950
    rPy = 100
    rDirection = 'down'
    blauwPion = pygame.image.load('glove_blue.png')
    blauwscore = pygame.image.load('blue_score.png')
    bPx = 450
    bPy = 100
    bDirection = 'right'
    DISPLAYSURF.blit(pygame.transform.scale(backPic, (750, 750)), (350, 0))
    shade = pygame.image.load('zwart.png').convert()
    DISPLAYSURF.blit(pygame.transform.scale(shade, (555, 5)), (450, 650))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (555, 5)), (450, 95))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 560)), (445, 95))
    DISPLAYSURF.blit(pygame.transform.scale(shade, (5, 550)), (1000, 100))
    fight = pygame.image.load('fight.png').convert()
    fightx1 = 700
    fighty1 = 100
    fightx2 = 450
    fighty2 = 350
    fightx3 = 950
    fighty3 = 600

    def text(text, textc, size, x, y):
        font = pygame.font.Font(None, size)
        text = font.render(text, 1, (textc))
        textpos = text.get_rect()
        textpos.x = x
        textpos.y = y
        DISPLAYSURF.blit(text, textpos)

    def text_object(text,font):
        textSurface = font.render(text,True,white)
        return textSurface, textSurface.get_rect()

    def quitbutton():
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 1100 + 100 > mouse[0] > 1100 and 520 + 50 > mouse[1] > 520:
            pygame.draw.rect(DISPLAYSURF, RED, (1100,520,100,50))
            if click[0] == 1:
                quit()
        else:
            pygame.draw.rect(DISPLAYSURF, ANDERSROOD,(1100, 520, 100, 50))

        if 1100 + 100 > mouse[0] > 1100 and 450 + 50 > mouse[1] > 450:
            pygame.draw.rect(DISPLAYSURF, RED, (1100,450,100,50))
            if click[0] == 1:
                time.sleep(1)
                webbrowser.open_new("file://" + os.path.realpath("Manual.pdf"))
        else:
            pygame.draw.rect(DISPLAYSURF, ANDERSROOD, (1100,450,100,50))

        textSurf, textRect = text_object("Info",tekst)
        textRect.center= ((1100+(100/2)), (450 +(50/2)))
        display.blit(textSurf,textRect)

        textSurf, textRect = text_object("Quit",tekst)
        textRect.center= ((1100+(100/2)), (520 +(50/2)))
        display.blit(textSurf,textRect)


    turn = 'playerOne'
    DISPLAYSURF.blit(pygame.transform.scale(hudpion_blauw, (100, 100)), (200, 0))

    P1color = (0,   102,   205)
    player1 = Player(1, 50)
    text("Mike Tysen ", P1color, 30, 20, 20)
    text("HP:       "+ str(player1.hp), white, 30, 20, 40)

    player2 = Player(2, 50)
    P2color = (201, 57, 57)
    text("Rocky Belboa ", P2color, 30, 20, 90)
    text("HP:       " + str(player2.hp), white, 30, 20, 110)

    def Hoekfight(attacker, defender):
        damage = random.randint(1, 6)
        defense = random.randint(1, 6)
        if damage > defense:
            defender.hp -= damage
            if defender.hp == player1:
                DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                text("HP:       " + str(player1.hp), white, 30, 20, 40)
            elif defender.hp == player2:
                DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                text("HP:       " + str(player2.hp), white, 30, 20, 110)
        elif damage < defense:
            attacker.hp -= defense
            if attacker.hp == player1:
                DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                text("HP:       " + str(player1.hp), white, 30, 20, 40)
            elif attacker.hp == player2:
                DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                text("HP:       " + str(player2.hp), white, 30, 20, 110)
        elif damage == defense:
            Hoekfight(attacker, defender)
        print(player1.hp)
        print(player2.hp)

    #def game(rPx, rPy, bPx, bPy, gPx, gPy, grPx, grPy):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if player1.hp > 0 and player2.hp <= 0:
                winningscreen('P1 Mike Tysen WINS')
            if player1.hp <= 0 and player2.hp > 0:
                winningscreen('P2 Rocky Belboa WINS')
            if turn == 'playerOne':
                if player1.hp <= 0:
                    bPx = 1500
                    bPy = 1500
                    DISPLAYSURF.blit(pygame.transform.scale(hudpion_rood, (100, 100)), (200, 80))
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 80)), (0, 0))
                    turn = 'playerTwo'
            if turn == 'playerTwo':
                if player2.hp <= 0:
                    rPx = 1500
                    rPy = 1500
                    DISPLAYSURF.blit(pygame.transform.scale(hudpion_blauw, (100, 100)), (200, 0))
                    DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 80)), (0, 80))
                    turn = 'playerOne'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                    list = [1,2,3,4,5,6,7]
                    rand = random.randint(0,5)
                    image = dice[rand]
                    grand = rand + 1
                    ggrand = grand + 1

                    if turn == 'playerOne':
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 0))
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 450)), (0, 300))
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion_rood, (100, 100)), (200, 80))
                        if player2.hp <= 0:
                            DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 160))
                        if bDirection == 'right':
                            for i in list[:grand]:
                                if bPx == 950:
                                    bDirection = 'down'
                                    for n in list[i:ggrand]:
                                        bPy += 50
                                    break
                                else:
                                    bPx += 50
                            if (bPx == fightx1 and bPy == fighty1) or (bPx == fightx3 and bPy == fighty2) or (bPx == fightx1 and bPy == fighty3) or (bPx == fightx2 and bPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 6
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 17
                                    elif rand == 2:
                                        player1.hp -= 19
                                    elif rand == 3:
                                        player1.hp -= 21
                                    elif rand == 4:
                                        player1.hp -= 23
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 5
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 9
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 9
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 7
                                    elif rand == 5:
                                        player1.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 9
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 5
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 20
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 13
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 17
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 27
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 29
                                    elif rand == 5:
                                        player1.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 30
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 25
                                    elif rand == 5:
                                        player1.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 30
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 12
                                    elif rand == 2:
                                        player1.hp -= 14
                                    elif rand == 3:
                                        player1.hp -= 16
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 20
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                            turn = 'playerTwo'
                        elif bDirection == 'down':
                            for i in list[:grand]:
                                if bPy == 600:
                                    bDirection = 'left'
                                    for n in list[i:ggrand]:
                                        bPx -= 50
                                    break
                                else:
                                    bPy += 50
                            if (bPx == fightx1 and bPy == fighty1) or (bPx == fightx3 and bPy == fighty2) or (bPx == fightx1 and bPy == fighty3) or (bPx == fightx2 and bPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 6
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 17
                                    elif rand == 2:
                                        player1.hp -= 19
                                    elif rand == 3:
                                        player1.hp -= 21
                                    elif rand == 4:
                                        player1.hp -= 23
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 5
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 9
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 9
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 7
                                    elif rand == 5:
                                        player1.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 9
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 5
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 20
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 13
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 17
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 27
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 29
                                    elif rand == 5:
                                        player1.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 30
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 25
                                    elif rand == 5:
                                        player1.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 30
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 12
                                    elif rand == 2:
                                        player1.hp -= 14
                                    elif rand == 3:
                                        player1.hp -= 16
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 20
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                            turn = 'playerTwo'
                        elif bDirection == 'left':
                            for i in list[:grand]:
                                if bPx == 450:
                                    bDirection = 'up'
                                    for n in list[i:ggrand]:
                                        bPy -= 50
                                    break
                                else:
                                    bPx -= 50
                            if (bPx == fightx1 and bPy == fighty1) or (bPx == fightx3 and bPy == fighty2) or (bPx == fightx1 and bPy == fighty3) or (bPx == fightx2 and bPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 6
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 17
                                    elif rand == 2:
                                        player1.hp -= 19
                                    elif rand == 3:
                                        player1.hp -= 21
                                    elif rand == 4:
                                        player1.hp -= 23
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 5
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 9
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 9
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 7
                                    elif rand == 5:
                                        player1.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 9
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 5
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 20
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 13
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 17
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 27
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 29
                                    elif rand == 5:
                                        player1.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 30
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 25
                                    elif rand == 5:
                                        player1.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 30
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 12
                                    elif rand == 2:
                                        player1.hp -= 14
                                    elif rand == 3:
                                        player1.hp -= 16
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 20
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                            turn = 'playerTwo'
                        elif bDirection == 'up':
                            for i in list[:grand]:
                                if bPy == 100:
                                    bDirection = 'right'
                                    for n in list[i:ggrand]:
                                        bPx += 50
                                    break
                                else:
                                    bPy -= 50
                            if (bPx == fightx1 and bPy == fighty1) or (bPx == fightx3 and bPy == fighty2) or (bPx == fightx1 and bPy == fighty3) or (bPx == fightx2 and bPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 6
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 17
                                    elif rand == 2:
                                        player1.hp -= 19
                                    elif rand == 3:
                                        player1.hp -= 21
                                    elif rand == 4:
                                        player1.hp -= 23
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 5
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 8
                                    elif rand == 5:
                                        player1.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 9
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 9
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 7
                                    elif rand == 5:
                                        player1.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 12
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 9
                                    elif rand == 1:
                                        player1.hp -= 8
                                    elif rand == 2:
                                        player1.hp -= 7
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 13
                                    elif rand == 5:
                                        player1.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 5
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 20
                                    elif rand == 3:
                                        player1.hp -= 15
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 25
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 15
                                    elif rand == 3:
                                        player1.hp -= 7
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 13
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 17
                                    elif rand == 4:
                                        player1.hp -= 10
                                    elif rand == 5:
                                        player1.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 15
                                    elif rand == 1:
                                        player1.hp -= 28
                                    elif rand == 2:
                                        player1.hp -= 27
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 29
                                    elif rand == 5:
                                        player1.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 20
                                    elif rand == 1:
                                        player1.hp -= 25
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 20
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 10
                                    elif rand == 2:
                                        player1.hp -= 30
                                    elif rand == 3:
                                        player1.hp -= 30
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 11
                                    elif rand == 4:
                                        player1.hp -= 25
                                    elif rand == 5:
                                        player1.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 30
                                    elif rand == 2:
                                        player1.hp -= 12
                                    elif rand == 3:
                                        player1.hp -= 25
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 12
                                    elif rand == 2:
                                        player1.hp -= 14
                                    elif rand == 3:
                                        player1.hp -= 16
                                    elif rand == 4:
                                        player1.hp -= 14
                                    elif rand == 5:
                                        player1.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player1.hp -= 10
                                    elif rand == 1:
                                        player1.hp -= 15
                                    elif rand == 2:
                                        player1.hp -= 25
                                    elif rand == 3:
                                        player1.hp -= 20
                                    elif rand == 4:
                                        player1.hp -= 15
                                    elif rand == 5:
                                        player1.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                                    text("HP:       " + str(player1.hp), white, 30, 20, 40)
                            turn = 'playerTwo'
                        if 100 <= bPy <= 200 and 900 <= bPx <= 1000:
                            Hoekfight(player1, player2)
                        elif 100 <= bPy <= 200 and 450 <= bPx <= 550:
                            if player1.hp < 46:
                                player1.hp += 5
                            else:
                                player1.hp = 50
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 40))
                        text("HP:       " + str(player1.hp), white, 30, 20, 40)
                        turn = 'playerTwo'


                    elif turn == 'playerTwo':
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (350, 450)), (0, 300))
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 80))
                        DISPLAYSURF.blit(pygame.transform.scale(hudpion_blauw, (100, 100)), (200, 0))
                        if player1.hp <= 0:
                            DISPLAYSURF.blit(pygame.transform.scale(shade, (100, 100)), (200, 160))
                        if rDirection == 'right':
                            for i in list[:grand]:
                                if rPx == 950:
                                    rDirection = 'down'
                                    for n in list[i:ggrand]:
                                        rPy += 50
                                    break
                                else:
                                    rPx += 50
                            if (rPx == fightx1 and rPy == fighty1) or (rPx == fightx3 and rPy == fighty2) or (rPx == fightx1 and rPy == fighty3) or (rPx == fightx2 and rPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", " Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 6
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 17
                                    elif rand == 2:
                                        player2.hp -= 19
                                    elif rand == 3:
                                        player2.hp -= 21
                                    elif rand == 4:
                                        player2.hp -= 23
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 5
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 9
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 9
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 7
                                    elif rand == 5:
                                        player2.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 9
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 5
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 20
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 13
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 17
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 27
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 29
                                    elif rand == 5:
                                        player2.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 30
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 25
                                    elif rand == 5:
                                        player2.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 30
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 12
                                    elif rand == 2:
                                        player2.hp -= 14
                                    elif rand == 3:
                                        player2.hp -= 16
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 20
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                            turn = 'playerOne'
                        elif rDirection == 'down':
                            for i in list[:grand]:
                                if rPy == 600:
                                    rDirection = 'left'
                                    for n in list[i:ggrand]:
                                        rPx -= 50
                                    break
                                else:
                                    rPy += 50
                            if (rPx == fightx1 and rPy == fighty1) or (rPx == fightx3 and rPy == fighty2) or (rPx == fightx1 and rPy == fighty3) or (rPx == fightx2 and rPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 6
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 17
                                    elif rand == 2:
                                        player2.hp -= 19
                                    elif rand == 3:
                                        player2.hp -= 21
                                    elif rand == 4:
                                        player2.hp -= 23
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 5
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 9
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 9
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 7
                                    elif rand == 5:
                                        player2.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 9
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 5
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 20
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 13
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 17
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 27
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 29
                                    elif rand == 5:
                                        player2.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 30
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 25
                                    elif rand == 5:
                                        player2.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 30
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 12
                                    elif rand == 2:
                                        player2.hp -= 14
                                    elif rand == 3:
                                        player2.hp -= 16
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 20
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                            turn = 'playerOne'
                        elif rDirection == 'left':
                            for i in list[:grand]:
                                if rPx == 450:
                                    rDirection = 'up'
                                    for n in list[i:ggrand]:
                                        rPy -= 50
                                    break
                                else:
                                    rPx -= 50
                            if (rPx == fightx1 and rPy == fighty1) or (rPx == fightx3 and rPy == fighty2) or (rPx == fightx1 and rPy == fighty3) or (rPx == fightx2 and rPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 6
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 17
                                    elif rand == 2:
                                        player2.hp -= 19
                                    elif rand == 3:
                                        player2.hp -= 21
                                    elif rand == 4:
                                        player2.hp -= 23
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 5
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 9
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 9
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 7
                                    elif rand == 5:
                                        player2.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 9
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 5
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 20
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 13
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 17
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 27
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 29
                                    elif rand == 5:
                                        player2.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 30
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 25
                                    elif rand == 5:
                                        player2.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 30
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 12
                                    elif rand == 2:
                                        player2.hp -= 14
                                    elif rand == 3:
                                        player2.hp -= 16
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 20
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                            turn = 'playerOne'
                        elif rDirection == 'up':
                            for i in list[:grand]:
                                if rPy == 100:
                                    rDirection = 'right'
                                    for n in list[i:ggrand]:
                                        rPx += 50
                                    break
                                else:
                                    rPy -= 50
                            if (rPx == fightx1 and rPy == fighty1) or (rPx == fightx3 and rPy == fighty2) or (rPx == fightx1 and rPy == fighty3) or (rPx == fightx2 and rPy == fighty2):
                                super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
                                super_random = random.randint(0, 17)
                                print(super_list[super_random])
                                if super_random == 0:
                                    DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 6
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 11
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 1:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 17
                                    elif rand == 2:
                                        player2.hp -= 19
                                    elif rand == 3:
                                        player2.hp -= 21
                                    elif rand == 4:
                                        player2.hp -= 23
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 2:
                                    DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 5
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 8
                                    elif rand == 5:
                                        player2.hp -= 26
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 3:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 9
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 4:
                                    DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 9
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 7
                                    elif rand == 5:
                                        player2.hp -= 13
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 5:
                                    DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 12
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 6:
                                    DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 9
                                    elif rand == 1:
                                        player2.hp -= 8
                                    elif rand == 2:
                                        player2.hp -= 7
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 13
                                    elif rand == 5:
                                        player2.hp -= 9
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 7:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 5
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 8
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 8:
                                    DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 20
                                    elif rand == 3:
                                        player2.hp -= 15
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 9:
                                    DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 25
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 15
                                    elif rand == 3:
                                        player2.hp -= 7
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 25
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 10:
                                    DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 13
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 17
                                    elif rand == 4:
                                        player2.hp -= 10
                                    elif rand == 5:
                                        player2.hp -= 7
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 11:
                                    DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 15
                                    elif rand == 1:
                                        player2.hp -= 28
                                    elif rand == 2:
                                        player2.hp -= 27
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 29
                                    elif rand == 5:
                                        player2.hp -= 30
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 12:
                                    DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 20
                                    elif rand == 1:
                                        player2.hp -= 25
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 20
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 13:
                                    DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 10
                                    elif rand == 2:
                                        player2.hp -= 30
                                    elif rand == 3:
                                        player2.hp -= 30
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 15
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 14:
                                    DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 11
                                    elif rand == 4:
                                        player2.hp -= 25
                                    elif rand == 5:
                                        player2.hp -= 20
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 15:
                                    DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 30
                                    elif rand == 2:
                                        player2.hp -= 12
                                    elif rand == 3:
                                        player2.hp -= 25
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 23
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 16:
                                    DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 12
                                    elif rand == 2:
                                        player2.hp -= 14
                                    elif rand == 3:
                                        player2.hp -= 16
                                    elif rand == 4:
                                        player2.hp -= 14
                                    elif rand == 5:
                                        player2.hp -= 12
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                                elif super_random == 17:
                                    DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                    if rand == 0:
                                        player2.hp -= 10
                                    elif rand == 1:
                                        player2.hp -= 15
                                    elif rand == 2:
                                        player2.hp -= 25
                                    elif rand == 3:
                                        player2.hp -= 20
                                    elif rand == 4:
                                        player2.hp -= 15
                                    elif rand == 5:
                                        player2.hp -= 10
                                    DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                                    text("HP:       "+ str(player2.hp), white, 30, 20, 110)
                            turn = 'playerOne'
                        if 100 <= rPy <= 200 and 900 <= rPx <= 1000:
                            if player2.hp < 46:
                                player2.hp += 5
                            else:
                                player2.hp = 50
                        elif 100 <= rPy <= 200 and 450 <= rPx <= 550:
                            Hoekfight(player2, player1)
                        DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 110))
                        text("HP:       " + str(player2.hp), white, 30, 20, 110)
                        turn = 'playerOne'

    #loop through each row
        for row in range(MAPHEIGHT):
            #loop through each column in the row
            for column in range(MAPWIDTH):
                #draw the resource at that position in the tilemap, using the correct colour
                pygame.draw.rect(DISPLAYSURF, colours[tilemap[row][column]], (450 + column*TILESIZE, 100 + row*TILESIZE, TILESIZE, TILESIZE))
        DISPLAYSURF.blit(pygame.transform.scale(midPic, (450, 450)), (500, 150))
        DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx1, fighty1))
        DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx2, fighty2))
        DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx1, fighty3))
        DISPLAYSURF.blit(pygame.transform.scale(fight, (50, 50)), (fightx3, fighty2))
        DISPLAYSURF.blit(pygame.transform.scale(roodPion, (50, 50)), (rPx, rPy))
        DISPLAYSURF.blit(pygame.transform.scale(blauwPion, (50, 50)), (bPx, bPy))

        quitbutton()
        DISPLAYSURF.blit(image, (1130,200))
        btn.render(DISPLAYSURF)
        pygame.display.update()


def text_object(text, font):
    textsurface = font.render(text, True, white)
    return textsurface, textsurface.get_rect()


def logo(x, y):
    display.blit(logoIMG, (x, y))

x = (800 * 0.211)
y = (600 * 0.1)


def button_main():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if 400+100 > mouse[0] > 400 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (400, 450, 100, 50))
        if click[0] == 1:
            time.sleep(1)
            webbrowser.open_new("file://" + os.path.realpath("Manual.pdf"))

    else:
        pygame.draw.rect(display, red, (400, 450, 100, 50))

    if 550 + 100 > mouse[0] > 550 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (550, 450, 100, 50))
        if click[0] == 1:
            time.sleep(1)
            quit()
    else:
        pygame.draw.rect(display, red, (550, 450, 100, 50))

    if 250 + 100 > mouse[0] > 250 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (250, 450, 100, 50))
        if click[0] == 1:
            time.sleep(1)
            options()
    else:
        pygame.draw.rect(display, red, (250, 450, 100, 50))

    if 100 + 100 > mouse[0] > 100 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (100, 450, 100, 50))
        if click[0] == 1:
            time.sleep(1)
            player_select()
    else:
        pygame.draw.rect(display, red, (100, 450, 100, 50))

    textsurf, textrect = text_object("QUIT", tekst)
    textrect.center = ((550+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("INFO", tekst)
    textrect.center = ((400+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("OPTIONS", tekst)
    textrect.center = ((250+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("PLAY", tekst)
    textrect.center = ((100+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)


def button_options():

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if 390+30 > mouse[0] > 390 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (390, 450, 30, 50))
        if click[0] == 1:
            pygame.mixer.music.set_volume(0.0)
    else:
        pygame.draw.rect(display, red, (390, 450, 30, 50))

    if 420+30 > mouse[0] > 420 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (420, 450, 30, 50))
        if click[0] == 1:
            pygame.mixer.music.set_volume(0.2)
    else:
        pygame.draw.rect(display, red, (420, 450, 30, 50))

    if 450+30 > mouse[0] > 450 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (450, 450, 30, 50))
        if click[0] == 1:
            pygame.mixer.music.set_volume(0.4)
    else:
        pygame.draw.rect(display, red, (450, 450, 30, 50))


    if 480+30 > mouse[0] > 480 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (480, 450, 30, 50))
        if click[0] == 1:
            pygame.mixer.music.set_volume(0.6)
    else:
        pygame.draw.rect(display, red, (480, 450, 30, 50))

    if 510+30 > mouse[0] > 510 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (510, 450, 30, 50))
        if click[0] == 1:
            pygame.mixer.music.set_volume(0.8)
    else:
        pygame.draw.rect(display, red, (510, 450, 30, 50))


    if 540+30 > mouse[0] > 540 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (540, 450, 30, 50))
        if click[0] == 1:
            pygame.mixer.music.set_volume(1.0)
    else:
        pygame.draw.rect(display, red, (540, 450, 30, 50))





    if 270+100 > mouse[0] > 270 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (270, 450, 100, 50))
        if click[0] == 1:
            print("window mode")
            pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    else:
        pygame.draw.rect(display, red, (270, 450, 100, 50))

    if 650 + 100 > mouse[0] > 650 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (650, 450, 100, 50))
        if click[0] == 1:
            main_menu()
    else:
        pygame.draw.rect(display, red, (650, 450, 100, 50))

    if 150 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (150, 450, 100, 50))
        if click[0] == 1:
            pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
            print("fullscreen mode")
    else:
        pygame.draw.rect(display, red, (150, 450, 100, 50))

    textsurf, textrect = text_object("Return", tekst)
    textrect.center = ((650+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("  +", tekst)
    textrect.center = ((500 +(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object(" Volume ", tekst)
    textrect.center = ((425+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)


    textsurf, textrect = text_object("  -", tekst)
    textrect.center = ((350+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("Windowed", tekst)
    textrect.center = ((270+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("Fullscreen", tekst)
    textrect.center = ((150+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)


def button_player():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if 400+100 > mouse[0] > 400 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (400, 450, 100, 50))
        if click[0] == 1:
            gameboard_4()
    else:
        pygame.draw.rect(display, red, (400, 450, 100, 50))

    if 650 + 100 > mouse[0] > 650 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (650, 450, 100, 50))
        if click[0] == 1:
            main_menu()
    else:
        pygame.draw.rect(display, red, (650, 450, 100, 50))

    if 250 + 100 > mouse[0] > 250 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (250, 450, 100, 50))
        if click[0] == 1:
            gameboard_3()

    else:
        pygame.draw.rect(display, red, (250, 450, 100, 50))

    if 100 + 100 > mouse[0] > 100 and 450 + 50 > mouse[1] > 450:
        pygame.draw.rect(display, dark_red, (100, 450, 100, 50))
        if click[0] == 1:
            gameboard_2()
    else:
        pygame.draw.rect(display, red, (100, 450, 100, 50))
    textsurf, textrect = text_object("Return", tekst)
    textrect.center = ((650+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("4 Players", tekst)
    textrect.center = ((400+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("3 Players", tekst)
    textrect.center = ((250+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)

    textsurf, textrect = text_object("2 Players", tekst)
    textrect.center = ((100+(100/2)), (450 + (50/2)))
    display.blit(textsurf, textrect)


def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        display.fill(white)
        logo(x, y)
        button_main()
        pygame.display.flip()
        fps.tick()


def player_select():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        display.fill(white)
        logo(x, y)
        button_player()
        pygame.display.flip()
        fps.tick()


def options():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        display.fill(white)
        logo(x, y)
        button_options()
        pygame.display.flip()
        fps.tick()

main_menu()
pygame.quit()
quit()
