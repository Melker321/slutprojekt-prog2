import pygame
import random
pygame.init()

# Svårighetsnivåer
nivåer = {
    "lätt": {"bredd": 9, "höjd": 9, "minor": 10},
    "medel": {"bredd": 14, "höjd": 14, "minor": 40},
    "svår": {"bredd": 18, "höjd": 18, "minor": 100}
}

# Cellklass
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
        färg = (200, 200, 200) if self.status == "stängd" else (150, 150, 150)
        if self.markering:
            färg = (255, 0, 0)  # röd om markerad

        rect = pygame.Rect(self.x * self.storlek, self.y * self.storlek, self.storlek, self.storlek)
        pygame.draw.rect(yta, färg, rect)
        pygame.draw.rect(yta, (0, 0, 0), rect, 1)  # svart kant runt cell

# Spelplan
class Plan:
    def __init__(self, bredd, höjd, antal_minor):
        self.bredd = bredd
        self.höjd = höjd
        self.antal_minor = antal_minor
        self.storlek = 30  # storlek på varje ruta i pixlar
        self.celler = [[Cell(x, y, self.storlek) for y in range(höjd)] for x in range(bredd)]

    def rita(self, yta):
        for x in range(self.bredd):
            for y in range(self.höjd):
                self.celler[x][y].rita(yta)

# Spelklass (inte använd ännu)
class Spel:
    def __init__(self, val, updatera, vinnst, spelplanen):
        self.val = val
        self.updatera = updatera
        self.vinnst = vinnst
        self.spelplanen = spelplanen

# Välj nivå
nivå = nivåer["lätt"]  # Byt till "medel" eller "svår" om du vill testa andra

# Skapa spelplan
plan = Plan(nivå["bredd"], nivå["höjd"], nivå["minor"])

# Skapa fönster baserat på storlek
fönster = pygame.display.set_mode((plan.bredd * plan.storlek, plan.höjd * plan.storlek))
pygame.display.set_caption("Minesweeper")

# Fyll bakgrunden
fönster.fill((0, 0, 0))
plan.rita(fönster)
pygame.display.flip()

# Spelloop
while True:
    for handelse in pygame.event.get():
        if handelse.type == pygame.QUIT:
            exit()
