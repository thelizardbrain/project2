import os
import pygame, sys
import random



class Supercards:
    def __init__(self, supercardname):
        self.Name = supercardname
        self.Super_image = ("superfightcards", "superfight.png")

        if self.Name == "John Cena":
            self.Super_image = os.path.join("superfightcards", "john cena.png")
            self.damage = []
        elif self.Name == "Jason Statham":
            self.Super_image = os.path.join("superfightcards", "Jason statham.png")
            self.damage = []
        elif self.Name == "Bruce Hee":
            self.Super_image = os.path.join("superfightcards", "bruce hee.png")
            self.damage = []
        elif self.Name == "Jackie Chen":
            self.Super_image = os.path.join("superfightcards", "jackie chen.png")
            self.damage = []
        elif self.Name == "Agua man":
            self.Super_image = os.path.join("superfightcards", "agua man.png")
            self.damage = []
        elif self.Name == "Pariz Hilten":
            self.Super_image = os.path.join("superfightcards", "pariz hilten.png")
        elif self.Name == "Dexter":
            self.Super_image = os.path.join("superfightcards", "dexter.png")
            self.damage = []
        elif self.Name == "Steve Urkel":
            self.Super_image = os.path.join("superfightcards", "steve urkel.png")
            self.damage = []
        elif self.Name == "Ernold Schwarzenegger":
            self.Super_image = os.path.join("superfightcards", "ernold schwarzenegger.png")
            self.damage = []
        elif self.Name == "James Bend":
            self.Super_image = os.path.join("superfightcards", "james bend.png")
            self.damage = []
        elif self.Name == "The Roch":
            self.Super_image = os.path.join("superfightcards", "the roch.png")
            self.damage = []
        elif self.Name == "Chack Norris":
            self.Super_image = os.path.join("superfightcards", "chack norris.png")
            self.damage = []
        elif self.Name == "Vin Dieser":
            self.Super_image = os.path.join("superfightcards", "vin dieser.png")
            self.damage = []
        elif self.Name == "Super Merio":
            self.Super_image = os.path.join("superfightcards", "super merio.png")
            self.damage = []
        elif self.Name == "Steve Seagal":
            self.Super_image = os.path.join("superfightcards", "steve seagal.png")
            self.damage = []
        elif self.Name == "Jet Ri":
            self.Super_image = os.path.join("superfightcards", "jet ri.png")
            self.damage = []
        elif self.Name == "Wesley Sniper":
            self.Super_image = os.path.join("superfightcards", "wesley sniper.png")
            self.damage = []
        elif self.Name == "Terry Crews":
            self.Super_image = os.path.join("superfightcards", "terry crews.png")
            self.damage = []

    def player_damage(self, damage):
        self.damage -= damage

