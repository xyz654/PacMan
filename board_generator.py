import pygame
import sys
import numpy as np

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW_LIGHT = (255, 255, 102)
YELLOW = (255, 255, 0)
GREY = (211,211,211)
ORANGE =(255,69,0)




class BoardGenerator:

    

    def __init__(self,path):
        pygame.init()

        #glowne stale
        self.FPS = 60
        self.screen_width = 700
        self.screen_height = 600

        self.nX = 20 #4
        self.nY = 25 #5

        self.border = 20

        #ogolne wymiary siatki w pixelach
        self.width = self.border*self.nX
        self.height = self.border*self.nY

        #przesuniecia by siatka byla na srodku
        self.dx = (self.screen_width-self.width)/2
        self.dy = (self.screen_height-self.height)/2


        #oknoself.
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        pygame.display.set_caption("Pac-Man board generator")

        # zegar
        self.clock = pygame.time.Clock()


        #glowne zmienne
        self.difficulty=1
        self.difficulty_to_save = 1
        self.isRunning = False
        self.mousePos = pygame.mouse.get_pos()
        self.mouse_is_pressed = False
        self.boardTab=np.zeros((self.nX,self.nY))
        
        #ladowanie planszy
        self.load(path)
        
        #graf poruszania sie pac-mana - reprezentacja macierzowa 
        self.graph=np.zeros((self.nX*self.nY, self.nX*self.nY))

        #lista budowy
        self.buildTab = [False,  #rubber 
                    False,  #wall
                    False,  #floor
                    False,  #big dot
                    False,  #Pac-Man
                    False,   #tunnel
                    False    #duszeki
                    ]  

        self.counters = [0 for el in self.buildTab]

        #wsp tuneli 
        self.t1=np.zeros(2)
        self.t2=np.zeros(2)


    #funkcja ustawiajaca wszytskie wskazniki budowy na False, poza jednym wskazanym w argumencie
    def makeThemAllFalse(self, ind):
        for i in range(len(self.buildTab)):
            if i != ind:
                self.buildTab[i] = False


    def draw_board(self):

        #wypelnianie ekranu kolorem
        self.screen.fill(WHITE)

        #zaznaczanie kwadracika
        if(self.mousePos[0]>=self.dx and self.mousePos[1]>=self.dy and self.mousePos[0]<self.width+self.dx and self.mousePos[1]<self.height+self.dy):
            xk=(self.mousePos[0])-(self.mousePos[0]-self.dx)%self.border
            yk=(self.mousePos[1])-(self.mousePos[1]-self.dy)%self.border
            pygame.draw.rect(self.screen, GREEN, (xk, yk, self.border, self.border))

        #rysowanie siatki
        for x in range(self.nX+1):
            for y in range(self.nY+1):
                pygame.draw.line(self.screen, BLACK, (self.dx+x*self.border, self.dy), (self.dx+x*self.border, self.dy+self.height), 1)
                pygame.draw.line(self.screen, BLACK, (self.dx, self.dy+y*self.border), (self.dx+self.width, self.dy+y*self.border), 1)

        #rysowanie planszy
        for x in range(self.nX):
            for y in range(self.nY):
                #wall
                if self.boardTab[x][y] == 1:
                    pygame.draw.rect(self.screen,BLUE,(self.dx+x*self.border,self.dy+y*self.border,self.border,self.border))
                #floor
                if self.boardTab[x][y] == 2:
                    pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.border,self.dy+y*self.border,self.border,self.border))
                    pygame.draw.circle(self.screen, YELLOW_LIGHT, (self.dx+x*self.border+self.border/2, self.dy+y*self.border+self.border/2), self.border/6)
                #big dot
                if self.boardTab[x][y] == 3:
                    pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.border,self.dy+y*self.border,self.border,self.border))
                    pygame.draw.circle(self.screen, YELLOW_LIGHT, (self.dx+x*self.border+self.border/2, self.dy+y*self.border+self.border/2), self.border/4)
                #Pac-Man
                if self.boardTab[x][y] == 4:
                    pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.border,self.dy+y*self.border,self.border,self.border))
                    pygame.draw.circle(self.screen, YELLOW, (self.dx+x*self.border+self.border/2, self.dy+y*self.border+self.border/2), self.border/3)
                #tunnel
                if self.boardTab[x][y] == 5:
                    pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.border,self.dy+y*self.border,self.border,self.border))
                    pygame.draw.rect(self.screen, RED, (self.dx+x*self.border+self.border/4,self.dy+y*self.border+self.border/4,self.border/2,self.border/2))
                #duszek
                if self.boardTab[x][y] == 6:
                    pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.border,self.dy+y*self.border,self.border,self.border))
                    pygame.draw.circle(self.screen, ORANGE, (self.dx+x*self.border+self.border/2, self.dy+y*self.border+self.border/2), self.border/3)
                
        #rysowanie legendy
        font = pygame.font.Font('freesansbold.ttf', 20)
        font1=pygame.font.Font('freesansbold.ttf', 10)
        text = font.render('Legend', True, BLACK, WHITE)
        wall=font1.render('to set wall press: W', True, BLACK, WHITE)
        pacman=font1.render('to set pacman press: P', True, BLACK, WHITE)
        rubber=font1.render('to get rubber press: X', True, BLACK, WHITE)
        floor=font1.render('to set floor press: Q', True, BLACK, WHITE)
        tunel=font1.render('to set tunel press: R', True, BLACK, WHITE)
        bigdot=font1.render('to set BigDot press: E', True, BLACK, WHITE)
        ghosts=font1.render('to set Ghosts press: G', True, BLACK, WHITE)


        textRect = text.get_rect()
        textRect.center = (self.dx//2, self.dy)
        self.screen.blit(text, textRect)
        self.screen.blit(wall,(self.dx//8, 1.5*self.dy))
        self.screen.blit(pacman,(self.dx//8, 2*self.dy))
        self.screen.blit(rubber,(self.dx//8,2.5*self.dy))
        self.screen.blit(floor,(self.dx//8, 3*self.dy))
        self.screen.blit(tunel,(self.dx//8, 3.5*self.dy))
        self.screen.blit(bigdot,(self.dx//8, 4*self.dy))
        self.screen.blit(ghosts,(self.dx//8, 4.5*self.dy))

        #wyswietlanie statystyk 

        stats = font.render('Statystics', True, BLACK, WHITE)
        wallStats=font1.render("Walls:  "+(str)(self.counters[1]), True, BLACK, WHITE)
        pacmanStats=font1.render("Pacman: " +(str)(self.counters[4])+ "/1", True, BLACK, WHITE)
        floorStats=font1.render('Floor:  '+(str)(self.counters[2]), True, BLACK, WHITE)
        tunelStats=font1.render('Tunels: '+(str)(self.counters[5])+ "/2", True, BLACK, WHITE)
        bigdotStats=font1.render('Big dots: '+(str)(self.counters[3]), True, BLACK, WHITE)
        ghostsStats=font1.render('Ghosts: '+(str)(self.counters[6])+ "/4", True, BLACK, WHITE)


        statsRect = stats.get_rect()
        statsRect.center = (self.dx//2, 5.5*self.dy)

        self.screen.blit(stats,statsRect)
        self.screen.blit(wallStats,(self.dx//8, 6*self.dy))
        self.screen.blit(pacmanStats,(self.dx//8, 6.5*self.dy))
        self.screen.blit(floorStats,(self.dx//8, 7*self.dy))
        self.screen.blit(tunelStats,(self.dx//8, 7.5*self.dy))
        self.screen.blit(bigdotStats,(self.dx//8, 8*self.dy))
        self.screen.blit(ghostsStats,(self.dx//8, 8.5*self.dy))



        #dodawanie przycisku zapisz
        pygame.draw.rect(self.screen,GREY,((self.width+self.dx+20),self.height+self.dy-40,100,30),0,10)
        pygame.draw.rect(self.screen,BLACK,((self.width+self.dx+20),self.height+self.dy-40,100,30),1,10)

        save=font1.render('SAVE', True, BLACK, GREY)
        self.screen.blit(save,((self.width+self.dx+60), self.height+self.dy-30))


    def build(self):
        #pobieranie miejsca indeksu w tab myszki
        i=(int)(self.mousePos[0]-self.dx)//self.border
        j=(int)(self.mousePos[1]-self.dy)//self.border

        #jesli kursor jest poza polem, to wychodze z funkcji
        if i < 0 or j < 0 or i >= self.nX or j >= self.nY:
            return
        
        #buduje tylko jesli myszka jest wcisniete
        if self.mouse_is_pressed:
            #przechodze po wszystkich mozliwosciach bycia wcisnietym
            for ind in range(len(self.buildTab)):
                #jesli jest cos wcisniete to to buduje
                if self.buildTab[ind]:
                    #jesli nie jestem gumka a dame pole to sciana to wychodze
                    if self.boardTab[i][j] == 1 and ind != 0: return

                    #jesli chce postawic pacmana albo tunel albo duszki to sprawdzam czy jeszcze moge je wgl wstawic i jak nie to wychodze
                    if (ind==4 and self.counters[4]>0) or (ind==5 and self.counters[5]>1) or (ind==6 and self.counters[6]>3): return

                    #jesli chce postawic tunel to musi byc na brzegach ale nie w rogu!, jak nie to wychodze
                    if ind==5 and i != 0 and i != self.nX-1 and j != 0 and j != self.nY-1: return

                    #jesli chce postawic tunel to nie moze byc w rogu!, jak nie to wychodze

                    if ind==5 and ((i==0 and j==0) or (i==0 and j==self.nY-1) or (i==self.nX-1 and j==0) or (i==self.nX-1 and j==self.nY-1)): return

                    #jesli nie ma podlogi a chce polozyc: duza kropke, pacmana, duszka, to wychodze
                    if self.boardTab[i][j] != 2 and (ind==3 or ind==4 or ind==6): return    

                    #jesli chce postawic podloge, to nie moze byc na skraju
                    if ind==2 and (i==0 or j==0 or i==self.nX-1 or j==self.nY-1): return

                    #jesli cos tam jest to zmniejszam counter czegos co nadpisuje
                    if(int(self.boardTab[i][j]) != 0):
                        self.counters[int(self.boardTab[i][j])] -= 1

                    if ind==0: #jesli jestem gumka trzeba sprawdzic co chce zmazac - czy tunel
                        if self.boardTab[i][j]==5:
                            if self.counters[5]==0: #byl tylko jeden
                                self.t1[0]=0
                                self.t1[1]=0
                            else: #byly dwa - trzeba sie dowiedziec ktory usuwam
                                if self.t1[0]==i and self.t1[1]==j: #chce usunac t1
                                    #przepisuje dane do t1 i usuwam t2
                                    self.t1[0]=self.t2[0]
                                    self.t1[1]=self.t2[1]
                                    self.t2[0]=0
                                    self.t2[1]=0
                                else: #chce usunac t2
                                    self.t2[0]=0
                                    self.t2[1]=0
                    
                    self.boardTab[i][j] = ind
                    self.counters[ind] += 1
    
                    #wychodze z petli no bo raczej juz reszta jest False
                    return


    def makeGraph(self):
        for i in range(self.nX):
            for j in range(self.nY):
                #jezeli jest tam podloga - to dodaje do grafu
                if self.boardTab[i][j]==2:
                    #lewo
                    if self.boardTab[i-1][j]==2:
                        self.graph[j*self.nX+i][j*self.nX+i-1]=1
                        self.graph[j*self.nX+i-1][j*self.nX+i]=1
                    #prawo
                    if self.boardTab[i+1][j]==2: 
                        self.graph[j*self.nX+i][j*self.nX+i+1]=1
                        self.graph[j*self.nX+i+1][j*self.nX+i]=1
                    #gora
                    if self.boardTab[i][j-1]==2:
                        self.graph[j*self.nX+i][(j-1)*self.nX+i]=1
                        self.graph[(j-1)*self.nX+i][j*self.nX+i]=1
                    #dol
                    if self.boardTab[i][j+1]==2:
                        self.graph[j*self.nX+i][(j+1)*self.nX+i]=1
                        self.graph[(j+1)*self.nX+i][j*self.nX+i]=1

                #obsluga tuneli
                if self.boardTab[i][j]==5 and self.counters[5]==2:
                    self.graph[(int)(self.t1[1]*self.nX+self.t1[0])][(int)(self.t2[1]*self.nX+self.t2[0])]=1
                    self.graph[(int)(self.t2[1]*self.nX+self.t2[0])][(int)(self.t1[1]*self.nX+self.t1[0])]=1

    
    def save(self):
        path = filedialog.asksaveasfile(defaultextension=".npy")
        if path != None:
            with open(path.name, 'wb') as f:
                for i in range(self.nX):
                    for j in range(self.nY):
                        np.save(f, np.array([self.boardTab[i][j]]))
                np.save(f, np.array([self.difficulty_to_save]))
    
    def load(self, path):
        if len(path)!=0:
            with open(path, 'rb') as f:
                for i in range(self.nX):
                    for j in range(self.nY):
                        self.boardTab[i][j]=np.load(f)[0]

    def prepareToSave(self):
        #funkcja do obslugi slidera
        def countSlider(event):
            self.difficulty_to_save = int(round(self.difficulty.get(), 0))
            sliderLabel.config(text="Current difficulty: "+str(self.difficulty_to_save))

        #tworze okno
        root = tk.Tk()
        #ustawiam tytul
        root.title("Prepare to save")

        #rozmiary
        window_width = 700
        window_height = 600

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        centerX = int(screen_width/2 - window_width/2)
        centerY = int(screen_height/2 - window_height/2)

        root.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')

        #mozliwosc zmiany rozmiaru
        root.resizable(True, True)

        #widgety
        ttk.Label(root, text='Fill the details:').pack()
        ttk.Label(root, text="Set the difficulty:").pack()
        self.difficulty = tk.DoubleVar()
        slider = ttk.Scale(
                            root,
                            from_=1,
                            to=5,
                            orient='horizontal', 
                            variable=self.difficulty,
                            command=countSlider
                        )
        slider.pack()

        sliderLabel = ttk.Label(root, text="Current difficulty: "+str(self.difficulty_to_save))
        sliderLabel.pack()


        ttk.Button(root, text="Save", command=self.save).pack()

        root.mainloop()


    def run(self):

        #glowna petla
        self.isRunning = True
        while self.isRunning:

            #pobieranie pozycji myszki
            self.mousePos = pygame.mouse.get_pos()


            #rysowanie 
            self.draw_board()

            #budowanie
            self.build()


            #przyciski
            x=(int)(self.mousePos[0]-self.width-self.dx-20)
            y=(int)(self.mousePos[1]-(self.height+self.dy-40))

            if self.mouse_is_pressed and x>0 and x<100 and y>0 and y<30:
                #zapisz
                self.makeGraph()
                self.isRunning = False 

            
            #przechwytywanie zdarzen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #keydowny
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #LPM
                    if event.button == 1:
                        self.mouse_is_pressed = True

                if event.type == pygame.KEYDOWN:
                    #rubber
                    if event.key == pygame.K_x:
                        self.makeThemAllFalse(0)
                        self.buildTab[0] = not self.buildTab[0]
                    #wall
                    if event.key == pygame.K_w:
                        self.makeThemAllFalse(1)
                        self.buildTab[1] = not self.buildTab[1]
                    #floor
                    if event.key == pygame.K_q:
                        self.makeThemAllFalse(2)
                        self.buildTab[2] = not self.buildTab[2]
                    #big dot
                    if event.key == pygame.K_e:
                        self.makeThemAllFalse(3)
                        self.buildTab[3] = not self.buildTab[3]
                    #Pac-Man
                    if event.key == pygame.K_p:
                        self.makeThemAllFalse(4)
                        self.buildTab[4] = not self.buildTab[4]
                    #tunnel
                    if event.key == pygame.K_r:
                        self.makeThemAllFalse(5)
                        self.buildTab[5] = not self.buildTab[5]
                    #duszki
                    if event.key == pygame.K_g:
                        self.makeThemAllFalse(6)
                        self.buildTab[6] = not self.buildTab[6]
                

                #keyupy
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_is_pressed = False
            
            #odswiezanie okna
            pygame.display.update()
            #kontroluje FPS
            self.clock.tick(self.FPS)
        
        #dalsze kroki
        if not self.isRunning:
            pygame.quit()
            self.prepareToSave()
                

     
# bo = BoardGenerator([])
# bo.run()