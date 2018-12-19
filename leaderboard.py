import pygame
import startmenu
import colours
import basetest
pygame.init()

customtext = pygame.font.Font('freesansbold.ttf', 20)

def center_box(w, h):
    box_x = (800 - w)/2
    box_y = (600 - h)/2

    return box_x, box_y

def leaderboard(gameDisplay, file_name):
    display = True
    box_height = 500
    box_width = 400

    while display:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        file = open(file_name, 'r')
        lines = file.readlines()
        scores = []

        for line in lines:
            sep = line.index(',')
            name = line.strip()[:sep]
            score = line.strip()[(sep + 1):]
            scores.append ((score, name))

        file.close
        scores.sort(reverse=True)
        top_10 = scores[:10]

        print top_10

        box = pygame.surface.Surface((box_width, box_height))
        box.fill(colours.lightgray)

        #Leaderboard title
        textSurf, textRect = startmenu.text_objects("Leaderboard", startmenu.smallText, colours.black)
        textRect.center = ((box_width/2), 50)
        box.blit(textSurf, textRect)

        for i, entry in enumerate(top_10):

            #Position of names
            nameSurf, nameRect = startmenu.text_objects(entry[1], customtext, colours.black)
            nameRect.left = 70 #CALCULATE THE SEPERATION LATER
            nameRect.centery = (30 * i + 100)
            box.blit(nameSurf, nameRect)

            #Position of scores
            scoreSurf, scoreRect = startmenu.text_objects(entry[0], customtext, colours.black)
            scoreRect.right = (box_width - 70)
            scoreRect.centery = (30 * i + 100)
            box.blit(scoreSurf, scoreRect)

        gameDisplay.blit(box, center_box(box_width, box_height))
        pygame.display.update()
        startmenu.clock.tick(15)
