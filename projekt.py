import pygame
import random
pygame.init()

nivåer = {
"lätt" : {"bredd":9, "höjd":9, "minor": 10},
"medel": {"bredd":14, "höjd":14, "minor":40},
"svår" : {"bredd":18, "höjd":18, "minor":100} 
}

class Cell:
    def __init__(self, x, y, storlek):
        self.x = x
        self.y = y
        self.storlek = storlek
        self.status = "stängd"
        self.markering = False
        self.närheten = 0
        self.mina = False 
        

    def rita(self, yta):
        färg = (252, 171, 16) if self.status == "stängd" else (255,255,255) #if och else gör att färgen beror på om status är stängd eller inte
        if self.markering:#om markerat så ändras färgen.
            färg = (255,0,0)

        rect = pygame.Rect(self.x * self.storlek, self.y * self.storlek, self.storlek, self.storlek)
        pygame.draw.rect(yta, färg, rect)
        pygame.draw.rect(yta, (0, 0, 0), rect, 1)


        if self.markering and self.status == "stängd":
            pygame.draw.circle(yta, (255, 0, 0), rect.center, self.storlek // 4)

            
        elif self.status == "öppen" and self.närheten > 0:
            font = pygame.font.SysFont(None, 24)
            text = font.render(str(self.närheten), True, (0, 0, 255))
            yta.blit(text, text.get_rect(center=rect.center))
            
class MineCell(Cell):
    def __init__(self, x, y, storlek):
        super().__init__(x, y, storlek)
        self.mina = True
    
    def rita(self, yta):
        super().rita(yta)
        if self.status == "öppen":
            rect = pygame.Rect(self.x * self.storlek, self.y * self.storlek, self.storlek, self.storlek)
            pygame.draw.circle(yta, (0, 0, 0), rect.center, self.storlek // 3)

class Plan:
    def __init__(self, bredd, höjd, antal_minor ):

        self.bredd = bredd
        self.höjd = höjd
        self.antal_minor = antal_minor
        self.storlek = 30
        self.skapa_celler()
        self.bomber_placerade = False 
        

    def skapa_celler(self):
        self.celler = [[Cell(x,y,self.storlek) for y in range (self.höjd)] for x in range(self.bredd)]

    def placera_bomber_efter_klick(self, klick_x, klick_y):
        möjliga_positioner = [(x, y) for x in range(self.bredd) for y in range(self.höjd)
                          if abs(x - klick_x) > 1 or abs(y - klick_y) > 1]  #abs så det bomb inte hamnar på klicket
        positioner = random.sample(möjliga_positioner, self.antal_minor)
        for x, y in positioner:
            self.celler[x][y] = MineCell(x, y, self.storlek)
        self.räkna_bomber()
        self.bomber_placerade = True

    

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

    def öppna_cell(self, x, y):
        cell = self.celler[x][y]
        if cell.status == "öppen" or cell.markering:
            return  
    
        cell.status = "öppen"
    
  
        if cell.närheten == 0:
            for i in range(max(0, x-1), min(self.bredd, x+2)):
                for j in range(max(0, y-1), min(self.höjd, y+2)):
                    if i == x and j == y:
                        continue
                    self.öppna_cell(i, j)


    def avsluta_spelet(self):
    
        for x in range(self.bredd):
            for y in range(self.höjd):
                if self.celler[x][y].mina:
                    self.celler[x][y].status = "öppen"

       

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



pygame.display.flip()

förlorat = False

while True:
    for ändring in pygame.event.get():
        if ändring.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif not förlorat and ändring.type == pygame.MOUSEBUTTONDOWN: # om spslet inte är förlorat och musen klickas
            mus_x, mus_y = pygame.mouse.get_pos()
            x = mus_x // plan.storlek
            y = mus_y // plan.storlek # // så rätt pixel och ruta klickas
            cell = plan.celler[x][y]

            if ändring.button == 1:  
                if not plan.bomber_placerade:
                    plan.placera_bomber_efter_klick(x, y)
                    plan.öppna_cell(x, y)  
                else:
                    if cell.mina:
                        cell.status = "öppen"
                        förlorat = True
                        plan.avsluta_spelet()
                    else:
                        cell.status = "öppen"

            elif ändring.button == 3: 
                if cell.status == "stängd":
                    cell.markering = not cell.markering

    fönster.fill((255, 255, 255))
    plan.rita(fönster)
    
    if förlorat:
      
        font = pygame.font.SysFont(None, 20)
        text = font.render("BOOOM!! DU FÖRLORADE Tryck R för att börja om", True, (255, 0, 0))
        fönster.blit(text, (20, 20))

    pygame.display.flip()

    
    tangenter = pygame.key.get_pressed()
    if förlorat and tangenter[pygame.K_r]:
        plan = Plan(9, 9, 10)
        förlorat = False
        fönster = pygame.display.set_mode((plan.bredd * plan.storlek, plan.höjd * plan.storlek))
