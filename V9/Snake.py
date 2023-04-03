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

class SNAKE:
    def __init__(self, skin):
        self.body = [Vector2(3, 7), Vector2(2, 7), Vector2(1, 7)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        ####
        self.skin = str(skin)  # --------------------------- a changer apres

        self.head_up = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/body_horizontal.png').convert_alpha()

        """ CURVE BODY """
        self.body_tr = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(
            'Graphics/skin/'+str(self.skin)+'/body_bl.png').convert_alpha()

        # SOUND
        self.eat_sound = self.chose_sound_from_fruit()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        

        # pour chaque block et son index
        for index, block in enumerate(self.body):
            # connaitre la position
            x_pos = int(block.x*cell_size)
            y_pos = int(block.y*cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # Dans quelle direction va la tete
            if index == 0:  # la tete
                screen.blit(self.head, block_rect)
            elif index == len(self.body)-1:  # la queue
                screen.blit(self.tail, block_rect)
            else:  # les blocks entre
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                # vertical ou horizontal
                if previous_block.x == next_block.x:  # vertical
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:  # horizontal
                    screen.blit(self.body_horizontal, block_rect)
                else:  # les coins du serpent
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)  # coin top left
                    elif (previous_block.y == 1 and next_block.x == -1) or (previous_block.x == -1 and next_block.y == 1):
                        # coin bottom left
                        screen.blit(self.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)  # coin top right
                    elif (previous_block.y == 1 and next_block.x == 1) or (previous_block.x == 1 and next_block.y == 1):
                        # coin bottom right
                        screen.blit(self.body_br, block_rect)

    # update la direction de la tete

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left  # vers la gauche
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right  # vers la droite
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up  # vers le haut
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down  # vers le bas

    # update la direction de la queue
    def update_tail_graphics(self):
        # dernier et avant dernier element
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left  # vers la gauche
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right  # vers la droite
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up  # vers le haut
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down  # vers le bas

    def move_snake(self):
        if self.new_block == True:  # s'il y a une nouveau block
            body_copy = self.body[:]  # copie du corps
            # on ajoute un element tout devant (la tete) avec une certaine direction
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:  # s'il n'y a pas de nouvel element
            body_copy = self.body[:-1]  # copie du corps sans le dernier block
            # on ajoute un element tout devant (la tete) avec une certaine direction
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_eat_sound(self):
        self.eat_sound.play()
    
    def reset_snake(self):
        self.body = [Vector2(3, 7), Vector2(2, 7), Vector2(1, 7)]

    def get_fruit_from_file(self):
        # change le fruit dans le fichier
        fichier = open("current_fruit.txt", "r")
        contenu = fichier.read()
        return str(contenu)
        
    def chose_sound_from_fruit(self):
        self.eat_sound = pygame.mixer.Sound('Sound/eat-'+self.get_fruit_from_file()+'.mp3')
 