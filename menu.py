import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import board_generator as bg


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
        
        #zamykam okno
        root.destroy()
        #otwieram generator
        bo = bg.BoardGenerator(path.name)
        bo.run()

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
ttk.Button(root, text='Play!').pack()
ttk.Button(root, text='Create new board!', command=runNewGenerator).pack()
ttk.Button(root, text='Load draft board!', command=runDraftGenerator).pack()


root.mainloop()


