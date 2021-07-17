import time
import pygame, sys
from pygame.locals import *
import random
import pickle

XMAX = 1250
YMAX = 750
XRAND = 80
YRAND = 75
STEIN_ABSTANDX = 4
STEIN_ABSTANDY = 4
ZEILEN = 8
SPALTEN = 18
EBENEN = 5
DXYEBENE = 5
#HINTERGRUND = (50,50,100)
HINTERGRUND = (150,150,00)
BUTTON = (100,100,100)
MISCHENSCHRIFT = (0,0,0)
SELECTCOLOR = pygame.Color(0,255,0,50)

class Stein:
    nr = 0
    ebene = 0
    spalte = 0
    zeile = 0
    rect = None
    image = None
    sichtbar = False
    select = False

    def __init__(self, nr, image):
        self.nr = nr
        self.image = image
        self.rect = pygame.Rect(0,0,0,0)
    pass

    def setRect(self, left, top, sizex, sizey):
        self.rect = pygame.Rect(left,top,sizex,sizey)
    pass

    def setEbeneZeileSpalte(self, ebene, zeile, spalte):
        self.spalte = spalte
        self.zeile = zeile
        self.ebene = ebene
    pass
pass

class Mahjong:
    liste = []
    stein_gruppen = ()
    felder = []
    anz_ebenen = 0
    EBENEN = 0
    ZEILEN = 0
    SPALTEN = 0
    BILDBREITE = 0
    BILDHOEHE = 0
    DXYEBENE = 0
    STEIN_ABSTANDX = 0
    STEIN_ABSTANDY = 0
    BORDERBREITE = 0

    def __init__(self, steine, ebenen, zeilen, spalten, dxyebene, stein_abstandx, stein_abstandy):
        self.liste = steine[0]
        self.stein_gruppen = steine[1]
        self.EBENEN = ebenen
        self.ZEILEN = zeilen
        self.SPALTEN = spalten
        self.BILDBREITE = steine[2]
        self.BILDHOEHE = steine[3]
        self.BORDERBREITE = steine[4]
        self.DXYEBENE = dxyebene
        self.STEIN_ABSTANDX = stein_abstandx
        self.STEIN_ABSTANDY = stein_abstandy
        self.reset()
    pass

    def reset(self):
    #Felder mit leeren Steinobjekten initialisieren
        self.felder = []
        for z in range(self.EBENEN):
            new_feld = []
            for i in range(self.ZEILEN):
                new_line = []
                for j in range(self.SPALTEN):
                    new_line.append(Stein(-1, None))
                pass
                new_feld.append(new_line)
            pass
            self.felder.append(new_feld)
        pass
        #Liste mischen
        random.seed()
        random.shuffle(self.liste)
        #Auswahl der Figur
        rnd = random.randint(0,90)
        if rnd < 30:
            self.figur_laden("figur1.txt")
        elif rnd >= 30 and rnd < 60:
            self.figur_laden("figur2.txt")
        elif rnd >= 60:
            self.figur_laden("figur3.txt")
        pass
    pass

    def figur_laden(self, name):
    #Figur aus Text-Datei lesen und Felder mit Steinobjekten aus der Steinliste füllen
        datei = open(name, "r")
        n = 0
        zeile = 0
        self.anz_ebenen = 0
        for line in datei:
            spalte = 0
            for nr in range(len(line)-1):
                max_ebene = line[nr]
                if int(max_ebene) > self.anz_ebenen:
                    self.anz_ebenen = int(max_ebene)
                pass
                for ebene in range(int(max_ebene)+1):
                    if ebene > 0:
                        self.felder[ebene-1][zeile][spalte] = self.liste[n]
                        self.felder[ebene-1][zeile][spalte].sichtbar = True
                        n+=1
                    pass
                pass
                spalte+=1
            pass
            zeile+=1
        pass
        datei.close()
        for ebene in range(self.anz_ebenen):
            self.init_steine(ebene, (ebene)*self.DXYEBENE)
        pass
    pass

    def zugOK(self, stein):
        if stein == None:
            return False
        if not self.felder[stein.ebene][stein.zeile][stein.spalte+1].sichtbar or not self.felder[stein.ebene][stein.zeile][stein.spalte-1].sichtbar:
            return True
        else:
            return False
        pass
    pass

    def find_gruppe(self,x):
    #Zu welcher Gruppe gehört x
        for item in self.stein_gruppen:
            if x in item:
                return(item)
            pass
        pass
    pass

    def find_stein(self,x,y):
    #Liefert den Stein an der geklickten Positiom
        for ebene in range(self.EBENEN-1,-1,-1):
            for z in range(self.ZEILEN):
                for s in range(self.SPALTEN):
                    if self.felder[ebene][z][s].rect.collidepoint(x,y) and self.felder[ebene][z][s].sichtbar:
                        return self.felder[ebene][z][s]
                    pass
                pass
            pass
        pass
        return None
    pass

    def init_steine(self, ebene, v):
        #Steine mischen
        for z in range(self.ZEILEN):
            for s in range(self.SPALTEN):
                if self.felder[ebene][z][s].sichtbar:
                    z1=random.randint(0,ZEILEN-1)
                    s1=random.randint(0,SPALTEN-1)
                    while not self.felder[ebene][z1][s1].sichtbar:
                        z1=random.randint(0,ZEILEN-1)
                        s1=random.randint(0,SPALTEN-1)
                    pass
                    h = self.felder[ebene][z][s]
                    self.felder[ebene][z][s] = self.felder[ebene][z1][s1]
                    self.felder[ebene][z1][s1] = h  
                pass
            pass
        pass
        #In Steinen rect, spalte, zeile setzen. Steine auf Ebenen > 0 um v verschieben
        for ze in range(0,self.ZEILEN):
            for sp in range(0,self.SPALTEN):
                if self.felder[ebene][ze][sp].sichtbar:
                    self.felder[ebene][ze][sp].setRect(v + XRAND+sp*(self.BILDBREITE-self.STEIN_ABSTANDX), v + YRAND+ze*(self.BILDHOEHE-self.STEIN_ABSTANDY), self.BILDBREITE-self.BORDERBREITE, self.BILDHOEHE-self.BORDERBREITE)
                    self.felder[ebene][ze][sp].setEbeneZeileSpalte(ebene,ze,sp)
                pass
            pass
        pass
    pass

    def draw_rect_alpha(self, surface, color, rect):
        #Selectierten Stein grün einfärben
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)
    pass

