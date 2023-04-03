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


pygame.mixer.pre_init(44100, -16, 2, 512)  # preload le son
pygame.init()

cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size)) # TAILLE DE LA FENETRE 
clock = pygame.time.Clock()  # objet clock

game_font = pygame.font.Font('Font/SuperMario256.ttf', 50)
game_font_small = pygame.font.Font('Font/SuperMario256.ttf', 30)
game_font_very_small = pygame.font.Font('Font/SuperMario256.ttf', 25)
tete_de_mort = pygame.image.load('Graphics/death-skull.png').convert_alpha()  # image tete de mort

SCREEN_UPDATE = pygame.USEREVENT
# TIMER qui fait le screen update toutes les 150 ms
pygame.time.set_timer(SCREEN_UPDATE, 150)


menu_game = MENU()
main_game = MAIN()
game_over = GAMEOVER()
timer = TIMER()



def play_game():
    main_game.snake.chose_sound_from_fruit() # CHANGE LE SONS 
    main_game.update_map_from_file() # change la map
    main_game.update_diff_from_file() # change la difficulté
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # si on click sur la croix on quite le jeu
                pygame.quit()
                sys.exit()  # quite tous les sytemes restants
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:  # quand on press une touche + ON EMPECHE DE POUVOIR SE RETOURNER
                if event.key == pygame.K_UP:  # fleche du haut
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)

                if event.key == pygame.K_RIGHT:  # fleche de droite
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)

                if event.key == pygame.K_DOWN:  # fleche du bas
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)

                if event.key == pygame.K_LEFT:  # fleche de gauche
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)

        screen.fill((169, 190, 129))  # couleur du background
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)  # framerate maximal du jeu


def ecran_game_over():
    while True:
        # zones cliquables
        zone_cliquable_menu = pygame.rect.Rect(160, 640, 140, 50)
        zone_cliquable_relancer = pygame.rect.Rect(460, 640, 200, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # si on click sur la croix on quite le jeu
                pygame.quit()
                sys.exit()  # quite tous les sytemes restants
            if event.type == SCREEN_UPDATE:
                game_over.update()

            # Vérifier si l'utilisateur a cliqué sur le bouton menu pendant le game over
            if event.type == pygame.MOUSEBUTTONUP and zone_cliquable_menu.collidepoint(event.pos):
                menu_du_jeu()

            # Vérifier si l'utilisateur a cliqué sur le bouton 'relancer' pendant le game over
            if event.type == pygame.MOUSEBUTTONUP and zone_cliquable_relancer.collidepoint(event.pos):
                play_game()

        screen.fill((19, 10, 19))  # couleur du background
        game_over.draw_elements_game_over()
        pygame.display.update()
        clock.tick(60)  # framerate maximal du jeu


def menu_du_jeu():
    menu_game.reset_files()
    while True:
        # zones cliquables
        zone_cliquable_play = pygame.rect.Rect(325, 665, 150, 60)
        zone_skin_plus = pygame.rect.Rect(235, 565, 50, 50)
        zone_skin_moins = pygame.rect.Rect(55, 565, 50, 50)
        zone_fruit_plus = pygame.rect.Rect(555, 565, 50, 50)
        zone_fruit_moins = pygame.rect.Rect(335, 565, 50, 50)
        zone_map_plus = pygame.rect.Rect(55, 445, 50, 50)
        zone_map_moins = pygame.rect.Rect(225, 445, 50, 50)
        zone_diff_moins = pygame.rect.Rect(55, 325, 50, 50)
        zone_diff_plus = pygame.rect.Rect(225, 325, 50, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # si on click sur la croix on quite le jeu
                pygame.quit()
                sys.exit()  # quite tous les sytemes restants
            if event.type == SCREEN_UPDATE:
                game_over.update()

            # Vérifier si l'utilisateur a cliqué sur le bouton play
            if event.type == pygame.MOUSEBUTTONUP and zone_cliquable_play.collidepoint(event.pos):
                play_game()

            #-------------------------------------------------------------------- BOUTONS SKIN-------------------------    
            
            # Vérifier si l'utilisateur a cliqué sur le bouton skin plus
            if event.type == pygame.MOUSEBUTTONUP and zone_skin_plus.collidepoint(event.pos):
                menu_game.change_skin_plus()

            # Vérifier si l'utilisateur a cliqué sur le bouton skin moins
            if event.type == pygame.MOUSEBUTTONUP and zone_skin_moins.collidepoint(event.pos):
                menu_game.change_skin_moins()
               
            #-------------------------------------------------------------------- BOUTONS FRUIT------------------------- 
            # Vérifier si l'utilisateur a cliqué sur le bouton fruit plus
            if event.type == pygame.MOUSEBUTTONUP and zone_fruit_plus.collidepoint(event.pos):
                menu_game.change_fruit_plus()

            # Vérifier si l'utilisateur a cliqué sur le bouton skin moins
            if event.type == pygame.MOUSEBUTTONUP and zone_fruit_moins.collidepoint(event.pos):
                menu_game.change_fruit_moins()
                
            #-------------------------------------------------------------------- BOUTONS MAP------------------------- 
            # Vérifier si l'utilisateur a cliqué sur le bouton map plus
            if event.type == pygame.MOUSEBUTTONUP and zone_map_plus.collidepoint(event.pos):
                menu_game.change_map_plus()

            # Vérifier si l'utilisateur a cliqué sur le bouton map moins
            if event.type == pygame.MOUSEBUTTONUP and zone_map_moins.collidepoint(event.pos):
                menu_game.change_map_moins()
            
            #-------------------------------------------------------------------- BOUTONS DIFFICULTE------------------------- 
            # Vérifier si l'utilisateur a cliqué sur le bouton diff plus
            if event.type == pygame.MOUSEBUTTONUP and zone_diff_plus.collidepoint(event.pos):
                menu_game.change_diff_plus()

            # Vérifier si l'utilisateur a cliqué sur le bouton diff moins
            if event.type == pygame.MOUSEBUTTONUP and zone_diff_moins.collidepoint(event.pos):
                menu_game.change_diff_moins()
            
            

            # Vérifier si l'utilisateur a cliqué sur le bouton 'relancer' pendant le game over
            # if event.type == pygame.MOUSEBUTTONUP and zone_cliquable_relancer.collidepoint(event.pos):
                # play_game()

        menu_game.draw_elements_menu()
        pygame.display.update()
        clock.tick(60)  # framerate maximal du jeu


# LANCER LE MENU DE DÉPART
menu_du_jeu()
# ecran_game_over()
