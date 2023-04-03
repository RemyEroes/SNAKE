import pygame
import sys
import random
from pygame.math import Vector2
import re

from Timer import Timer
from Snake import Snake
from Main import Main
from Fruit import Fruit
from Menu import Menu
from Snake_game import Snake_game
from Obstacle import Obstacle

class FRUIT:
    def __init__(self, fruit):
        self.fruit = str(fruit)
        self.randomize()

    def draw_fruit(self):
        fruit = pygame.image.load('Graphics/fruit/'+str(self.fruit)+'.png').convert_alpha()  # image de fruit
        
        # les positions sont déterminées pas un certain nombre de fois la taille d'une cellule
        fruit_rect = pygame.Rect(
            int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size)
        screen.blit(fruit, fruit_rect)  # image de fruit
        # pygame.draw.rect(screen,(199,57,48),fruit_rect)

    def randomize(self):  # creer un element a une position random
        self.x = random.randint(0, cell_number-1)  # random x
        self.y = random.randint(0, cell_number-1)  # random y
        self.pos = Vector2(self.x, self.y)