pass

def animation():
    #Spielfeld animiert aufbauen
    for ebene in range(game.EBENEN):
        for ze in range(0,game.ZEILEN):
            for sp in range(0,game.SPALTEN):
                if game.felder[ebene][ze][sp].sichtbar:
                    surf_array = pygame.surfarray.make_surface(game.felder[ebene][ze][sp].image)
                    surf_array.set_colorkey((255,0,255))
                    surf.blit(surf_array,(game.felder[ebene][ze][sp].rect.left,game.felder[ebene][ze][sp].rect.top))
                    pygame.display.flip()
                    time.sleep(0.05)
                pass
            pass
        pass
    pass
pass

#Start Hauptprogramm
pygame.init()
FPS = 30
fspClock = pygame.time.Clock()
surf = pygame.display.set_mode((XMAX, YMAX))
#surf.set_colorkey((255,0,255))
surf.fill(HINTERGRUND)
pygame.display.set_caption("Mahjong 1.4")
#Datei mit Steindaten laden
f = open("steine.bin", "rb")
stein_daten = pickle.load(f)
#Mahjong-Object initialisieren
game = Mahjong(stein_daten, EBENEN, ZEILEN, SPALTEN, DXYEBENE, STEIN_ABSTANDX, STEIN_ABSTANDY)
f.close()
font = pygame.font.Font(pygame.font.get_default_font(), 25)
SteinSelect = None
punkte = 0
start_minuten = int(time.time()/60)
minuten = 1
gemischt = 0
#Buttonobjekte definieren
buttonQuit = pygame.Rect(XMAX-3*XRAND,YRAND+370,130,50)
buttonStart = pygame.Rect(XMAX-3*XRAND,YRAND+430,130,50)
buttonMischen = pygame.Rect(XMAX-3*XRAND,YRAND+490,130,50)
animation()

