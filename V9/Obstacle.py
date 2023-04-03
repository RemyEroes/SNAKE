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

class OBSTACLE:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.style = 'none'
        self.obstacles = []
        self.randomize(self.difficulty)

    def draw_obstacle(self):
        self.update_diff_from_file()
        nb_obstacles = len(self.obstacles)

        for index in range(nb_obstacles):
            #print(index, "x: "+str(self.obstacles[index].x),"y: "+str(self.obstacles[index].y))
            obstacle_rect = pygame.Rect(int(self.obstacles[index].x*cell_size), int(
                self.obstacles[index].y*cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (199, 57, 48), obstacle_rect)

    def randomize(self, dif):  # creer un element a une position random
        self.update_diff_from_file()
        nb_obstacles = self.get_nb_obstacles_from_difficulty()
        # SI ON EST PAS EN MODE AUCUN OBSTACLE
        if (self.difficulty != 'aucun'):
            for i in range(0,nb_obstacles):
                self.x = random.randint(1, cell_number-1)  # random x
                self.y = random.randint(1, cell_number-1)  # random y
                
                # pas en bas droite
                if (Vector2(self.x, self.y)!=Vector2(19,19) and Vector2(self.x, self.y)!=Vector2(19,18) and Vector2(self.x, self.y)!=Vector2(19,17) and Vector2(self.x, self.y)!=Vector2(18,19) and Vector2(self.x, self.y)!=Vector2(18,17) and Vector2(self.x, self.y)!=Vector2(17,17)):
                    self.pos = Vector2(self.x, self.y)
                    self.obstacles.append(self.pos)
                    i += 1
            
    
    def get_nb_obstacles_from_difficulty(self):
        fichier = open("current_diff.txt", "r")
        dif = fichier.read()
        
        if (dif == 'obstacle-1'):
            nb_obstacles = 3
        elif (dif == 'obstacle-2'):
            nb_obstacles = 6
        elif (dif == 'extreme'):
            nb_obstacles = 6
        else:
            nb_obstacles=0
        return nb_obstacles

    def update_diff_from_file(self):
        fichier = open("current_diff.txt", "r")
        contenu = fichier.read()
        print(contenu)

        diff = contenu
        self.difficulty= str(diff)
        return str(diff)