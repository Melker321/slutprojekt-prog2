class Cell:


        self.x = x
        self.y = y
        self.storlek = storlek
        self.status = "stängd"
        self.markering = False
        self.närheten = 0



class Plan:
    def __init__(self, bredd, höjd, antal_minor ):

        self.bredd = bredd
        self.höjd = höjd
        self.antal_minor = antal_minor



class Spel:
    def __init__(self, val, updatera, vinnst, spelplanen):
        self.val = val
        self.updatera = updatera
        self.vinnst = vinnst
        self.spelplanen = spelplanen

        
