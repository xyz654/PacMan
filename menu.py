import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import board_generator as bg
import main
import numpy as np
from os import listdir
from os.path import isfile, join
from PIL import Image
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
        # self.root.resizable(True, True)
        self.root.configure(background='black')

        style = ttk.Style()
        style.configure("First", background="black")

        style = ttk.Style()
        style.configure("BW.TLabel", background="black")

        ttk.Button(text="Test", style="BW.TLabel").pack()
        ttk.Label(text="Test", style="BW.TLabel").pack()

        #widgety
        welcome=tk.PhotoImage(file="graphics/pngFiles/writing/welcome.png")
        ttk.Label(self.root, image=welcome, style="BW.TLabel").place(x=window_width/2-304, y=50)
        play = tk.PhotoImage(file="graphics/pngFiles/writing/play.png")
        ttk.Button(self.root,  image=play ,command=self.start, style="BW.TLabel").place(x=window_width/2-45, y=150)
        createNewBoard=tk.PhotoImage(file="graphics/pngFiles/writing/createNewBoard.png")
        ttk.Button(self.root, image=createNewBoard, command=self.runNewGenerator,  style="BW.TLabel").place(x=window_width/2-170,y=225)
        loadDraftBoard=tk.PhotoImage(file="graphics/pngFiles/writing/loadDraftBoard.png")
        ttk.Button(self.root, image=loadDraftBoard, command=self.runDraftGenerator, style="BW.TLabel").place(x=window_width/2-168, y=300)
        statisticsText=tk.PhotoImage(file="graphics/pngFiles/writing/statistics.png")
        ttk.Button(self.root, image=statisticsText, command=self.statistics, style="BW.TLabel").place(x=window_width/2-112, y=375)

        exitText=tk.PhotoImage(file="graphics/pngFiles/writing/exit.png")
        ttk.Button(self.root, image=exitText, command=exit, style="BW.TLabel").place(x=window_width/2-63, y=450)  
        
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
            window_height = 100

            root2.title("No maps")
            root2.configure(background='black')

            screen_width = root2.winfo_screenwidth()
            screen_height = root2.winfo_screenheight()

            centerX = int(screen_width/2 - window_width/2)
            centerY = int(screen_height/2 - window_height/2)

            root2.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')



            #widgety
            ttk.Label(root2, text='No maps with this level!', background="yellow").place(x=50,y=10)
            ttk.Button(root2, text='OK!', command=root2.destroy).place(x=80,y=40)
        else:
            #losowo wybieram mape
            x=random.choice(generator)
            # subroot.destroy()
            game = main.Game("maps/"+x)
            game.run()

    def specificMap(self):

        def sortNames():
            generator.sort()
            i=1
            listbox.delete(0,tk.END)
            for elem in generator:
                listbox.insert(i, "name: {:<10s} \t  level: {:>2d} \t played: {:<5d} ".format(elem[0], elem[1], elem[2]) )
                i+=1

        def sortDescLevel():
            generator_sort=sorted(generator,key=lambda x: x[1], reverse=True)
            i=1
            listbox.delete(0,tk.END)
            for elem in generator_sort:
                listbox.insert(i, "name: {:<10s} \t  level: {:>2d} \t played: {:<5d} ".format(elem[0], elem[1], elem[2]) )
                i+=1

        def sortAscLevel():
            generator_sort=sorted(generator,key=lambda x: x[1], reverse=False)
            i=1
            listbox.delete(0,tk.END)
            for elem in generator_sort:
                listbox.insert(i, "name: {:<10s} \t  level: {:>2d} \t played: {:<5d} ".format(elem[0], elem[1], elem[2]) )
                i+=1

        def chosen():
            for i in listbox.curselection():
                game = main.Game("maps/"+listbox.get(i).split(" ",2)[1])
                root2.destroy()
                game.run()
                break

        def sortAscGames():
            generator_sort=sorted(generator,key=lambda x: x[2], reverse=False)
            i=1
            listbox.delete(0,tk.END)
            for elem in generator_sort:
                listbox.insert(i, "name: {:<10s} \t  level: {:>2d} \t played: {:<5d} ".format(elem[0], elem[1], elem[2]) )
                i+=1

        def sortDscGames():
            generator_sort=sorted(generator,key=lambda x: x[2], reverse=True)
            i=1
            listbox.delete(0,tk.END)
            for elem in generator_sort:
                listbox.insert(i, "name: {:<10s} \t  level: {:>2d} \t played: {:<5d} ".format(elem[0], elem[1], elem[2]) )
                i+=1
        def find():
            inp = inputtxt.get(1.0, "end-1c")
            generator_new=[]
            i=1
            listbox.delete(0,tk.END)
            for elements in generator:
                if elements[0].startswith(inp):
                    listbox.insert(i, "name: {:<10s} \t  level: {:>2d} \t played: {:<5d} ".format(elements[0], elements[1], elements[2]) )
                    i+=1
        def findlevel():
            inp = inputtxtLevel.get(1.0, "end-1c")
            generator_new=[]
            i=1
            listbox.delete(0,tk.END)
            for elements in generator:
                if elements[1]==int(inp):
                    listbox.insert(i, "name: {:<10s} \t  level: {:>2d} \t played: {:<5d} ".format(elements[0], elements[1], elements[2]) )
                    i+=1

        generator=[]
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
                        if stat[0] == map:
                            statystics=int(stat[1])
                    level=int(currentStats[0])
                    if statystics:
                        generator.append((map,level,statystics))
                    else:
                        generator.append((map,level,0))

        
        #sprawdzenie czy sa jakies mapy
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
            ttk.Label(root2, text='No maps').pack()
            ttk.Button(root2, text='OK!', command=root2.destroy).pack()
        else:
            #tworze okno
            root2 = tk.Tk()

            #rozmiary
            window_width = 500
            window_height = 600

            root2.title("All maps")

            root2.configure(border=1, highlightbackground="yellow", highlightthickness=10, relief="sunken", background="black")

            screen_width = root2.winfo_screenwidth()
            screen_height = root2.winfo_screenheight()

            centerX = int(screen_width/2 - window_width/2)
            centerY = int(screen_height/2 - window_height/2)

            root2.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')
            
 
            # create listbox object
            listbox = tk.Listbox(root2, height = 7,
                  width = 300,
                  font = "Helvetica",
                  fg = "white",
                  highlightbackground="yellow",
                  selectforeground="black",
                  selectbackground="yellow",
                  background="black")
            
           
 
            i=1
            for elem in generator:
                listbox.insert(i, "name: {:<10s} \t  level: {:>2d} \t played: {:<5d} ".format(elem[0], elem[1], elem[2]) )
                i+=1
 
            # pack the widgets
            listbox.pack()

            # #Create style object
            # sto = ttk.Style()

            # #configure style
            # sto.configure('W.TButton', font= ('Arial', 10, 'underline'),
            # foreground='Green')



            tk.Button(root2, text="Sort by name", command=sortNames, relief="flat", background="black", foreground="yellow").place(x=170, y=150)
            tk.Button(root2, text="Sort descending by level", command=sortDescLevel, relief="flat", background="black", foreground="yellow").place(x=50, y=200)
            tk.Button(root2, text="Sort ascending by level", command=sortAscLevel, relief="flat", background="black", foreground="yellow").place(x=250,y=200)
            tk.Button(root2, text="Sort descending by number of games", command=sortDscGames, relief="flat", background="black", foreground="yellow").place(x=110, y=250)
            tk.Button(root2, text="Sort ascending by number of games", command=sortAscGames, relief="flat", background="black", foreground="yellow").place(x=115, y=300)
            inputtxt = tk.Text(root2, height = 1, width = 30, background="lightgrey")   
            inputtxt.place(x=120, y=350)
                
            printButton = tk.Button(root2, text = "Find", command = find, relief="flat", background="black", foreground="yellow")
            printButton.place(x=210, y=380)

            inputtxtLevel = tk.Text(root2, height = 1, width = 10, background="lightgrey")   
            inputtxtLevel.place(x=190, y=430)
                
            printButtonLevel = tk.Button(root2, text = "Find level", command = findlevel, relief="flat", background="black", foreground="yellow")
            printButtonLevel.place(x=190, y=460)

            tk.Button(root2, text="Play on chosen map", command=chosen, relief="flat", background="black", foreground="yellow").place(x=160, y=510)
            
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

        self.subroot.configure(background='black')

        screen_width = self.subroot.winfo_screenwidth()
        screen_height = self.subroot.winfo_screenheight()

        centerX = int(screen_width/2 - window_width/2)
        centerY = int(screen_height/2 - window_height/2)

        self.subroot.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')

        #mozliwosc zmiany rozmiaru
        self.subroot.resizable(True, True)

        #style
        style = ttk.Style()
        style.configure("BW.TLabel", background="black")

        #widgety
        randomMap=tk.PhotoImage(file="graphics/pngFiles/writing/randomMap.png")
        playPacMan=tk.PhotoImage(file="graphics/pngFiles/writing/playpacMan.png")
        ttk.Label(self.subroot, image=playPacMan, style="BW.TLabel").place(x=50, y=50)
        ttk.Button(self.subroot, image=randomMap, command=self.randomMap,style="BW.TLabel").place(x=200,y=150)
        setDifficulty=tk.PhotoImage(file="graphics/pngFiles/writing/setDifficulty.png")
        ttk.Label(self.subroot, image=setDifficulty, style="BW.TLabel").place(x=175, y=250)
        self.difficulty = tk.DoubleVar()
        style=ttk.Style()
        style.configure("TScale", background="black", troughcolor="yellow")
        slider = ttk.Scale(
                                self.subroot,
                                from_=1,
                                to=5,
                                orient='horizontal', 
                                variable=self.difficulty,
                                command=self.updateSlider,\
                                style="TScale"
                        )
        slider.place(x=300, y=290)
        style = ttk.Style()
        style.configure("BW.TLabel1", background="black")
        self.difficultyLabel = ttk.Label(self.subroot, text="Current difficulty: "+str(self.difficulty_to_save), background="yellow")
        self.difficultyLabel.place(x=290, y=320)
        chooseTheLevel=tk.PhotoImage(file="graphics/pngFiles/writing/chooseTheLevel.png")
        ttk.Button(self.subroot, image=chooseTheLevel, command=self.levelMap, style="BW.TLabel").place(x=180, y=350)
        chooseTheMap=tk.PhotoImage(file="graphics/pngFiles/writing/chooseTheMap.png")
        ttk.Button(self.subroot, image=chooseTheMap, command=self.specificMap, style="BW.TLabel").place(x=200, y=450)


        self.subroot.mainloop()


    def statistics(self):
        
        #statystyki
        stats = np.array([])
        with open("./generalStats.npy", 'rb') as f:
            stats = np.load(f)
            f.close()

        localStats = np.array([])
        with open("./mapStats.npy", 'rb') as f:
            localStats=np.load(f)
            f.close()
        
        #tworze okno
        root2 = tk.Tk()

        #rozmiary
        window_width = 300
        window_height = 200

        root2.title("Statistics")

        screen_width = root2.winfo_screenwidth()
        screen_height = root2.winfo_screenheight()

        centerX = int(screen_width/2 - window_width/2)
        centerY = int(screen_height/2 - window_height/2)

        root2.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')
        root2.configure(background='black')


        mostPopular=''
        numberOfGames=0
        for stat in localStats:
            if numberOfGames<int(stat[1]):
                numberOfGames=int(stat[1])
                mostPopular=stat[0]

        mostPopularLevel=None
        levels=[0,0,0,0,0]
        gamesOnLevel=0

        onlyfiles = [f for f in listdir("./maps") if isfile(join("./maps", f))]
        for map in onlyfiles:
            currentStats=self.loadData("maps/"+map)
            for stat in localStats:
                if stat[0] == map:
                    levels[int(currentStats[0])-1]+=int(stat[1])

        for i in range(len(levels)):
            if gamesOnLevel<levels[i]:
                gamesOnLevel=levels[i]
                mostPopularLevel=i+1


        for stat in localStats:
            if numberOfGames<int(stat[1]):
                numberOfGames=int(stat[1])
                mostPopular=stat[0]

        ttk.Label(root2, text='Game time: ' + str(round(stats[0],2))+ 's', foreground='yellow', background="black").pack()
        ttk.Label(root2, text='Number of games: ' + str(int(stats[1])), foreground='yellow', background="black").pack()
        ttk.Label(root2, text='Average number of points: ' + str(int(stats[2])), foreground='yellow', background="black").pack()
        ttk.Label(root2, text='Number of kills by Clyde: ' + str(int(stats[3])), foreground='yellow', background="black").pack()
        ttk.Label(root2, text='Number of kills by Blinky: ' + str(int(stats[4])), foreground='yellow', background="black").pack()
        ttk.Label(root2, text='Number of kills by Inky: ' + str(int(stats[5])), foreground='yellow', background="black").pack()
        ttk.Label(root2, text='Number of kills by Pinky: ' + str(int(stats[6])), foreground='yellow', background="black").pack()
        ttk.Label(root2, text='The most popular map: ' + mostPopular, foreground='yellow', background="black").pack()
        ttk.Label(root2, text='The most popular level: ' + str(mostPopularLevel), foreground='yellow', background="black").pack()





            
 
          
        root2.mainloop()




menu = Menu()

