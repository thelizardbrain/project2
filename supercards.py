import os


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
