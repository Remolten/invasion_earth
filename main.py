import pygame
from pygame.locals import *

import sys
import random

import __init__

from player import *
from alien import *

#Use this to find an optimum resolution
OS = __init__.find_os()
max_screen_size_x, max_screen_size_y = __init__.find_resolution(OS)
screen_size_x, screen_size_y = __init__.set_resolution(max_screen_size_x,
                                                       max_screen_size_y)
#Do this just in case the exit fullscreen
__init__.set_position(max_screen_size_x, screen_size_x)

pygame.init()
#Untested potential hack for Linux
'''if fullscreen:
    window = pygame.display.set_mode((screen_size_x, screen_size_y), FULLSCREEN)
    screen_size_x, screen_size_y = pygame.display.get_info()
    pygame.display.set_fullscreen = False
    pygame.display.set_mode((screen_size_x, screen_size_y))'''
#Will always run for now
window = pygame.display.set_mode((screen_size_x, screen_size_y), FULLSCREEN)
pygame.display.set_caption('Invasion Earth')
#pygame.display.set_icon('my_logo_icon.png')
clock = pygame.time.Clock()
background = pygame.image.load('background.png').convert()
player = Player(screen_size_x, screen_size_y)
player_group = pygame.sprite.GroupSingle()
player_group.add(player)
aliens = OrderedUpdatesModded()
fullscreen = True

def main():
    global fullscreen
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
                if event.key == K_LSHIFT:
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
                if event.key == K_LSHIFT:
                    player.flash = False

            if event.type == MOUSEBUTTONDOWN:
                #Left = 1, Scroll Wheel = 2 Right = 3 Close = 6 Far = 7
                #Only trigger on left mouse clicks
                if event.button == 1:
                    player.shooting = True
                
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    player.shooting = False

        #Fills the screen with the background
        for y in range(screen_size_y / 256 + 1):
            for x in range(screen_size_x / 256 + 1):
                window.blit(background, (x * 256, y * 256))
                
        if random.randint(0, 120) == 11:
            alien = Alien(screen_size_x, screen_size_y)
            aliens.add(alien)
        
        groupcollidemodded(aliens, player.bolts_group)
        aliens.update()
        aliens.draw(window)
        player.new_bolts()
        player.bolts_group.update()
        player.bolts_group.draw(window)
        player.update(screen_size_x, screen_size_y)
        player_group.draw(window)
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
