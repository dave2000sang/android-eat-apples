import pygame
import random
import blyat
import time
import base
import leaderboard
import colours
import text

pygame.init()

gameDisplay = pygame.display.set_mode((text.display_width, text.display_height))
clock = pygame.time.Clock()

startmenu_image = pygame.image.load("start_menu.jpeg").convert()

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #Title:
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        textSurf, textRect = text.text_objects("Fuck", largeText, colours.black)
        textRect.center = (text.display_width/2, 50)
        gameDisplay.blit(textSurf, textRect)

        #Start Menu Background Image
        gameDisplay.fill(colours.white)

        #Start Menu Buttons
        text.button("Start",300, 100, 200, 100, colours.lightgray, colours.gray, base.game_loop)
        text.button("Leaderboard", 300, 250, 200, 100, colours.lightgray, colours.gray, "leaderboard")
        text.button("Quit", 300, 400, 200, 100, colours.lightgray, colours.gray, base.quitgame)

        pygame.display.update()
        clock.tick(15)
