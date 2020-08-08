import pygame
import time
import random
from os import path
import os

dir_path = path.dirname(os.path.realpath(__file__))

black = (0,0,0)
white = (255,255,255)

coin_amount = 0

# Game initialisations
display_width = 800
display_height = 600
FPS = 30
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A Flying Game')
clock = pygame.time.Clock()

# Loading sounds
losing_sound = pygame.mixer.Sound(dir_path + "/Sounds/losing_sound.wav")
bomb_sound = pygame.mixer.Sound(dir_path + "/Sounds/bomb_sound.wav")
coin_sound = pygame.mixer.Sound(dir_path + "/Sounds/coin_sound.wav")

# Loading background image
backgroundImg = pygame.image.load(dir_path + "/background.jpg").convert()
background = backgroundImg.get_rect()

# Loading bomb
bombImg = pygame.image.load(dir_path + "/bomb.png").convert_alpha()
bomb = bombImg.get_rect()

# Loading character animation images to list
img_dir = dir_path + "/Character"
char_anim = []
for i in range(1,7):
    filename = '{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    char_anim.append(img)
char = char_anim[0].get_rect()

# Loading dead character body image
deadCharImg = pygame.image.load(img_dir + "/dead.png").convert_alpha()
deadChar = deadCharImg.get_rect()

# Loadig explotion animation images to list
img_dir = dir_path + "/Explosions"
explosion_anim = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    explosion_anim.append(img)
    
# Loading coin animation images to list
img_dir = dir_path + "/Coins"
coin_anim = []
for i in range(3):
    filename = 'coin{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    coin_anim.append(img)
coin = coin_anim[0].get_rect()

def coins_collected(count):
    """display how many points player have"""
    
    font = pygame.font.SysFont(None, 25)
    text = font.render("Coins: "+str(count), True, black)
    gameDisplay.blit(text, (0,0))  
    
def rot_center(image, angle):
    """rotate a character, maintaining position."""

    loc = image.get_rect().center  #rot_image is not defined 
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def crash():
    """ Show dialog when player crashes"""
    
    message_display("You DIED!", 115)
     
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
        message_display("Your score: "+str(coin_amount), 60, 3/5 * display_height)
        message_display("Press R to try again", 70, 4/5 * display_height)
    
def message_display(text, size, y=display_height/3):
    """Display messages to screen"""
    
    largeText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
   
def paused():
    """Show dialog when game is paused"""
    
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
        message_display("Press P to continue", 70)
 
def check_collision(char, obs):
    """Check if two obstacles are in same pixels"""
    
    if char.x + char.width > obs.x and char.x < obs.x + obs.width:
        if (obs.y > char.y and obs.y < char.y + char.height) or (obs.y + obs.height > char.y and obs.y + obs.height < char.y + char.height):
            return True
 
def game_loop():
    """ Main game loop """
    
    char.x = (display_width * 0.1)
    char.y = (display_height / 2)
    
    
    y_change = 0
    background.x = 0
    bomb.x = display_width
    coin.x = display_width
    bomb.y = random.randrange(0, display_height - bomb.height)
    coin.y = random.randrange(0, display_height - bomb.height)
    bomb_speed = -7
    
    coin_num = 0
    char_num = 0
    exp_num = 0
    
    global coin_amount
    coin_amount = 0
    crashed = False
    gameExit = False
    #game_intro()
    
    while not gameExit:
        for event in pygame.event.get():
        
            # User close window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            # User press keys
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    y_change = -(display_height/30)
                elif event.key == pygame.K_p:
                    paused()     

            # User release keys 
            if event.type == pygame.KEYUP:  # Release keys
                if event.key == pygame.K_SPACE:
                    y_change = 0
            
        # Background moving
        rel_background_x = background.x % background.width
        gameDisplay.blit(backgroundImg, (rel_background_x - background.width, 0))
        background.x -= 1
        if rel_background_x < display_width:
            gameDisplay.blit(backgroundImg, (rel_background_x,0))

        # Moving character inside boundaries
        y_change += 1
        if char.y + y_change > 0 and char.y + char.height + y_change < display_height:
            char.y += y_change
        else:
            y_change = 0
        
        angle = y_change * -1   
        
        if crashed != True:
            gameDisplay.blit(rot_center(char_anim[int(char_num%5)], angle), (char.x,char.y))
        else:
            gameDisplay.blit(rot_center(deadCharImg, 180), (char.x,char.y))
        char_num += 1/5
          
        
        # Moving coins
        gameDisplay.blit(coin_anim[int(coin_num%3)], (coin.x, coin.y))
        coin_num += 1/6
        coin.x += bomb_speed
        if coin.x < -(coin.width):
            coin.x = random.randrange(display_width, display_width*2)
            coin.y = random.randrange(0, display_height-bomb.height)

        # How bombs move and explode 
        if crashed == True:
            # After last explosion frame game ends
            if exp_num > 8: 
                    crash()        
            # Show explosion frames as animation
            else:
                img_rect = explosion_anim[exp_num].get_rect() 
                gameDisplay.blit(explosion_anim[exp_num], (bomb.x + bomb.width/2 - img_rect.width/2, bomb.y + bomb.height/2 - img_rect.height/2))
                exp_num += 1   
        else:
            gameDisplay.blit(bombImg, (bomb.x,bomb.y))
            bomb.x += bomb_speed 
            if bomb.x < -(bomb.width): 
                bomb.x = random.randrange(display_width, display_width*2)
                bomb.y = random.randrange(0, display_height-bomb.height)
                bomb_speed -= 1
        
        
         
        #  If the bomb hit the character
        if check_collision(char, bomb) == True:
            pygame.mixer.Sound.play(bomb_sound)
            crashed = True
            
        # If coin hit the character
        if check_collision(char, coin) == True:
            pygame.mixer.Sound.play(coin_sound)
            coin.x = random.randrange(display_width, display_width*2)
            coin.y = random.randrange(0, display_height-bomb.height)
            coin_amount += 1

        
        coins_collected(coin_amount)       
        pygame.display.update()
        clock.tick(FPS)

def game_intro():

    intro = True
    gameDisplay.fill(white)
    message_display("A FLYING GAME!", 80, display_height/5)
    message_display("Press SPACE to start flying!", 30, 3*display_height/5)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

game_intro()            
game_loop()
pygame.quit()
quit()
