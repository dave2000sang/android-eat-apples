import pygame
import colours
import text
pygame.init()
import base
import startmenu


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
    lines = file.readlines()[1:]
    file.close

    high_score = 0
    high_name = ""

    for line in lines:
        name, score = line.split(",")
        score = int(score)
        if score > high_score:
            high_score = score
            high_name = name

    return high_name, high_score

def write_highscore(file_name, player_name, player_points):
    file = open(file_name, 'a')
    file.write ("\n" + player_name + "," + str(player_points))
    file.close()

def inputbox(display, string_input):
    #Inputbox Constants
    box_width = 600
    box_height = 300
    box_x = 100
    box_y = 150

    box = pygame.surface.Surface((box_width, box_height))
    box.fill(colours.lightgray)
    pygame.draw.rect(box, colours.black, (0,0, box_width, box_height), 5)
    titleSurf, titleRect = text.text_objects(string_input, text.smallText, colours.black)
    titleRect.center = (box_width / 2, 20)
    box.blit(titleSurf, titleRect)


    def blink(screen):
        for color in [colours.black, colours.white]:
            pygame.draw.rect(box, color, (box_width / 2, 65, 5, 20), 0)
            screen.blit(box, (box_x, box_y))
            pygame.display.flip()
            pygame.time.wait(300)

    def display_name(display, name):
        pygame.draw.rect(box, colours.white, (50, 60, box_width - 100, 30), 0)
        pygame.draw.rect(box, colours.black, (50, 60, box_width - 100, 30), 3)
        textSurf, textRect = text.text_objects(name, text.smallText, colours.black)
        textRect.center = (box_width/2, 75)
        box.blit(textSurf, textRect)


        display.blit(box, (box_x, box_y))
        pygame.display.update()

    name = ""
    display_name(display, name)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                base.quitgame()


            elif event.type == pygame.KEYDOWN:
                pressed_key = event.key

                if pressed_key == pygame.K_ESCAPE:
                    startmenu.game_intro()

                elif pressed_key in [13, 274]:
                    return name

                elif pressed_key == pygame.K_BACKSPACE: #backspace key
                    name = name[: -1]

                elif pressed_key <= 300:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT and 122 >= pressed_key >= 97:
                        pressed_key -= 32

                    name += event.unicode

        if name == "":
            blink(display)
        display_name(display, name)



    