#Gameloop
while True:
    surf.fill(HINTERGRUND)
    #Steinfelder zeichnen/aktualsieren
    for ebene in range(game.EBENEN):
        for ze in range(0,game.ZEILEN):
            for sp in range(0,game.SPALTEN):
                if game.felder[ebene][ze][sp].sichtbar:
                    surf_array = pygame.surfarray.make_surface(game.felder[ebene][ze][sp].image)
                    surf_array.set_colorkey((255,0,255))
                    surf.blit(surf_array,(game.felder[ebene][ze][sp].rect.left,game.felder[ebene][ze][sp].rect.top))
                    if game.felder[ebene][ze][sp].select:
                        game.draw_rect_alpha(surf, SELECTCOLOR, game.felder[ebene][ze][sp].rect)
                    pass
                pass
            pass
        pass
    pass
    #Benutzer-Events bearbeiten
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            stein = game.find_stein(mousex, mousey)
            if game.zugOK(stein):
                if SteinSelect == None:
                    SteinSelect = stein
                    SteinSelect.select = True
                else:
                    if stein.nr in game.find_gruppe(SteinSelect.nr) and stein.nr != SteinSelect.nr:
                        game.felder[SteinSelect.ebene][SteinSelect.zeile][SteinSelect.spalte].sichtbar = False
                        game.felder[stein.ebene][stein.zeile][stein.spalte].sichtbar = False
                        punkte += 30
                    pass
                    SteinSelect.select = False
                    SteinSelect = None
                    stein = None
                pass
            else:
                if SteinSelect != None:
                    SteinSelect.select = False
                    SteinSelect = None
                pass
            pass
            if buttonQuit.collidepoint(mousex, mousey):
                pygame.quit()
                sys.exit()
            pass
            if buttonMischen.collidepoint(mousex, mousey) and gemischt < 3:
                for ebene in range(game.anz_ebenen):
                    game.init_steine(ebene, (ebene)*DXYEBENE)
                pass
                gemischt+=1
                if gemischt == 3:
                    MISCHENSCHRIFT = (80,80,80)
                pass
            pass
            if buttonStart.collidepoint(mousex, mousey):
                punkte = 0
                start_minuten = int(time.time()/60)
                minuten = 1
                gemischt = 0
                MISCHENSCHRIFT = (0,0,0)
                SteinSelect = None
                surf.fill(HINTERGRUND)
                game.reset()
                animation()
            pass
        pass
    pass
    #Buttons und Punktestand zeichnen
    pygame.draw.rect(surf,BUTTON,buttonQuit)
    surf.blit(font.render("Ende", True, (0, 0, 0)), dest=(buttonQuit.left+15,buttonQuit.top+15))
    pygame.draw.rect(surf,BUTTON,buttonStart)
    surf.blit(font.render("Neu", True, (0, 0, 0)), dest=(buttonStart.left+15,buttonStart.top+15))
    pygame.draw.rect(surf,BUTTON,buttonMischen)
    surf.blit(font.render("Mischen", True, MISCHENSCHRIFT), dest=(buttonMischen.left+15,buttonMischen.top+15))
    surf.blit(font.render("Punkte = " + str(int(punkte/minuten)), True, BUTTON), dest=(XMAX-3*XRAND,YRAND))
    if punkte == 2160:
        surf.blit(font.render("Super geschafft !!!", True, (255, 0, 0)), dest=(XMAX-3*XRAND,YRAND+90))
    else:
        minuten = int(time.time()/60)-start_minuten
    if minuten == 0:
        minuten = 1
    surf.blit(font.render("Minuten = " + str(minuten), True, BUTTON), dest=(XMAX-3*XRAND,YRAND+30))
    
    #Update Gameloop
    pygame.display.update()
    fspClock.tick(FPS)
pass