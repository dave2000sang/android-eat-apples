import pygame
import random
import face_detect
import time
import math
import highscores
import colours
import text
import cv2
import base
from block import Block

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
block_color = (50, 7, 20)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Apple Monster')
clock = pygame.time.Clock()

background_image = pygame.image.load("game_background.jpg")
monsterImg = pygame.image.load('monster.png')
appleImg = pygame.image.load('apple.png')
ResetAppleImg = pygame.image.load('ResetApple.png')

def quitgame():
    pygame.quit()
    quit()

def pause():

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        gameDisplay.fill(colours.white)
        pausedSurf, pausedRect = text.text_objects("Paused", text.smallText, colours.black)
        pausedRect.center = (400, 200)
        gameDisplay.blit(pausedSurf, pausedRect)

        contSurf, contRect = text.text_objects("To continue, press ESCAPE again", text.smallText, colours.black)
        contRect.center = (400, 300)
        gameDisplay.blit(contSurf, contRect)
        pygame.display.update()
        clock.tick(5)


def monster(x, y):
    gameDisplay.blit(monsterImg, (x, y))

def print_apples(apple_x, apple_y, img):
    #pygame.draw.circle(gameDisplay, color, (apple_x, apple_y), apple_r, apple_w)
    gameDisplay.blit(img, (apple_x, apple_y))

class Apple:
    def __init__(self,x,y,speed,img):
        self.x = x
        self.y = y
        self.speed = speed
        self.img = img

class Reset_Apple (Apple):
    def __init__(self,x,y,speed,img):
        self.x = x
        self.y = y
        self.speed = speed
        self.img = img

def print_blocks(b_x, b_y, width, height):
    pygame.draw.rect(gameDisplay, block_color, [b_x, b_y, width, height], 0)

def game_over(count):
    highscores.register_highscore(gameDisplay, count)

