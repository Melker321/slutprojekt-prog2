import pygame
import random
pygame.init()

nivåer = {
"lätt" : {"bredd":9, "höjd":9, "minor": 10},
"medel": {"bredd":14, "höjd":14, "minor":40},
"svår" : {"bredd":18, "höjd":18, "minor":100} 
}

class Cell:
    def __init__(self, x, y, storlek, mina=False):
        self.x = x
        self.y = y
        self.storlek = storlek
        self.mina = mina
        self.status = "stängd"
        self.markering = False
        self.närheten = 0
        

    def rita(self, yta):
        färg = (200,200,200) if self.status == "stängd" else (150,150,150) #if och else gör att färgen beror på om status är stängd eller inte
        if self.markering:#om markerat så ändras färgen.
            färg = (255,0,0)

        rect = pygame.Rect(self.x * self.storlek, self.y * self.storlek, self.storlek, self.storlek)
        pygame.draw.rect(yta, färg, rect)
        pygame.draw.rect(yta, (0, 0, 0), rect, 1)
        


class Plan:
    def __init__(self, bredd, höjd, antal_minor ):

        self.bredd = bredd
        self.höjd = höjd
        self.antal_minor = antal_minor
        self.storlek = 30
        self.skapa_celler()
        self.placera_bomber()  
        self.räkna_bomber() 

    def skapa_celler(self):
        self.celler = [[Cell(x,y,self.storlek) for y in range (self.höjd)] for x in range(self.bredd)]

    def placera_bomber(self):
        positioner = random.sample([(x,y) for x in range (self.bredd) for y in range (self.höjd)], self.antal_minor)
        for x, y in positioner:
            self.celler[x][y].mina = True


    def räkna_bomber(self):
        for x in range ( self.bredd):
            for y in range (self.höjd):
                if self.celler[x][y].mina:
                    self.celler[x][y].närheten = -1

                else:
                    antal = 0
                    for i in range (max(0, x-1), min(self.bredd, x+2)): #max gör så att det största värdet tas. tex omm man är längst åt vänster
                        for j in range(max(0, y-1), min(self.höjd, y+2)):
                            if self.celler[i][j].mina:
                                antal += 1

                    self.celler[x][y].närheten = antal

       

    def rita (self,yta):
        for x in range (self.bredd):
            for y in range (self.höjd):
                self.celler [x][y].rita(yta)



class Spel:
    def __init__(self, val, updatera, vinnst, spelplanen):
        self.val = val
        self.updatera = updatera
        self.vinnst = vinnst
        self.spelplanen = spelplanen


plan = Plan(9, 9, 10)
fönster = pygame.display.set_mode((plan.bredd * plan.storlek, plan.höjd * plan.storlek))

fönster.fill((0, 0, 0))
plan.rita(fönster)


pygame.display.flip()

while True:
    for handelse in pygame.event.get():
        if handelse.type == pygame.QUIT:
            exit()



