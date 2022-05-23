from glob import glob
import random
import pygame
import math

from pygame import mixer

pygame.init()

# Sets width and height of the screen
screen = pygame.display.set_mode((800,600))

running = True

#Setting up a title for the window
pygame.display.set_caption("Test Game")


#Player
playerImage = pygame.image.load("soccer-player.png")
playerX = 370
playerY = 470
playerY_change = 0
playerX_change = 0

#Goal
goalImage = pygame.image.load("goal.png")
goalX = random.randint(0,736)
goalY = 0

#Football
#Ready - Not visible
#Moving
ballImage = pygame.image.load("football.png")
ballX = playerX
ballY = playerY
ballY_change = -0.5
ballX_change = 0.2
ball_state = "ready"
bounces = 0


scoreVal = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10


bgImage = pygame.image.load("bg.jpg")

def showScore(x,y):
    score = font.render("Goals:" + str(scoreVal),True,(255,255,255))
    screen.blit(score,(x,y))

def goal(x,y):
    screen.blit(goalImage,(x,y))

def player(x,y):
    # blit is used to draw something on screen
    screen.blit(playerImage,(x,y))
     
def kick(x,y):
    global ball_state
    ball_state = "moving"
    screen.blit(ballImage,(x, y))

def isCollision(targetX,targetY,ballX,ballY):
    dist = math.sqrt(math.pow(targetX-ballX,2) + math.pow(targetY-ballY,2))
    if dist < 32:
        return True
    else:
        return False



#Game loop
while running:


    #Get all events
    for event in pygame.event.get():
        # If window closed
        if event.type == pygame.QUIT:
            running = False
        #KEYDOWN is pressing that key
        if event.type == pygame.KEYDOWN:
            # Left Key Pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -0.1
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.1
            """
            if event.key == pygame.K_UP:
                playerY_change = -0.1
            if event.key == pygame.K_DOWN:
                playerY_change = 0.1
            """
            if event.key == pygame.K_SPACE:
                if ball_state == "ready":
                    kick_sound = mixer.Sound("football-kick.mp3")
                    kick_sound.play()
                    kick(playerX,playerY)
                    ballX = playerX
                    ballY = playerY
        if event.type == pygame.KEYUP: 
            playerX_change = 0
            #playerY_change = 0
    
    playerX += playerX_change
    #playerY += playerY_change

    # Setting x-axis boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Setting y-axis boundary
    """
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536
    """






    #Setting RGB Background
    screen.fill((255,0,255))     
    
    #BG Image
    screen.blit(bgImage,(0,0))

    #Make sure player is called after screen is filled
    player(playerX,playerY)
    goal(goalX,goalY)
    showScore(textX,textY)

    if bounces >= 5:
        ballY = playerY
        ball_state = "ready"
        bounces = 0
        ballY_change = -0.5
        ballX_change = 0.2
    
    # Ball movement
    if ball_state == "moving":
        ballY += ballY_change
        ballX += ballX_change
        if ballY <= 0:
            bounces += 1
            #print("Hit top edge")
            ballY_change = 0.5
        elif ballY >= 536:
            bounces += 1
            #print("Hit bottom edge")
            ballY_change = -0.5
        
        
        if ballX <= 0:
            bounces += 1
            #print("Hit left edge")
            ballX_change = 0.5
        elif ballX >= 736:
            bounces += 1
            #print("Hit Right Edge")
            ballX_change = -0.5


        kick(ballX,ballY)


        
        
    collision = isCollision(goalX,goalY,ballX,ballY)
    if collision:
        ballY = playerY
        ballX = playerX
        ball_state = "ready"
        bounces = 0
        print("GOAL!!!!")
        scoreVal += 1
        print(scoreVal)
        goalX = random.randint(64,736)
        goalY = 0
        goal_sound = mixer.Sound("goal.mp3")
        goal_sound.play()


    #Updating display to reflect changes
    pygame.display.update()