# super_list = ["John Cena", "Jason Statham", "Bruce Hee", "Jackie Chen", "Agua man", "Pariz Hilten", "Dexter", "Steve Urkel", "Ernold Schwarzenegger", "James Bend", "The Roch", "Chack Norris", "Vin Dieser", "Super Merio", "Steve Seagal", "Jet Ri", "Wesley Sniper", "Terry Crews"]
# super_random = random.randint(0, 17)
# print(super_list[super_random])
John = pygame.image.load('superfightcards/john cena.png')
Bruce = pygame.image.load('superfightcards/bruce hee.png')
Jackie = pygame.image.load('superfightcards/jackie chen.png')
Agua = pygame.image.load('superfightcards/agua man.png')
Pariz = pygame.image.load('superfightcards/pariz hilten.png')
Dexter = pygame.image.load('superfightcards/dexter.png')
Steve_Urkel = pygame.image.load('superfightcards/steve urkel.png')
Ernold = pygame.image.load('superfightcards/ernold schwarzenegger.png')
James = pygame.image.load('superfightcards/james bend.png')
Roch = pygame.image.load('superfightcards/the roch.png')
Chack = pygame.image.load('superfightcards/chack norris.png')
Vin = pygame.image.load('superfightcards/vin dieser.png')
Merio = pygame.image.load('superfightcards/super merio.png')
Steve_Seagal = pygame.image.load('superfightcards/steve seagal.png')
Jet = pygame.image.load('superfightcards/jet ri.png')
Wesley = pygame.image.load('superfightcards/wesley sinper.png')
Terry = pygame.image.load('superfightcards/terry crews.png')
Jason = pygame.image.load('superfightcards/Jason statham.png')
# hp4 = 3
# hp4 = 3
# hp4 = 3
                                # if super_random == 0:
                                #     DISPLAYSURF.blit(pygame.transform.scale(John, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 10
                                #     elif rand == 1:
                                #         hp4 -= 6
                                #     elif rand == 2:
                                #         hp4 -= 25
                                #     elif rand == 3:
                                #         hp4 -= 7
                                #     elif rand == 4:
                                #         hp4 -= 8
                                #     elif rand == 5:
                                #         hp4 -= 11
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 1:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Jason, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 15
                                #     elif rand == 1:
                                #         hp4 -= 17
                                #     elif rand == 2:
                                #         hp4 -= 19
                                #     elif rand == 3:
                                #         hp4 -= 21
                                #     elif rand == 4:
                                #         hp4 -= 23
                                #     elif rand == 5:
                                #         hp4 -= 26
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 2:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Bruce, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 20
                                #     elif rand == 1:
                                #         hp4 -= 15
                                #     elif rand == 2:
                                #         hp4 -= 5
                                #     elif rand == 3:
                                #         hp4 -= 7
                                #     elif rand == 4:
                                #         hp4 -= 8
                                #     elif rand == 5:
                                #         hp4 -= 26
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 3:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Jackie, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 12
                                #     elif rand == 1:
                                #         hp4 -= 10
                                #     elif rand == 2:
                                #         hp4 -= 15
                                #     elif rand == 3:
                                #         hp4 -= 9
                                #     elif rand == 4:
                                #         hp4 -= 10
                                #     elif rand == 5:
                                #         hp4 -= 25
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 4:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Agua, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 12
                                #     elif rand == 1:
                                #         hp4 -= 15
                                #     elif rand == 2:
                                #         hp4 -= 9
                                #     elif rand == 3:
                                #         hp4 -= 7
                                #     elif rand == 4:
                                #         hp4 -= 7
                                #     elif rand == 5:
                                #         hp4 -= 13
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 5:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Pariz, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 12
                                #     elif rand == 1:
                                #         hp4 -= 8
                                #     elif rand == 2:
                                #         hp4 -= 7
                                #     elif rand == 3:
                                #         hp4 -= 15
                                #     elif rand == 4:
                                #         hp4 -= 13
                                #     elif rand == 5:
                                #         hp4 -= 9
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 6:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Dexter, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 9
                                #     elif rand == 1:
                                #         hp4 -= 8
                                #     elif rand == 2:
                                #         hp4 -= 7
                                #     elif rand == 3:
                                #         hp4 -= 15
                                #     elif rand == 4:
                                #         hp4 -= 13
                                #     elif rand == 5:
                                #         hp4 -= 9
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 7:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Steve_Urkel, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 10
                                #     elif rand == 1:
                                #         hp4 -= 5
                                #     elif rand == 2:
                                #         hp4 -= 12
                                #     elif rand == 3:
                                #         hp4 -= 11
                                #     elif rand == 4:
                                #         hp4 -= 15
                                #     elif rand == 5:
                                #         hp4 -= 8
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 8:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Ernold, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 25
                                #     elif rand == 1:
                                #         hp4 -= 25
                                #     elif rand == 2:
                                #         hp4 -= 20
                                #     elif rand == 3:
                                #         hp4 -= 15
                                #     elif rand == 4:
                                #         hp4 -= 15
                                #     elif rand == 5:
                                #         hp4 -= 10
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 9:
                                #     DISPLAYSURF.blit(pygame.transform.scale(James, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 25
                                #     elif rand == 1:
                                #         hp4 -= 15
                                #     elif rand == 2:
                                #         hp4 -= 15
                                #     elif rand == 3:
                                #         hp4 -= 7
                                #     elif rand == 4:
                                #         hp4 -= 20
                                #     elif rand == 5:
                                #         hp4 -= 25
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 10:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Roch, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 13
                                #     elif rand == 1:
                                #         hp4 -= 28
                                #     elif rand == 2:
                                #         hp4 -= 30
                                #     elif rand == 3:
                                #         hp4 -= 17
                                #     elif rand == 4:
                                #         hp4 -= 10
                                #     elif rand == 5:
                                #         hp4 -= 7
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 11:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Chack, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 15
                                #     elif rand == 1:
                                #         hp4 -= 28
                                #     elif rand == 2:
                                #         hp4 -= 27
                                #     elif rand == 3:
                                #         hp4 -= 25
                                #     elif rand == 4:
                                #         hp4 -= 29
                                #     elif rand == 5:
                                #         hp4 -= 30
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 12:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Vin, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 20
                                #     elif rand == 1:
                                #         hp4 -= 25
                                #     elif rand == 2:
                                #         hp4 -= 30
                                #     elif rand == 3:
                                #         hp4 -= 25
                                #     elif rand == 4:
                                #         hp4 -= 20
                                #     elif rand == 5:
                                #         hp4 -= 15
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 13:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Merio, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 10
                                #     elif rand == 1:
                                #         hp4 -= 10
                                #     elif rand == 2:
                                #         hp4 -= 30
                                #     elif rand == 3:
                                #         hp4 -= 30
                                #     elif rand == 4:
                                #         hp4 -= 15
                                #     elif rand == 5:
                                #         hp4 -= 15
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 14:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Steve_Seagal, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 10
                                #     elif rand == 1:
                                #         hp4 -= 15
                                #     elif rand == 2:
                                #         hp4 -= 12
                                #     elif rand == 3:
                                #         hp4 -= 11
                                #     elif rand == 4:
                                #         hp4 -= 25
                                #     elif rand == 5:
                                #         hp4 -= 20
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 15:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Jet, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 10
                                #     elif rand == 1:
                                #         hp4 -= 30
                                #     elif rand == 2:
                                #         hp4 -= 12
                                #     elif rand == 3:
                                #         hp4 -= 25
                                #     elif rand == 4:
                                #         hp4 -= 14
                                #     elif rand == 5:
                                #         hp4 -= 23
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 16:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Wesley, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 10
                                #     elif rand == 1:
                                #         hp4 -= 12
                                #     elif rand == 2:
                                #         hp4 -= 14
                                #     elif rand == 3:
                                #         hp4 -= 16
                                #     elif rand == 4:
                                #         hp4 -= 14
                                #     elif rand == 5:
                                #         hp4 -= 12
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
                                # elif super_random == 17:
                                #     DISPLAYSURF.blit(pygame.transform.scale(Terry, (350, 450)), (0, 300))
                                #     if rand == 0:
                                #         hp4 -= 10
                                #     elif rand == 1:
                                #         hp4 -= 15
                                #     elif rand == 2:
                                #         hp4 -= 25
                                #     elif rand == 3:
                                #         hp4 -= 20
                                #     elif rand == 4:
                                #         hp4 -= 15
                                #     elif rand == 5:
                                #         hp4 -= 10
                                #     DISPLAYSURF.blit(pygame.transform.scale(shade, (150, 20)), (20, 250))
                                #     text("HP:       " + str(hp4), white, 30, 20, 250)
