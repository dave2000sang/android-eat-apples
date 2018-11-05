import pygame
pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

jet_width = 208

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('fuckblyat')
clock = pygame.time.Clock()

jetImg = pygame.image.load('fighterjet.png')

def jet(x, y):
    gameDisplay.blit(jetImg, (x, y))


def game_loop():
    x = (display_width * 0.4)
    y = (display_height * 0.5)

    x_change = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            print(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5


                if event.key == pygame.K_RIGHT:
                    x_change = 5



            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0


        x += x_change
        if x < 0:
            x = 0

        if x > display_width - jet_width:
            x = display_width - jet_width


        gameDisplay.fill(white)

        jet(x, y)


        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
quit()

