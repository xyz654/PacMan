import pygame
import sys
import numpy as np


pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW_LIGHT = (255, 255, 102)
YELLOW = (255, 255, 0)
GREY = (211,211,211)


#glowne stale
FPS = 60
screen_width = 700
screen_height = 600

#glowne zmienne
mousePos = pygame.mouse.get_pos()
mouse_is_pressed=False


#okno
screen = pygame.display.set_mode((screen_width, screen_height))
 
pygame.display.set_caption("Pac-Man board generator")

# zegar
clock = pygame.time.Clock()


def show():

    screen.fill(WHITE)

    #czcionki
    font1=pygame.font.Font('freesansbold.ttf', 20)


    #welcome - napis

    save=font1.render('WELCOME!', True, BLACK, WHITE)
    screen.blit(save,(screen_width//2-50,screen_height//8+15))

    #przycisk - rozpocznij tworzenie nowej planszy

    pygame.draw.rect(screen,GREY,((screen_width//4),screen_height//4,screen_width//2,50),0,10)
    pygame.draw.rect(screen,BLACK,((screen_width//4),screen_height//4,screen_width//2,50),1,10)
    save=font1.render('CREATE NEW BOARD', True, BLACK, GREY)
    screen.blit(save,(screen_width//3+10,screen_height//4+15))

    #przycisk - wczytaj plansze robocze

    pygame.draw.rect(screen,GREY,((screen_width//4),3*screen_height//8,screen_width//2,50),0,10)
    pygame.draw.rect(screen,BLACK,((screen_width//4),3*screen_height//8,screen_width//2,50),1,10)
    save=font1.render('LOAD DRAFT BOARD', True, BLACK, GREY)
    screen.blit(save,(screen_width//3+15,3*screen_height//8+15))

    #przycisk - graj

    pygame.draw.rect(screen,GREY,((screen_width//4),4*screen_height//8,screen_width//2,50),0,10)
    pygame.draw.rect(screen,BLACK,((screen_width//4),4*screen_height//8,screen_width//2,50),1,10)
    save=font1.render('PLAY', True, BLACK, GREY)
    screen.blit(save,(screen_width//2-25,4*screen_height//8+15))



while True:

    #pobieranie pozycji myszki
    mousePos = pygame.mouse.get_pos()

    show()


    #przechwytywanie zdarzen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #LPM
            if event.button == 1:
                mouse_is_pressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_is_pressed = False


    x=(int)(mousePos[0])
    y=(int)(mousePos[1])

    if mouse_is_pressed and x>screen_width//4 and x<3*screen_width//4 and y>screen_height//4 and y<screen_height//4+50:
        #rozpocznij tworzenie nowej planszy
        print("new")
        import board_generator
        # break
    
    if mouse_is_pressed and x>screen_width//4 and x<3*screen_width//4 and y>3*screen_height//8 and y<3*screen_height//8+50:
        #wczytaj wersje robocz
        print("wersja robocza")
        # break

    if mouse_is_pressed and x>screen_width//4 and x<3*screen_width//4 and y>screen_height//2 and y<screen_height//2+50:
        #graj
        print("graj")
        # break


    #odswiezanie okna
    pygame.display.update()
    #kontroluje FPS
    clock.tick(FPS)