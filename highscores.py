import pygame
import colours

pygame.init()

def register_highscore(display, player_points):
    highscore_name, highscore_points = get_highscore('highscores.txt')

    if player_points > highscore_points:
        player_name = inputbox(display, "New High Score!")

    elif player_points == highscore_points:
        player_name = inputbox(display, "So close!")

    elif player_points < highscore_points:
        player_name = inputbox(display, "Unlucky Run?")

    if len(player_name) == 0:
        return

    write_highscore('highscores.txt', player_name, player_points)

def get_highscore(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()
    file.close

    high_score = 0

    for line in lines:
        name, score = line.split(",")
        score = int(score)

    if score > high_score:
        high_score = score
        high_name = name

    return high_name, high_score

def write_highscore(file_name, player_name, player_points):
    file = open(file_name, 'a')
    print (player_name + "," + player_points)
    file.close()

def inputbox(display, text):
    import startmenu
    box_width = 600
    box_height = 150

    box = pygame.surface.Surface((box_width, box_height))
    box.fill(colours.lightgray)
    pygame.draw.rect(box, colours.black, (0,0, box_width, box_height), 1)
    textSurf, textRect = startmenu.text_objects(text, startmenu.largeText, colours.black)
    box.blit(textSurf, textRect)

    def display_name(display, name):
        pygame.draw.rect(box, colours.white, (50, 60, box_width - 100, 20), 0)
        textSurf, textRect = startmenu.text_objects(name, startmenu.smallText, colours.black)
        box.blit(textSurf, textRect)
        display.blit(box, (0, box_height/2))
        pygame.display.flip()

    name = ""
    display_name(display, name)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT():
                startmenu.quitgame()

            elif event.type == pygame.KEYDOWN:
                pressed_key = event.key
                if pressed_key in [13, 274]:
                    return name

                elif pressed_key == 8: #backspace key
                    name = name[: -1]

                elif pressed_key <= 300:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT and 122 >= pressed_key >= 97:
                        pressed_key -= 32

                    name += chr(pressed_key)






    