def game_loop():
    # Monster starting position
    monsterX = (display_width * 0.4)
    monsterY = (display_height * 0.8) - 20

    velocity = 0
    count = 0

    # Width and Height of apple sprite
    apple_w = appleImg.get_rect().width
    apple_h = appleImg.get_rect().height

    # print apple_w
    # print apple_h

    # Width and Height of monster
    monster_width = monsterImg.get_rect().width
    monster_height = monsterImg.get_rect().height

    # Constants for apples
    APPLE_X = random.randrange(0, display_width - apple_w)
    APPLE_Y = -600
    APPLE_SPEED = 15
    APPLE_RADIUS = 20

    # apples list holds all apples
    apples = []
    apples.append(Apple(APPLE_X,APPLE_Y,APPLE_SPEED,appleImg))

    # floor blocks
    block_width = 1.5 * (2*APPLE_RADIUS)    # 60
    block_height = 20                       # 20
    num_blocks = int(math.ceil(display_width/block_width))
    blocks = []

    # Measure Time Elapsed
    start_time = time.time()

    # Time to release a new Reset apple
    TIME_Reset_Apple = 15
    TIME_Reset_increment = TIME_Reset_Apple

    # Time to release a new apple
    TIME_Apple = 20 + random.randrange(0, 5)
    TIME_Apple_increment = 20

    # interval to change speed by speedChange every changeSpeedInterval
    initialInterval = 5
    changeSpeedInterval = initialInterval
    speedChange = 5

    # Initiate blocks
    for i in range(num_blocks):
        blocks.append(Block(block_width, block_height, i*block_width, monsterY + monster_height))

    gameExit = False

    # while game is running
    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
                gameExit = True
            # print(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over(count)
                    gameExit = True

                elif event.key == pygame.K_p:
                    pause()


        # for detecting face:
        coord, velocity = face_detect.process_frame()

        # Move android from detecting face movement
        if len(coord):
            monsterX += velocity * 3
        if monsterX < 0:
            monsterX = 0
        if monsterX > display_width - monster_width:
            monsterX = display_width - monster_width

        # Game Background
        gameDisplay.blit(background_image, (0, 0))

        # Display camera live streaming
        face_img = cv2.cvtColor(face_detect.face_img, cv2.COLOR_BGR2RGB)
        bg = pygame.image.frombuffer(face_img.tostring(), face_img.shape[1::-1], "RGB")

        gameDisplay.blit(bg, (0, 0))

        # Update monster
        monster(monsterX, monsterY)

        # Update/draw floor:
        for i in range(num_blocks):
            cur_block = blocks[i]
            if cur_block.visible:
                print_blocks(cur_block.x, cur_block.y, cur_block.width, cur_block.height)

        # If TIME_Reset_Apple seconds have passed, add a new reset apple
        cur_time = time.time() - start_time


        # print "time: " + str(cur_time)
        # print "Next time: " + str(TIME_Apple)
        # print len(apples)

        # After Time_Reset_increment seconds passed, add a reset apple
        if abs(cur_time - TIME_Reset_Apple) <= 0.05:
            temp_x = random.randrange(0, display_width - apple_w)
            apples.append(Reset_Apple(temp_x, APPLE_Y, APPLE_SPEED, ResetAppleImg))
            TIME_Reset_Apple += TIME_Reset_increment

        # Insert a new regular apple (every TIME_Apple seconds have passed)
        if abs(cur_time - TIME_Apple) <= 0.05:
            temp_x = random.randrange(0, display_width - apple_w)
            temp_y = - random.randrange(0, display_width)
            apples.append(Apple(temp_x,temp_y, APPLE_SPEED, appleImg))
            TIME_Apple += TIME_Apple_increment + random.randrange(0, 5)        # Make a new random apple

        # Query through and update apple(s) falling
        for i in range(len(apples)):
            cur_apple = apples[i]

            print_apples(cur_apple.x, cur_apple.y, cur_apple.img)

            # Increase speed of Apple every time you catch a multiple of 5.
            if count == changeSpeedInterval:
                changeSpeedInterval += initialInterval
                APPLE_SPEED = APPLE_SPEED + speedChange

            # print APPLE_SPEED
            cur_apple.y += APPLE_SPEED


            # check collision between apple and monster
            if cur_apple.y + apple_h > monsterY:
                if cur_apple.x + apple_w >= monsterX and cur_apple.x <= monsterX + monster_width:

                    count += 1

                    if isinstance(cur_apple, Reset_Apple):
                        # Reset blocks
                        for j in range(len(blocks)):
                            blocks[j].reappear()
                        del apples[i]                   # remove the Reset_Apple
                        Insert_Reset_Already = False    # can now add another Reset_Apple
                        break

                    cur_apple.y = - cur_apple.y - random.randrange(0, display_width)
                    cur_apple.x = random.randrange(0, display_width - apple_w)
                    Insert_Apple = False

            # When missed apple (apple passed monster)
            if cur_apple.y + apple_h > monsterY + monster_height:
                hit_block = False

                # Make disappear block with x coordinate
                for k in range(len(blocks)):
                    cur_block = blocks[k]

                    # Why is it width/2
                    if cur_apple.x + apple_w/2 <= cur_block.x + cur_block.width and cur_apple.x + apple_w/2 >= cur_block.x and cur_block.visible:
                        cur_block.disappear()
                        hit_block = True

                        # Reset apple y coordinate
                        cur_apple.y = - cur_apple.y - random.randrange(0, display_width)
                        cur_apple.x = random.randrange(0, display_width - apple_w)
                        break

                # if pass through (no block disappear)
                # if hit_block == False:
                #    game_over(count)
                #    gameExit = True

                if cur_apple.y > display_height:
                    game_over(count)
                    gameExit = True

                # Check if current apple is a Reset_Apple, if it is, delete it.
                if isinstance(cur_apple, Reset_Apple):
                    del apples[i]
                    break

        update_cnt = "Score: " + str(count)
        countSurf, countRect = text.text_objects(update_cnt, text.smallText, colours.black)
        countRect.center = (800 - countRect.width, 0 + countRect.height)
        gameDisplay.blit(countSurf, countRect)

        pygame.display.update()
        clock.tick(30)
