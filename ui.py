import pygame
from pygame.locals import *

#For quitting
import sys

#TODO time to make a main menu class implementing buttons

class Button():
    def __init__(self, window, pos, text=None):
        self.window = window
        self.rect = pygame.Rect(pos[0], pos[1], 190, 49)
        self.images = {'normal': pygame.image.load('blue_button00.png').convert_alpha(), 'down': pygame.image.load('blue_button01.png').convert_alpha()}
        #Temporary value so it won't trigger automatically
        self.click_down_pos = (-1111, -1111)
        self.click_up_pos = (-1111, -1111)
        self.font = pygame.font.Font('kenvector_future.ttf', 20)
        self.text = self.font.render(text, True, (255, 255, 255))
        self.text_size = self.font.size(text)
        self.text_rect = pygame.Rect(self.rect.x + 4 + ((self.rect.w - self.text_size[0]) / 2), self.rect.y + ((self.rect.h - self.text_size[1]) / 2), self.text_size[0], self.text_size[1])
        
    def update(self, events):
        #If using by itself, you need to add a background or fill method
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.click_up_pos = (-1111, -1111)
                self.click_down_pos = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONUP:
                self.click_down_pos = (-1111, -1111)
                self.click_up_pos = pygame.mouse.get_pos()
                
            if self.rect.collidepoint(self.click_down_pos):
                self.window.blit(self.images['down'], self.rect)
            elif self.rect.collidepoint(self.click_up_pos):
                return 'clicked'
            else:
                self.window.blit(self.images['normal'], self.rect)
        
        self.window.blit(self.text, self.text_rect)
        
class Menu():
    def __init__(self, number_buttons, window, text=None, background=None):
        self.buttons = []
        self.window = window
        self.background = background
        for number in range(number_buttons):
            self.buttons.append(Button(window, (window.get_width() / 2 - 95, window.get_height() / 2 - ((number_buttons / 2) * 60) + 60 * number), text[number]))
            
    def update(self, events):
        if self.background == None:
            self.window.fill((0, 0, 0))
        else:
            self.window.blit(self.background, (0, 0))
            
        for button in self.buttons:
            if button.update(events) == 'clicked':
                #The following code below is game specific
                #Could generalize by adding an input for setting what to do when clicked
                if button == self.buttons[0]:
                    return 'Start Game'
                elif button == self.buttons[1]:
                    pass
                elif button == self.buttons[2]:
                    pygame.quit()
                    sys.exit()
