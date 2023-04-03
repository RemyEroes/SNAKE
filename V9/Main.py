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

class MAIN:
    # creation du fruit et du serpent
    def __init__(self):
        self.snake = SNAKE(self.update_skin_from_file())
        self.fruit = FRUIT(self.update_fruit_from_file())
        self.difficulty = self.update_diff_from_file() #----------------------------------------------------------------------------------- DIFFICULTÉ DU JEU
        ## ON DEFINIT QUELLE DIFFOCULTE ON UTILISE
        #if self.difficulty == 'obstacle-1' or self.difficulty == 'obstacle-2' or self.difficulty == 'extreme':
        self.obstacles = OBSTACLE(self.difficulty)
        self.timer = TIMER()
        self.map =  self.update_map_from_file()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_map()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        ## SI DIFFICULTE OBSTACLES
        print(self.difficulty)
        if self.difficulty == 'obstacle-1' or self.difficulty == 'obstacle-2' or self.difficulty == 'extreme':
            self.obstacles.draw_obstacle() # dessine les obstacles obstacles
        
        self.timer.draw_timer() #dessine le timer
        

    def check_collision(self):
        # check si la tete touche le fruit
        if self.fruit.pos == self.snake.body[0]:
            # repositionner le fruit
            self.fruit.randomize()
            # ajouter un block au serpent            
            self.snake.add_block()
            # jouer le son crunch
            self.snake.play_eat_sound()

        # si le fruit apparait sur le corps du serpent
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        # si le serpent sort du jeu
        if not 0 <= self.snake.body[0].x < cell_number:  # gauche et droite
            game_over.facondemourir=str('AIE ! Un mur...') # façon de mourrir c'est le mur
            print(game_over.facondemourir)
            self.game_over()
        if not 0 <= self.snake.body[0].y < cell_number:  # haut et bas
            game_over.facondemourir=str('AIE ! Un mur...') # façon de mourrir c'est le mur
            print(game_over.facondemourir)
            self.game_over()

        # si le serpent se touche
        for block in self.snake.body[1:]:
            # si un block est identique à la tete du serpent c'ets qu'il s'est rentré dedans
            if block == self.snake.body[0]:
                game_over.facondemourir=str("Ouich ! je me suis mordu") # façon de mourrir c'est le mur
                print(game_over.facondemourir)
                self.game_over()

        
        # si le serpent touche une case obstacle
        ## UNIQUEMENT SI DIFFICULTE OBSTACLES
        if self.difficulty == 'obstacle-1' or self.difficulty == 'obstacle-2' or self.difficulty == 'extreme':
            nb_obstacles = len(main_game.obstacles.obstacles)
            for index in range(int(nb_obstacles)):
                if (self.snake.body[0].x == main_game.obstacles.obstacles[index].x and self.snake.body[0].y == main_game.obstacles.obstacles[index].y ) :
                    game_over.facondemourir=str('Pardi ! Un obstacle...') # façon de mourrir c'est un obstacle
                    print(game_over.facondemourir)
                    self.game_over()
            
    def game_over(self): 
        self.snake = SNAKE(self.update_skin_from_file())
        main_game.snake.reset_snake()
        ecran_game_over()

    def draw_grass(self):

        grass_color = (152, 171, 116)

        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

        # #AVEC IMAGE
        # map_rect = grass.get_rect(center=(cell_size*cell_number/2, cell_size*cell_number/2))

        # # RENDER
        # screen.blit(grass, map_rect)

    def draw_map(self):
        #IMAGE
        map_world = pygame.image.load('Graphics/map/'+self.map+'.png').convert_alpha()  
        map_rect = map_world.get_rect(center=(cell_size*cell_number/2, cell_size*cell_number/2))

        # RENDER
        screen.blit(map_world, map_rect)
    
    def draw_titre_menu(self):
        # texte
        titre_text = str('Bienvenue sur SNAKE !')  # vous etes mort
        titre_surface = game_font.render(titre_text, True, (255, 255, 255))
        titre_x = int(cell_size*cell_number/2)  # position x du titre
        titre_y = int(cell_size*cell_number/6)  # position y du titre
        titre_rect = titre_surface.get_rect(center=(titre_x, titre_y))

        # RENDER
        screen.blit(titre_surface, titre_rect)

    def draw_score(self):
        fruit = pygame.image.load('Graphics/fruit/'+str(self.fruit.fruit)+'.png').convert_alpha()  # image de fruit
        # score
        # score en fonction de la taille du serpent (-3 du corps du début)
        score_text = str(len(self.snake.body)-3)
        score_surface = game_font.render(score_text, True, (0, 0, 0))
        score_x = int(cell_size*cell_number - 60)  # position x du score
        score_y = int(cell_size*cell_number - 40)  # position y du score
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)
        # fuit a coté
        fruit_rect = fruit.get_rect(
            midright=(score_rect.left, score_rect.centery))
        # background score
        # bg_rect =pygame.Rect(pomme_rect.left,pomme_rect.top-10,int(pomme_rect.width+score_rect.width)+20,pomme_rect.height+10)

        # RENDER
        # pygame.draw.rect(screen,(255,255,255),bg_rect)
        screen.blit(fruit, fruit_rect)
        screen.blit(score_surface, score_rect)

    def update_skin_from_file(self):
        fichier = open("current_skin.txt", "r")
        contenu = fichier.read()
        print(contenu)

        skin = contenu
        return skin

    def update_fruit_from_file(self):
        fichier = open("current_fruit.txt", "r")
        contenu = fichier.read()
        print(contenu)

        fruit = contenu
        return fruit

    def update_map_from_file(self):
        fichier = open("current_map.txt", "r")
        contenu = fichier.read()
        print(contenu)

        map_world = contenu
        return map_world

    def update_diff_from_file(self):
        fichier = open("current_diff.txt", "r")
        contenu = fichier.read()
        print(contenu)

        diff = contenu
        self.difficulty= str(diff)
        return str(diff)
