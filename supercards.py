import os
import pygame


class supercards:
    def __init__(self, supercardname):
        self.name = supercardname
        self.image = ("superfightcards", "superfight_oud.png")

        if supercardname == "John Cena":
            self.image = os.path.join("superfightcards", "john cena.png")
            self.damage = []
        elif supercardname == "Jason Statham":
            self.image = self.image = os.path.join("superfightcards", "Jason statham.png")
            self.damage = []
        elif supercardname == "Bruce Hee":
            self.image = os.path.join("superfightcards", "bruce hee.png")
            self.damage = []
        elif supercardname == "Jackie Chen":
            self.image = os.path.join("superfightcards", "jackie chen.png")
            self.damage = []
        elif supercardname == "Agua man":
            self.image = os.path.join("superfightcards", "agua man.png")
            self.damage = []
        elif supercardname == "Pariz Hilten":
            self.image = os.path.join("superfightcards", "pariz hilten.png")
        elif supercardname == "Dexter":
            self.image = os.path.join("superfightcards", "dexter.png")
            self.damage = []
        elif supercardname == "Steve Urkel":
            self.image = os.path.join("superfightcards", "steve urkel.png")
            self.damage = []
        elif supercardname == "Ernold Schwarzenegger":
            self.image = os.path.join("superfightcards", "ernold schwarzenegger.png")
            self.damage = []
        elif supercardname == "James Bend":
            self.image = os.path.join("superfightcards", "james bend.png")
            self.damage = []
        elif supercardname == "The Roch":
            self.image = os.path.join("superfightcards", "the roch.png")
            self.damage = []
        elif supercardname == "Chack Norris":
            self.image = os.path.join("superfightcards", "chack norris.png")
            self.damage = []
        elif supercardname == "Vin Dieser":
            self.image = os.path.join("superfightcards", "vin dieser.png")
            self.damage = []
        elif supercardname == "Super Merio":
            self.image = os.path.join("superfightcards", "super merio.png")
            self.damage = []
        elif supercardname == "Steve Seagal":
            self.image = os.path.join("superfightcards", "steve seagal.png")
            self.damage = []
        elif supercardname == "Jet Ri":
            self.image = os.path.join("superfightcards", "jet ri.png")
            self.damage = []
        elif supercardname == "Wesley Sniper":
            self.image = os.path.join("superfightcards", "wesley sniper.png")
            self.damage = []
        elif supercardname == "Terry Crews":
            self.image = os.path.join("superfightcards", "terry crews.png")
            self.damage = []

    def damage(self, damage):
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

