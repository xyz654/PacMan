import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import board_generator as bg
import main
import numpy as np
from os import listdir
from os.path import isfile, join
import random

class Menu:

    

    def __init__(self):
        self.difficulty=1
        self.difficulty_to_save = 1

        # #tworze okno
        # self.subroot = None

            #tworze okno
        self.root = tk.Tk()

        
        #ustawiam tytul
        self.root.title("Pac-Man")

        #rozmiary
        window_width = 700
        window_height = 600

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        centerX = int(screen_width/2 - window_width/2)
        centerY = int(screen_height/2 - window_height/2)

        self.root.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')

        #mozliwosc zmiany rozmiaru
        self.root.resizable(True, True)

        #widgety
        ttk.Label(self.root, text='Welcome to Pac-Man!').pack()
        ttk.Button(self.root, text='Play!', command=self.start).pack()
        ttk.Button(self.root, text='Create new board!', command=self.runNewGenerator).pack()
        ttk.Button(self.root, text='Load draft board!', command=self.runDraftGenerator).pack()
        ttk.Button(self.root, text='Exit', command=exit).pack()  

        self.root.mainloop()


    def runNewGenerator(self):
        #zamykam okno
        self.root.destroy()
        #otwieram generator
        bo = bg.BoardGenerator([])
        bo.run()
        
    def runDraftGenerator(self):
        #pobieram sciezke
        path = filedialog.askopenfile(initialdir="./maps")
        if path!=None:
            file_extension = os.path.splitext(path.name)[1]
            if file_extension == ".npy":
                #zamykam okno
                self.root.destroy()
                #otwieram generator
                bo = bg.BoardGenerator(path.name)
                bo.run()

    def loadData(self,path):
        #pobieram dane z pliku
        with open(path, 'rb') as f:
            #zbieranie statystyk
            stats = np.load(f)
            return stats



    def runGame(self):
        path = filedialog.askopenfile(initialdir="./maps")
        if path!=None:
            file_extension = os.path.splitext(path.name)[1]
            if file_extension == ".npy":
                #gdy loadData zwroci 0 - jest git
                if self.loadData(path.name)[3]==0:
                    #zamykam okno
                    self.root.destroy()
                    #uruchamiam gre ale najpierw sprawdze czy nie jest wersja robocza
                    game = main.Game(path.name)
                    game.run()
                else:
                    #tworze okno
                    root2 = tk.Tk()

                    #rozmiary
                    window_width = 250
                    window_height = 50

                    root2.title("Draft board")

                    screen_width = root2.winfo_screenwidth()
                    screen_height = root2.winfo_screenheight()

                    centerX = int(screen_width/2 - window_width/2)
                    centerY = int(screen_height/2 - window_height/2)

                    root2.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')


                    #widgety
                    ttk.Label(root2, text='Cannot play, it is the draft board').pack()
                    ttk.Button(root2, text='OK!', command=root2.destroy).pack()


                    self.root.mainloop()
    
    def randomMap(self):
        #get all maps
        onlyfiles = [f for f in listdir("./maps") if isfile(join("./maps", f))]
        generator=[]
        for map in onlyfiles:
            currentStats=self.loadData("maps/"+map)
            #jesli nie jest wersja roboczca to dodaje do losowania
            if currentStats[3]==0:
                generator.append(map)
        #losowo wybieram mape
        x=random.choice(generator)
        # subroot.destroy()
        print("./maps/"+x)
        game = main.Game("./maps/"+x)
        game.run()

    def levelMap(self):
        #get all maps
        onlyfiles = [f for f in listdir("./maps") if isfile(join("./maps", f))]
        generator=[]
        for map in onlyfiles:
            currentStats=self.loadData("maps/"+map)
            #jesli nie jest wersja roboczca to dodaje do losowania
            if currentStats[3]==0 and currentStats[0]==self.difficulty_to_save:
                generator.append(map)
        #sprawdzenie czy jest taki level dostepny
        if len(generator)==0:
            #tworze okno
            root2 = tk.Tk()

            #rozmiary
            window_width = 250
            window_height = 50

            root2.title("No maps")

            screen_width = root2.winfo_screenwidth()
            screen_height = root2.winfo_screenheight()

            centerX = int(screen_width/2 - window_width/2)
            centerY = int(screen_height/2 - window_height/2)

            root2.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')


            #widgety
            ttk.Label(root2, text='No maps with this level, you can create your own one').pack()
            ttk.Button(root2, text='OK!', command=root2.destroy).pack()
        else:
            #losowo wybieram mape
            x=random.choice(generator)
            # subroot.destroy()
            game = main.Game("maps/"+x)
            game.run()

    def specificMap(self):

        generator=[]
        def sortNames():
            generator.sort()
            i=1
            listbox.delete(0,tk.END)
            for elem in generator:
                listbox.insert(i, "{:<10s}  {:>2f} {:<5d} ".format(elem[0], elem[1], elem[2]) )
                i+=1
        def sortDescLevel():
            generator_sort=sorted(generator,key=lambda x: x[1], reverse=True)
            print(generator_sort)
            i=1
            listbox.delete(0,tk.END)
            for elem in generator_sort:
                listbox.insert(i, "{:<10s}  {:>2f} {:<5d} ".format(elem[0], elem[1], elem[2]) )
                i+=1
        def sortAscLevel():
            generator_sort=sorted(generator,key=lambda x: x[1], reverse=False)
            print(generator_sort)
            i=1
            listbox.delete(0,tk.END)
            for elem in generator_sort:
                listbox.insert(i, "{:<10s}  {:>2f} {:<5d} ".format(elem[0], elem[1], elem[2]) )
                i+=1
        onlyfiles = [f for f in listdir("./maps") if isfile(join("./maps", f))]
        
        #statystyki
        stats = np.array([])
        with open("./mapStats.npy", 'rb') as f:
            #zbieram nazwe aktualnej planszy
            stats = np.load(f)
            for map in onlyfiles:
                currentStats=self.loadData("maps/"+map)
            #jesli nie jest wersja roboczca to dodaje do losowania
                if currentStats[3]==0:
                    statystics=0
                    for stat in stats:
                        print("statystykiii", stat[0], map)
                        if stat[0] == map:
                            statystics=int(stat[1])
                    if statystics:
                        generator.append((map,currentStats[0],statystics))
                    else:
                        generator.append((map,currentStats[0],0))
            f.close()

        
        #sprawdzenie czy jest taki level dostepny
        if len(generator)==0:
            #tworze okno
            root2 = tk.Tk()

            #rozmiary
            window_width = 250
            window_height = 50

            root2.title("No maps")

            screen_width = root2.winfo_screenwidth()
            screen_height = root2.winfo_screenheight()

            centerX = int(screen_width/2 - window_width/2)
            centerY = int(screen_height/2 - window_height/2)

            root2.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')


            #widgety
            ttk.Label(root2, text='No maps, you can create your own one').pack()
            ttk.Button(root2, text='OK!', command=root2.destroy).pack()
        else:
            #tworze okno
            root2 = tk.Tk()

            #rozmiary
            window_width = 500
            window_height = 500

            root2.title("All maps")

            screen_width = root2.winfo_screenwidth()
            screen_height = root2.winfo_screenheight()

            centerX = int(screen_width/2 - window_width/2)
            centerY = int(screen_height/2 - window_height/2)

            root2.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')
            
 
            # create listbox object
            listbox = tk.Listbox(root2, height = 10,
                  width = 300,
                  bg = "yellow",
                  font = "Helvetica",
                  fg = "black")
           
 
            i=1
            for elem in generator:
                listbox.insert(i, "{:<10s}  {:>2f} {:<5d} ".format(elem[0], elem[1], elem[2]) )
                i+=1
 
            # pack the widgets
            listbox.pack()

            tk.Button(root2, text="Sort by name", command=sortNames).pack()
            tk.Button(root2, text="Sort descending by level", command=sortDescLevel).pack()
            tk.Button(root2, text="Sort ascending by level", command=sortAscLevel).pack()
            # tk.Button(root2, text="Sort descending by number of games", command=sortDscGames).pack()
            # tk.Button(root2, text="Sort ascending by number of games", command=sortAscGames).pack()

            
            root2.mainloop()



    def updateSlider(self,event):
        self.difficulty_to_save = int(round(self.difficulty.get(), 0))
        self.difficultyLabel.config(text="Current difficulty: "+str(self.difficulty_to_save))




    def start(self):
        self.root.destroy()

        self.subroot = tk.Tk()
        
        #ustawiam tytul
        self.subroot.title("Pac-Man")

        #rozmiary
        window_width = 700
        window_height = 600

        screen_width = self.subroot.winfo_screenwidth()
        screen_height = self.subroot.winfo_screenheight()

        centerX = int(screen_width/2 - window_width/2)
        centerY = int(screen_height/2 - window_height/2)

        self.subroot.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')

        #mozliwosc zmiany rozmiaru
        self.subroot.resizable(True, True)

        #widgety
        ttk.Label(self.subroot, text='Welcome to Pac-Man!').pack()
        ttk.Button(self.subroot, text='Play on random map', command=self.randomMap).pack()
        ttk.Label(self.subroot, text="Set the difficulty:").pack()
        self.difficulty = tk.DoubleVar()
        slider = ttk.Scale(
                                self.subroot,
                                from_=1,
                                to=5,
                                orient='horizontal', 
                                variable=self.difficulty,
                                command=self.updateSlider
                        )
        slider.pack()
        self.difficultyLabel = ttk.Label(self.subroot, text="Current difficulty: "+str(self.difficulty_to_save))
        self.difficultyLabel.pack()
        ttk.Button(self.subroot, text='Choose the level', command=self.levelMap).pack()

        ttk.Button(self.subroot, text='Choose the map', command=self.specificMap).pack()


        self.subroot.mainloop()

    

menu=Menu()

