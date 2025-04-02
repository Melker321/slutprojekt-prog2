class Cell:

    def __init__(self, mina, status, markering, närheten):
        self.mina= mina 
        self.status = status
        self.markering = markering
        self.närheten = närheten



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

        
