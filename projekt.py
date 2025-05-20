import pygame
import random
pygame.init()

pygame.mixer.music.load("city-bgm-336601.mp3")  
pygame.mixer.music.play(-1)

def visa_meny(fönster): # funktion för menyn med argument fönster 
    font = pygame.font.SysFont(None, 36)
    fönster.fill((200, 200, 200))

    texter = ["Välj svårighetsgrad:", "1. Lätt", "2. Medel", "3. Svår"] # lista med text
    for i, text in enumerate(texter): #for loop 
        yta = font.render(text, True, (0, 0, 0))
        fönster.blit(yta, (40, 40 + i * 50)) # i så att texten inte är på varandra 

    pygame.display.flip() #uppdateraskärmen

def starta_nytt_spel(nivå_namn): 
    nivå = nivåer[nivå_namn]  # nivån man väljer visas #variabeln nivå_namn får ett värde
    return Plan(nivå["bredd"], nivå["höjd"], nivå["minor"]) # olika värden beroendå på nivå

nivåer = {
"lätt" : {"bredd":9, "höjd":9, "minor": 10}, # dictionary ,lista och värden på allt så att det blir lättare att göra nivåer
"medel": {"bredd":14, "höjd":14, "minor":30}, 
"svår" : {"bredd":18, "höjd":18, "minor":60} 
}

