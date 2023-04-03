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


class GAMEOVER:
    def __init__(self):
        self.volume = .5
        self.difficulty = 'aucun'
        self.facondemourir = 'mur'


    def update(self):
        self.draw_elements_game_over()

    def draw_elements_game_over(self):
        self.draw_background_menu()
        self.draw_tete_de_mort_menu()
        self.draw_dead_menu()
        self.draw_current_score_menu()
        self.draw_high_score_menu()
        self.draw_menu_button()
        self.draw_relancer_button()

    def start_game(self):
        self.snake.reset_snake()
        del main_game

    def draw_background_menu(self):
        background_menu_color = (10, 10, 10)
        bg_menu_rect = pygame.Rect(0, 0, cell_size*cell_number, cell_number*cell_size)

        # RENDER
        pygame.draw.rect(screen, background_menu_color, bg_menu_rect)

    def draw_tete_de_mort_menu(self):
        # tete de mort
        tete_de_mort_rect = tete_de_mort.get_rect(
            center=(cell_size*cell_number/2, cell_size*cell_number/2))

        # RENDER
        screen.blit(tete_de_mort, tete_de_mort_rect)

    def draw_dead_menu(self):
        # texte
        dead_text = str(self.facondemourir)  # vous etes mort
        dead_surface = game_font.render(dead_text, True, (255, 255, 255))
        dead_x = int(cell_size*cell_number/2)  # position x du titre
        dead_y = int(cell_size*cell_number/3)  # position y du titre
        dead_rect = dead_surface.get_rect(center=(dead_x, dead_y))

        # RENDER
        screen.blit(dead_surface, dead_rect)

    def draw_current_score_menu(self):
        # texte
        # score atteint durant la partie ----------------------------------------- METTRE LE SCORE APRES ---------
        dead_text = str('Votre score : ' + str('3'))
        dead_surface = game_font_small.render(dead_text, True, (255, 255, 255))
        # position x du current score
        dead_x = int((cell_size*cell_number/3)-40)
        dead_y = int(2*cell_size*cell_number/3)  # position y du current score
        dead_rect = dead_surface.get_rect(center=(dead_x, dead_y))

        # RENDER
        screen.blit(dead_surface, dead_rect)

    def draw_high_score_menu(self):
        # texte
        # score atteint durant la partie ----------------------------------------- METTRE LE SCORE APRES ---------
        high_text = str('Score Max : ' + str('56'))
        high_surface = game_font_small.render(high_text, True, (255, 255, 255))
        # position x du high score
        high_x = int((2*cell_size*cell_number/3)+40)
        high_y = int(2*cell_size*cell_number/3)  # position y du high score
        high_rect = high_surface.get_rect(center=(high_x, high_y))

        # RENDER
        screen.blit(high_surface, high_rect)

    def draw_menu_button(self):

        # Couleur texte
        couleur_texte_menu = (255, 255, 255)
        couleur_texte_menu_hover = (255, 0, 0)

        # zone cliquable
        zone_cliquable = pygame.rect.Rect(160, 640, 140, 50)
        # pygame.draw.rect(screen, (0,0,0), zone_cliquable)

        # texte MENU
        menu_text = str('MENU')  # MENU

        # Bouton change de couleur si hover
        if zone_cliquable.collidepoint(pygame.mouse.get_pos()):
            couleur_texte = couleur_texte_menu_hover
        else:
            couleur_texte = couleur_texte_menu

        menu_surface = game_font_small.render(menu_text, True, couleur_texte)
        menu_x = int((cell_size*cell_number/3)-40)  # position x du bouton menu
        menu_y = int(5*cell_size*cell_number/6)  # position y du bouton menu
        menu_rect = menu_surface.get_rect(center=(menu_x, menu_y))

        # RENDER
        screen.blit(menu_surface, menu_rect)

    def draw_relancer_button(self):

        # Couleur texte
        couleur_texte_menu = (255, 255, 255)
        couleur_texte_menu_hover = (255, 0, 0)

        # zone cliquable
        zone_cliquable = pygame.rect.Rect(460, 640, 200, 50)
        # pygame.draw.rect(screen, (34,0,0), zone_cliquable)

        # texte MENU
        menu_text = str('RELANCER')  # MENU

        # Bouton change de couleur si hover
        if zone_cliquable.collidepoint(pygame.mouse.get_pos()):
            couleur_texte = couleur_texte_menu_hover
        else:
            couleur_texte = couleur_texte_menu

        menu_surface = game_font_small.render(menu_text, True, couleur_texte)
        # position x du bouton menu
        menu_x = int((3*cell_size*cell_number/4)-40)
        menu_y = int(5*cell_size*cell_number/6)  # position y du bouton menu
        menu_rect = menu_surface.get_rect(center=(menu_x, menu_y))

        # RENDER
        screen.blit(menu_surface, menu_rect)
