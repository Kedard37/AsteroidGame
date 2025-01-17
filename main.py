# importing ibraries
import pygame, sys, os, random, math, time, asyncio
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

# colours
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# global variables
height = 600
width = 800
Time = 0
ship_x = width/2 - 50
ship_y = height/2 - 50
ship_angle = 0
ship_is_rotating = False
ship_is_forward = False
ship_direction = 0
ship_speed = 0
asteroid_x = list()
asteroid_y = list() 
asteroid_angle = list()
asteroid_speed = list()
no_asteroids = 5
bullet_x = list()
bullet_y = list()
bullet_angle = list()
bullet_ejected = False
no_bullets = 0
bullet_speed = 10
score = 0
game_over = False
flag = False

for i in range(0, no_asteroids):
    asteroid_x.append(random.randint(0, width))
    asteroid_y.append(random.randint(0, height))
    asteroid_angle.append(random.randint(0, 360))
    asteroid_speed.append(random.randint(1, 4))

# window set up
window = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption('Asteroids Game')

# load images
bg = pygame.image.load(os.path.join('images', 'nebula_brown.png'))
debris = pygame.image.load(os.path.join('images', 'debris2_brown.png'))
ship = pygame.image.load(os.path.join('images', 'ship.png'))
ship_thrusted = pygame.image.load(os.path.join('images','ship_thrusted.png'))
asteroid = pygame.image.load(os.path.join('images','asteroid.png'))
shot = pygame.image.load(os.path.join('images','shot2.png'))
explosion = pygame.image.load(os.path.join('images','explosion_blue.png'))

# load sounds
#Missile sound
missile_sound = pygame.mixer.Sound(os.path.join('sounds','missile.ogg'))
missile_sound.set_volume(1)
#thrust sound
thruster_sound = pygame.mixer.Sound(os.path.join('sounds','thrust.ogg'))
thruster_sound.set_volume(1)
#explosion sound
explosion_sound = pygame.mixer.Sound(os.path.join('sounds','explosion.ogg'))
explosion_sound.set_volume(1)
#background score
pygame.mixer.music.load(os.path.join('sounds','game.ogg'))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

# to rotate any image
def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def isCollision(enemyX, enemyY, bulletX, bulletY, dist):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < dist:
        return True
    else:
        return False

# draw game function
def draw(canvas):
    global Time, ship_is_forward, bullet_x, bullet_y, flag
    canvas.fill(black)
    canvas.blit(bg, (0, 0))
    canvas.blit(debris,(Time * 0.3, 0))
    canvas.blit(debris,(Time * 0.3 - width, 0))
    Time += 1
    for i in range(0, no_asteroids):
        canvas.blit(rot_center(asteroid, Time) ,(asteroid_x[i], asteroid_y[i]))
    for i in range(0, no_bullets):
        canvas.blit(shot ,(bullet_x[i], bullet_y[i]))
    if ship_is_forward:
        canvas.blit(rot_center(ship_thrusted, ship_angle), (ship_x, ship_y))
    else:
        canvas.blit(rot_center(ship, ship_angle), (ship_x, ship_y))

    #draw Score
    myfont1 = pygame.font.SysFont("Comic Sans MS", 40)
    label1 = myfont1.render("Score : "+str(score), 1, green)
    canvas.blit(label1, (50,20))

    if game_over:
        myfont2 = pygame.font.SysFont("Comic Sans MS", 60)
        label2 = myfont2.render("GAME OVER ", 1, white)
        canvas.blit(label2, (400, 20))
        flag = True
        

# handle input function
def handle_input():
    global ship_angle, ship_is_rotating, ship_direction
    global ship_x, ship_y, ship_is_forward, ship_speed
    global bullet_x, bullet_y, bullet_angle, no_bullets, bullet_ejected
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()   

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                ship_is_rotating = True
                ship_direction = 0
            elif event.key == K_LEFT:
                ship_is_rotating = True
                ship_direction = 1
            elif event.key == K_UP:
                ship_is_forward = True
                ship_speed = 7
                thruster_sound.play()
            elif event.key == K_SPACE:
                bullet_ejected = True
                bullet_x.append(ship_x + 50)
                bullet_y.append(ship_y + 50)
                bullet_angle.append(ship_angle)
                no_bullets = no_bullets + 1
                missile_sound.play()

        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                ship_is_rotating = False
                bullet_ejected = False
            else:
                ship_is_forward = False
                thruster_sound.stop() 

    if ship_is_rotating:
        if ship_direction == 0:
            ship_angle = ship_angle - 7    
        elif ship_direction == 1:
            ship_angle = ship_angle + 7

    if ship_is_forward or ship_speed > 0:
        ship_x = (ship_x + math.cos(math.radians(ship_angle)) * ship_speed )
        ship_y = (ship_y - math.sin(math.radians(ship_angle)) * ship_speed )
        if ship_y < 0:
            ship_y = height
        elif ship_y > height:
            ship_y = 0
        elif ship_x < 0:
            ship_x = width
        elif ship_x > width:
            ship_x = 0 
        if ship_is_forward == False:
            ship_speed = ship_speed - 0.3

def update_screen():
    pygame.display.update()
    fps.tick(60)

def game_logic():
    global bullet_x, bullet_y, bullet_angle, no_bullets, bullet_speed
    global asteroid_x, asteroid_y
    global score, game_over
   
    for i in range(0, no_bullets):
       bullet_x[i] = (bullet_x[i] + math.cos(math.radians(bullet_angle[i]))* bullet_speed)
       bullet_y[i] = (bullet_y[i] - math.sin(math.radians(bullet_angle[i]))* bullet_speed)

    for i in range(0, no_asteroids):
        asteroid_x[i] = (asteroid_x[i] + math.cos(math.radians(asteroid_angle[i])) * asteroid_speed[i])
        asteroid_y[i] = (asteroid_y[i] - math.sin(math.radians(asteroid_angle[i])) * asteroid_speed[i]) 

        if asteroid_y[i] < 0:
            asteroid_y[i] = height
        elif asteroid_y[i] > height:
            asteroid_y[i] = 0
        elif asteroid_x[i] < 0:
            asteroid_x[i] = width
        elif asteroid_x[i] > width:
            asteroid_x[i] = 0 

        if isCollision(ship_x, ship_y, asteroid_x[i], asteroid_y[i], 30):
            game_over = True
    
    for i in range(0, no_bullets):
        for j in range(0, no_asteroids):
            if isCollision(bullet_x[i], bullet_y[i], asteroid_x[j], asteroid_y[j], 50):
               asteroid_x[j] = (random.randint(0,width))
               asteroid_y[j] = (random.randint(0,height))
               asteroid_angle[j] = (random.randint(0,365))
               explosion_sound.play()
               score = score + 1

# asteroids game loop
async def main():
    while True:
        draw(window)
        handle_input()
        game_logic()
        update_screen()
        if flag == True:
            time.sleep(3)
            exit()
        await asyncio.sleep(0)

asyncio.run(main())    