class Cell:
    def __init__(self, x, y, storlek):
        self.x = x # position i x led
        self.y = y # position i y led
        self.storlek = storlek
        self.status = "stängd" #öppen eller ständ cell
        self.markering = False # markerat eller itne
        self.närheten = 0 #minor runt cellen
        self.mina = False  # mina eller inte 
        

    def rita(self, yta):
        färg = (252, 171, 16) if self.status == "stängd" else (255,255,255) #if och else gör att färgen beror på om status är stängd eller inte. så om man klickat eller inte
        if self.markering:#om markerat så ändras färgen till röd
            färg = (255,0,0)

        rect = pygame.Rect(self.x * self.storlek, self.y * self.storlek, self.storlek, self.storlek) #
        pygame.draw.rect(yta, färg, rect)
        pygame.draw.rect(yta, (0, 0, 0), rect, 1) # blir som en svart kant


        if self.markering and self.status == "stängd":
            pygame.draw.circle(yta, (255, 0, 0), rect.center, self.storlek // 4)

            
        elif self.status == "öppen" and self.närheten > 0: #om öppen och öven 1 
            font = pygame.font.SysFont(None, 24)
            text = font.render(str(self.närheten), True, (0, 0, 255)) # om cellen är öppen och har minor runt sig visas det med hjälp av variabeln self.närheten
            yta.blit(text, text.get_rect(center=rect.center))
            
class MineCell(Cell): #arv
    def __init__(self, x, y, storlek):
        super().__init__(x, y, storlek)# ärver Cell klassens postion och storleken, 
        self.mina = True # detta är minorna 
    
    def rita(self, yta):
        super().rita(yta) #funkitonen rita ärver från cell, 
        if self.status == "öppen":
            rect = pygame.Rect(self.x * self.storlek, self.y * self.storlek, self.storlek, self.storlek)
            pygame.draw.circle(yta, (0, 0, 0), rect.center, self.storlek // 3) # man ändrar på funkionen för att lägga till bomb.

class Plan:
    def __init__(self, bredd, höjd, antal_minor ):

        self.bredd = bredd
        self.höjd = höjd
        self.antal_minor = antal_minor
        self.storlek = 30 # cellstorlek, antalet celler gör banan större
        self.skapa_celler()
        self.bomber_placerade = False 
        

    def skapa_celler(self):
        self.celler = [[Cell(x,y,self.storlek) for y in range (self.höjd)] for x in range(self.bredd)] #antal celler på höjd och bredd

    def placera_bomber_efter_klick(self, klick_x, klick_y):
        möjliga_positioner = [(x, y) for x in range(self.bredd) for y in range(self.höjd)
                          if abs(x - klick_x) > 1 or abs(y - klick_y) > 1]  #abs så det bomb inte hamnar på klicket
        positioner = random.sample(möjliga_positioner, self.antal_minor) # random minior på planen. utifrån antelet minor tottalt
        for x, y in positioner:
            self.celler[x][y] = MineCell(x, y, self.storlek)# byter till mincell vilket betycer att det blir en bomb. variabeln self.meina har blivit true
        self.räkna_bomber() # räknar bomber runt varje cell
        self.bomber_placerade = True # minor placerade så inte fler placeras

    

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
    
  
        if cell.närheten == 0: # kollar om det är 0 bomber runt cellen
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



def visa_och_hämta_vald_nivå():
    visa_meny(fönster)  # Visa menyn med texten "Välj svårighetsgrad"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return starta_nytt_spel("lätt") #funktionen avslutas med return. 
                elif event.key == pygame.K_2:
                    return starta_nytt_spel("medel")
                elif event.key == pygame.K_3:
                    return starta_nytt_spel("svår")


fönster = pygame.display.set_mode((400, 300)) # antal pixlar för menyn
plan = visa_och_hämta_vald_nivå() # nivån man tryck på visas
fönster = pygame.display.set_mode((plan.bredd * plan.storlek, plan.höjd * plan.storlek)) # plan visar värdet på funktionen.
#antal pixlar eller celler för spelet beroende på nivån.



pygame.display.flip()

förlorat = False

while True:
    for ändring in pygame.event.get():
        try:
            if ändring.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif not förlorat and ändring.type == pygame.MOUSEBUTTONDOWN: 
                mus_x, mus_y = pygame.mouse.get_pos()
                try:
                    x = mus_x // plan.storlek
                    y = mus_y // plan.storlek
                    cell = plan.celler[x][y]
                except IndexError: #om man klickar på nåogt som "inte finns"
                    print("Klick utanför spelplanen!")
                    continue  #fortsätter och krashar itne om man klickar fel

                if ändring.button == 1:
                    if not plan.bomber_placerade:
                        plan.placera_bomber_efter_klick(x, y)
                        plan.öppna_cell(x, y)
                    else:
                        if cell.mina:
                            cell.status = "öppen"
                            förlorat = True
                            plan.avsluta_spelet() # om man körs funktionen 
                        else:
                            plan.öppna_cell(x, y)

                elif ändring.button == 3:
                    if cell.status == "stängd":
                        cell.markering = not cell.markering

            elif ändring.type == pygame.KEYDOWN:
                if förlorat and ändring.key == pygame.K_r: # om man förlorat och trycker r så kommer man till menyn igen
                    fönster = pygame.display.set_mode((400, 300))
                    plan = visa_och_hämta_vald_nivå()
                    fönster = pygame.display.set_mode((plan.bredd * plan.storlek, plan.höjd * plan.storlek))
                    förlorat = False

        except Exception as e:
            print(f"Ett oväntat fel uppstod: {e}") # e blir som variabel för felmedelandet


    fönster.fill((255, 255, 255))
    plan.rita(fönster)
    
    if förlorat: # om man förlorar så kommer ett medeleande på skärmen skrivas ut 
        höjd = fönster.get_height()
        fontstorlek = max(20, int(höjd * 0.05))
        font = pygame.font.SysFont(None, fontstorlek, bold=True)

        texter = ["BOOOM!! DU FÖRLORADE", "Tryck R för att gå till menyn"]
        padding = fontstorlek // 4
        max_bredd = fönster.get_width() - 20

        total_text_höjd = len(texter) * (fontstorlek + 5)  

        bakgrund_rect = pygame.Rect(
            10,
            (fönster.get_height() - total_text_höjd - 2 * padding) // 2,
            max_bredd,
            total_text_höjd + 2 * padding
        )

        pygame.draw.rect(fönster, (230, 230, 230), bakgrund_rect)
        pygame.draw.rect(fönster, (255, 0, 0), bakgrund_rect, 2)

        for i, rad_text in enumerate(texter):
            text_y = bakgrund_rect.top + padding + i * (fontstorlek + 5)
            text_surf = font.render(rad_text, True, (255, 0, 0))
            text_rect = text_surf.get_rect(center=(fönster.get_width() // 2, text_y + fontstorlek // 2))
            fönster.blit(text_surf, text_rect)



    pygame.display.flip() # visar allt på skärmen

