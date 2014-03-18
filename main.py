import pygame
from pygame.locals import *

#Use multiple cores etc.
#Distribute throughout individual functions
#import pp

import sys
import random

import __init__

from player import *
from alien import *
from powerup import *
from ui import *

#Use this to find an optimum resolution
OS = __init__.find_os()
max_screen_size_x, max_screen_size_y = __init__.find_resolution(OS)
screen_size_x, screen_size_y = __init__.set_resolution(max_screen_size_x,
                                                       max_screen_size_y)
#Do this just in case they exit fullscreen
__init__.set_position(max_screen_size_x, screen_size_x)

pygame.init()
window = pygame.display.set_mode((screen_size_x, screen_size_y), FULLSCREEN)
pygame.display.set_caption('Invasion Earth')
health_image = pygame.image.load('playerLife1_blue.png').convert_alpha()
pygame.display.set_icon(health_image)
clock = pygame.time.Clock()
background = pygame.image.load('background.png').convert()
window_rect = pygame.Rect(0, 0, screen_size_x, screen_size_y)
player = Player(window_rect)
player_group = pygame.sprite.GroupSingle()
player_group.add(player)
aliens = OrderedUpdatesModded()
powerups = OrderedUpdatesModded()
fullscreen = True
active_powerup = None

#WIP
#TODO implement this into Main_Menu class
def main_menu():
    global fullscreen
    main_menu = Menu(3, window, text=['Start Game', 'Options', 'Quit'])
    while True:
        for event in pygame.event.get():
            #Bug here where events needs to be inside the for loop???
            #Otherwise it glitches out, no idea why
            #This means it will only take one event per loop through
            #Could cause a bug if user clicks at same time as pressing key, unlikely tho
            events = []
            events.append(event)
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    if fullscreen:
                        pygame.display.set_mode((screen_size_x, screen_size_y))
                        fullscreen = False
                    else:
                        pygame.display.set_mode((screen_size_x, screen_size_y),
                                                FULLSCREEN)
                        fullscreen = True
                        
        state = main_menu.update(events)
        if state == 'Start Game':
            break
        elif state == 'Options':
            pass
        elif state == 'Quit':
            pygame.quit()
            sys.exit()
        pygame.display.update()
        clock.tick(60)

def main():
    global fullscreen, active_powerup
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pass
                if event.key == K_UP or event.key == ord('w'):
                    player.move_up = True
                    player.move_down = False
                if event.key == K_DOWN or event.key == ord('s'):
                    player.move_down = True
                    player.move_up = False
                if event.key == K_LEFT or event.key == ord('a'):
                    player.move_left = True
                    player.move_right = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    player.move_right = True
                    player.move_left = False
                if event.key == K_SPACE:
                    player.shooting = True
                if event.key == K_LSHIFT or event.key == K_RSHIFT:
                    player.flash = True
                                
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    if fullscreen:
                        pygame.display.set_mode((screen_size_x, screen_size_y))
                        fullscreen = False
                    else:
                        pygame.display.set_mode((screen_size_x, screen_size_y),
                                                FULLSCREEN)
                        fullscreen = True
                if event.key == K_UP or event.key == ord('w'):
                    player.move_up = False
                if event.key == K_DOWN or event.key == ord('s'):
                    player.move_down = False
                if event.key == K_LEFT or event.key == ord('a'):
                    player.move_left = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    player.move_right = False
                if event.key == K_SPACE:
                    player.shooting = False
                if event.key == K_LSHIFT or event.key == K_RSHIFT:
                    player.flash = False

            if event.type == MOUSEBUTTONDOWN:
                #Left = 1, Scroll Wheel = 2 Right = 3 Close = 6 Far = 7
                #Only triggers on left mouse clicks
                if event.button == 1:
                    player.shooting = True
                
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    player.shooting = False

        #Fills the screen with the background
        for y in range(screen_size_y / 256 + 1):
            for x in range(screen_size_x / 256 + 1):
                window.blit(background, (x * 256, y * 256))
                
        #Print amount of player lives
        #TODO use lives with collisions etc.
        #When finished git commit for it and push
        for i in range(player.health):
            window.blit(health_image, (10 + i * 43, 10))
            
        #Maybe move this code
        #TODO Change this to spritecollide group function
        for alien in aliens.sprites():
            if player.rect.colliderect(alien):
                alien.kill()
                if player.active_powerup != 'shield':
                    player.damage()
                else:
                    player.active_powerup = None
                
        #Do something when player hits a powerup
        for powerup in powerups.sprites():
            if player.rect.colliderect(powerup):
                player.active_powerup = powerup.type
                powerup.kill()
                
        #Just a temporary test
        if player.dead:
            print('Game Over')
            pygame.quit()
            sys.exit()
                
        if random.randint(0, 120) == 11:
            alien = Alien(window_rect)
            aliens.add(alien)
            
        if player.active_powerup == 'bolt':
            aliens.empty()
            player.active_powerup = None
            
        if random.randint(0, 240) == 11 and player.active_powerup == None:
            powerup = Powerup(window_rect)
            powerups.add(powerup)
        
        groupcollidemodded(aliens, player.bolts_group)
        if player.active_powerup != 'star':
            aliens.update()
        else:
            pass
            #Not sure about this
            #Need to add a timer
            #player.active_powerup = None
            
        aliens.draw(window)
        powerups.update()
        powerups.draw(window)
        player.new_bolts()
        player.bolts_group.update()
        player.bolts_group.draw(window)
        player.update()
        player_group.draw(window)
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main_menu()
    main()
