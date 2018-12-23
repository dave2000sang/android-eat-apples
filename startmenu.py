import pygame
import random
import blyat
import time
import base
import leaderboard
import colours
import text

pygame.init()

clock = pygame.time.Clock()

startmenu_image = pygame.image.load("start_menu.jpeg").convert()

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                base.quitgame()
                break
        #Title:
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        textSurf, textRect = text.text_objects("Fuck", largeText, colours.black)
        textRect.center = (text.display_width/2, 50)
        text.gameDisplay.blit(textSurf, textRect)

        #Start Menu Background Image
        text.gameDisplay.fill(colours.white)

        #Start Menu Buttons
        text.button(text.gameDisplay, "Start",300, 100, 200, 100, colours.lightgray, colours.gray, base.game_loop)
        text.button(text.gameDisplay, "Leaderboard", 300, 250, 200, 100, colours.lightgray, colours.gray, "leaderboard")
        text.button(text.gameDisplay, "Quit", 300, 400, 200, 100, colours.lightgray, colours.gray, base.quitgame)

        pygame.display.update()
        clock.tick(15)
