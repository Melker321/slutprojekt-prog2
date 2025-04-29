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
        for x in range (self.bredd):
            for y in range (self.höjd):
                cell = self.celler[x][y]

        rect = pygame.Rect(x * cell.storlek, y * cell.storlek, cell.storlek, cell.storlek)


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



fönster = pygame.display.set_mode((640, 480))   

fönster.fill((0,0,0))

plan = Plan(9, 9, 10) 
plan.rita(fönster) 


pygame.display.flip()

while True:
    for handelse in pygame.event.get():
        if handelse.type == pygame.QUIT:
            exit()



