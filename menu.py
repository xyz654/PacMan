import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import board_generator as bg
import main
import numpy as np


def runNewGenerator():
    #zamykam okno
    root.destroy()
    #otwieram generator
    bo = bg.BoardGenerator([])
    bo.run()
    
def runDraftGenerator():
    #pobieram sciezke
    path = filedialog.askopenfile()
    if path!=None:
        file_extension = os.path.splitext(path.name)[1]
        if file_extension == ".npy":
            #zamykam okno
            root.destroy()
            #otwieram generator
            bo = bg.BoardGenerator(path.name)
            bo.run()

def loadData(path):
    #pobieram dane z pliku
    with open(path, 'rb') as f:
        #zbieranie statystyk
        stats = np.load(f)
        print(stats[3])
        return stats[3]



def runGame():
    path = filedialog.askopenfile()
    if path!=None:
        file_extension = os.path.splitext(path.name)[1]
        if file_extension == ".npy":
            #gdy loadData zwroci 0 - jest git
            if loadData(path.name)==0:
                #zamykam okno
                root.destroy()
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


                root.mainloop()

    

#tworze okno
root = tk.Tk()

#ustawiam tytul
root.title("Pac-Man")

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
ttk.Label(root, text='Welcome to Pac-Man!').pack()
ttk.Button(root, text='Play!', command=runGame).pack()
ttk.Button(root, text='Create new board!', command=runNewGenerator).pack()
ttk.Button(root, text='Load draft board!', command=runDraftGenerator).pack()


root.mainloop()


