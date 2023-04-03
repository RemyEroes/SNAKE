
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

class MENU:
    def __init__(self):
        self.volume = 0.5
        self.difficulty = 'aucun'
        self.map = 'lune'
        self.skin = 'bleu'
        self.fruit = 'pomme'
        self.difficulty = 'aucun'

    def update(self):
        self.draw_elements_menu()

    def draw_elements_menu(self):
        self.draw_background_menu()
        self.draw_titre_menu()
        self.draw_high_score()
        self.draw_diff_selector()
        self.draw_map_selector()
        self.draw_map_preview()
        self.draw_skin_selector()
        self.draw_snake_preview()
        self.draw_fruit_selector()
        self.draw_fruit_preview()
        self.draw_play_button()

    def draw_background_menu(self):
        background_menu_color = (153, 198, 98)
        bg_menu_rect = pygame.Rect(
            0, 0, cell_size*cell_number, cell_number*cell_size)

        # RENDER
        pygame.draw.rect(screen, background_menu_color, bg_menu_rect)

    def draw_titre_menu(self):
        # texte
        titre_text = str('Bienvenue sur SNAKE !')  # vous etes mort
        titre_surface = game_font.render(titre_text, True, (255, 255, 255))
        titre_x = int(cell_size*cell_number/2)  # position x du titre
        titre_y = int(cell_size*cell_number/6)  # position y du titre
        titre_rect = titre_surface.get_rect(center=(titre_x, titre_y))

        # RENDER
        screen.blit(titre_surface, titre_rect)

    def draw_high_score(self):
        # texte
        # score atteint durant la partie ----------------------------------------- METTRE LE SCORE APRES ---------
        high_text = str('Record actuel : ' + str('56'))
        high_surface = game_font_small.render(high_text, True, (0, 0, 0))
        # position x du high score
        high_x = int((4*cell_size*cell_number/5)-30)
        high_y = int(1*cell_size*cell_number/4)  # position y du high score
        high_rect = high_surface.get_rect(center=(high_x, high_y))

        # RENDER
        screen.blit(high_surface, high_rect)

    #-------------------------------------------- SNAKE --------------------------------------------
    
    def draw_snake_preview(self):
        localisation_skin = 'Graphics/skin/' + \
            str(self.skin)+'/preview/'+str(self.skin)+'.png'
        skin_actuel = pygame.image.load(
            localisation_skin).convert_alpha()  # image skin à utiliser
        # SKIN
        skin_actuel_rect = skin_actuel.get_rect(
            center=((cell_size*cell_number/2)+40, cell_size*cell_number/2))

        # RENDER
        screen.blit(skin_actuel, skin_actuel_rect)

    def draw_skin_selector(self):
        # couleur texte
        couleur_bg = (255, 255, 255)
        couleur_texte = (0, 0, 0)
        couleur_titre_skin = (255, 255, 255)
        # elements
        zone_cliquable_droite = pygame.rect.Rect(235, 565, 50, 50)
        pygame.draw.rect(screen, (155, 155, 155), zone_cliquable_droite)
        zone_cliquable_gauche = pygame.rect.Rect(55, 565, 50, 50)
        pygame.draw.rect(screen, (155, 155, 155), zone_cliquable_gauche)

        bg_skin_selector = pygame.rect.Rect(105, 565, 130, 50)
        pygame.draw.rect(screen, couleur_bg, bg_skin_selector)

        # texte skin ("nom du skin")
        skin_text = str(self.skin)  # skin

        # titre skin
        skin_titre_text = str('skin')

        skin_surface = game_font_small.render(skin_text, True, couleur_texte)
        skin_rect = skin_surface.get_rect(center=(170, 593))
        # ------------------------------------------#
        skin_titre_surface = game_font_small.render(
            skin_titre_text, True, couleur_titre_skin)
        skin_titre_rect = skin_titre_surface.get_rect(center=(170, 540))

        # RENDER
        screen.blit(skin_titre_surface, skin_titre_rect)
        screen.blit(skin_surface, skin_rect)

    def change_skin_plus(self):
        skins = ['bleu', 'vert', 'rose', 'violet', 'malade', 'marin', 'noel']
        # combien y a t'il de skin
        nb_skin_max = len(skins)

        # chercher quel index on est
        for i in range(nb_skin_max):
            if skins[i] == self.skin:
                index_skin = i

        # ajoute 1 au skin sauf si on est déja au dernier
        if index_skin < nb_skin_max-1:
            index_skin += 1
            self.skin = skins[index_skin]
            # change le skin dans le fichier
            self.update_skin(skins[index_skin])

            # CHANGER LE SKIN
            del main_game.snake
            main_game.snake = SNAKE(main_game.update_skin_from_file())

        else:
            index_skin = 0
            self.skin = skins[index_skin]
            # change le skin dans le fichier
            self.update_skin(skins[index_skin])

            # CHANGER LE SKIN
            del main_game.snake
            main_game.snake = SNAKE(main_game.update_skin_from_file())

    def change_skin_moins(self):
        skins = ['bleu', 'vert', 'rose', 'violet', 'malade', 'marin', 'noel']
        # combien y a t'il de skin
        nb_skin_max = len(skins)

        # chercher quel index on est
        for i in range(nb_skin_max):
            if skins[i] == self.skin:
                index_skin = i

        # ajoute 1 au skin sauf si on est déja au dernier
        if index_skin > 0:
            index_skin -= 1
            self.skin = skins[index_skin]
            # change le skin dans le fichier
            self.update_skin(skins[index_skin])

            # CHANGER LE SKIN
            del main_game.snake
            main_game.snake = SNAKE(main_game.update_skin_from_file())

        else:
            index_skin = nb_skin_max-1
            self.skin = skins[index_skin]
            # change le skin dans le fichier
            self.update_skin(skins[index_skin])

            # CHANGER LE SKIN
            del main_game.snake
            main_game.snake = SNAKE(main_game.update_skin_from_file())

    def update_skin(self, skin):
        # change le skin dans le fichier
        fichier = open("current_skin.txt", "r")
        contenu = fichier.read()
        print("old skin"+contenu+"----- new skin"+str(skin))

        nom_fichier = "current_skin.txt"
        nouvelle_chaine = str(skin)

        with open(nom_fichier, 'w') as f:
            # Écriture le nouveau skin dans le fichier
            f.write(nouvelle_chaine)
    
    #-------------------------------------------- FRUIT --------------------------------------------
    
    def draw_fruit_preview(self):
        localisation_fruit = 'Graphics/fruit/' + \
        str(self.fruit)+'.png'
        fruit_actuel = pygame.image.load(
            localisation_fruit).convert_alpha()  # image fruit à utiliser
        # Fruit
        fruit_actuel_rect = fruit_actuel.get_rect(center=((cell_size*cell_number/2)+130, cell_size*cell_number/2))

        # RENDER
        screen.blit(fruit_actuel, fruit_actuel_rect)

    def draw_fruit_selector(self):
        # couleur texte
        couleur_bg = (255, 255, 255)
        couleur_texte = (0, 0, 0)
        couleur_titre_fruit = (255, 255, 255)
        # elements
        zone_cliquable_droite = pygame.rect.Rect(555, 565, 50, 50)
        pygame.draw.rect(screen, (155, 155, 155), zone_cliquable_droite)
        zone_cliquable_gauche = pygame.rect.Rect(335, 565, 50, 50)
        pygame.draw.rect(screen, (155, 155, 155), zone_cliquable_gauche)

        bg_fruit_selector = pygame.rect.Rect(385, 565, 170, 50)
        pygame.draw.rect(screen, couleur_bg, bg_fruit_selector)

        # texte fruit ("nom du fruit")
        fruit_text = str(self.fruit)  # fruit

        # titre skin
        fruit_titre_text = str('fruit')

        fruit_surface = game_font_small.render(fruit_text, True, couleur_texte)
        fruit_rect = fruit_surface.get_rect(center=(470, 593))
        # ------------------------------------------#
        fruit_titre_surface = game_font_small.render(
            fruit_titre_text, True, couleur_titre_fruit)
        fruit_titre_rect = fruit_titre_surface.get_rect(center=(470, 540))

        # RENDER
        screen.blit(fruit_titre_surface, fruit_titre_rect)
        screen.blit(fruit_surface, fruit_rect)

    def change_fruit_plus(self):
        fruits = ['pomme', 'banane', 'kiwi', 'pasteque', 'raisin', 'fraise', 'orange']
        # combien y a t'il de fruit
        nb_fruit_max = len(fruits)

        # chercher quel index on est
        for i in range(nb_fruit_max):
            if fruits[i] == self.fruit:
                index_fruit = i

        # ajoute 1 au fruit sauf si on est déja au dernier
        if index_fruit < nb_fruit_max-1:
            index_fruit += 1
            self.fruit = fruits[index_fruit]
            # change le fruit dans le fichier
            self.update_fruit(fruits[index_fruit])

            # CHANGER LE fruit
            del main_game.fruit
            main_game.fruit = FRUIT(main_game.update_fruit_from_file())
            main_game.snake.chose_sound_from_fruit() # CHANGE LE SONS 

        else:
            index_fruit = 0
            self.fruit = fruits[index_fruit]
            # change le fruit dans le fichier
            self.update_fruit(fruits[index_fruit])

            # CHANGER LE fruit
            del main_game.fruit
            main_game.fruit = FRUIT(main_game.update_fruit_from_file())
            main_game.snake.chose_sound_from_fruit() # CHANGE LE SONS 

    def change_fruit_moins(self):
        fruits = ['pomme', 'banane', 'kiwi', 'pasteque', 'raisin', 'fraise', 'orange']
        # combien y a t'il de fruit
        nb_fruit_max = len(fruits)

        # chercher quel index on est
        for i in range(nb_fruit_max):
            if fruits[i] == self.fruit:
                index_fruit = i

        # ajoute 1 au fruit sauf si on est déja au dernier
        if index_fruit > 0:
            index_fruit -= 1
            self.fruit = fruits[index_fruit]
            # change le fruit dans le fichier
            self.update_fruit(fruits[index_fruit])

            # CHANGER LE fruit
            del main_game.fruit
            main_game.fruit = FRUIT(main_game.update_fruit_from_file())
            main_game.snake.chose_sound_from_fruit() # CHANGE LE SONS 

        else:
            index_fruit = nb_fruit_max-1
            self.fruit = fruits[index_fruit]
            # change le fruit dans le fichier
            self.update_fruit(fruits[index_fruit])

            # CHANGER LE fruit
            del main_game.fruit
            main_game.fruit = FRUIT(main_game.update_fruit_from_file())
            main_game.snake.chose_sound_from_fruit() # CHANGE LE SONS 

    def update_fruit(self, fruit):
        # change le fruit dans le fichier
        fichier = open("current_fruit.txt", "r")
        contenu = fichier.read()
        #print("old fruit"+contenu+"----- new fruit"+str(fruit))

        nom_fichier = "current_fruit.txt"
        nouvelle_chaine = str(fruit)

        with open(nom_fichier, 'w') as f:
            # Écriture le nouveau fruit dans le fichier
            f.write(nouvelle_chaine)
            
    
    #-------------------------------------------- MAP --------------------------------------------
    
    def draw_map_preview(self):
        localisation_map = 'Graphics/map/'+str(self.map)+'-preview.png'
        map_actuel = pygame.image.load(
            localisation_map).convert_alpha()  # image map à utiliser
        # map
        map_actuel_rect = map_actuel.get_rect(center=((cell_size*cell_number/2)+70, cell_size*cell_number/2))

        # RENDER
        screen.blit(map_actuel, map_actuel_rect)

    def draw_map_selector(self):
        # couleur texte
        couleur_bg = (255, 255, 255)
        couleur_texte = (0, 0, 0)
        couleur_titre_map = (255, 255, 255)
        # elements
        zone_cliquable_droite = pygame.rect.Rect(55, 445, 50, 50)
        pygame.draw.rect(screen, (155, 155, 155), zone_cliquable_droite)
        zone_cliquable_gauche = pygame.rect.Rect(225, 445, 50, 50)
        pygame.draw.rect(screen, (155, 155, 155), zone_cliquable_gauche)

        bg_map_selector = pygame.rect.Rect(105, 445, 120, 50)
        pygame.draw.rect(screen, couleur_bg, bg_map_selector)

        # texte map ("nom du map")
        map_text = str(self.map)  # map

        # titre skin
        map_titre_text = str('map')

        map_surface = game_font_very_small.render(map_text, True, couleur_texte)
        map_rect = map_surface.get_rect(center=(165, 473))
        # ------------------------------------------#
        map_titre_surface = game_font_small.render(map_titre_text, True, couleur_titre_map)
        map_titre_rect = map_titre_surface.get_rect(center=(170, 420))

        # RENDER
        screen.blit(map_titre_surface, map_titre_rect)
        screen.blit(map_surface, map_rect)

    def change_map_plus(self):
        maps = ['lune', 'terre']
        # combien y a t'il de map
        nb_map_max = len(maps)

        # chercher quel index on est
        for i in range(nb_map_max):
            if maps[i] == self.map:
                index_map = i

        # ajoute 1 au map sauf si on est déja au dernier
        if index_map < nb_map_max-1:
            index_map += 1
            self.map = maps[index_map]
            # change le map dans le fichier
            self.update_map(maps[index_map])

            # CHANGER LE map
            main_game.update_map_from_file()
            
        else:
            index_map = 0
            self.map = maps[index_map]
            # change le map dans le fichier
            self.update_map(maps[index_map])

            # CHANGER LE map
            main_game.update_map_from_file()
    
    def change_map_moins(self):
        maps = ['lune', 'terre']
        # combien y a t'il de map
        nb_map_max = len(maps)

        # chercher quel index on est
        for i in range(nb_map_max):
            if maps[i] == self.map:
                index_map = i

        # ajoute 1 au map sauf si on est déja au dernier
        if index_map > 0:
            index_map -= 1
            self.map = maps[index_map]
            # change le map dans le fichier
            self.update_map(maps[index_map])

            # CHANGER LE map
            main_game.update_map_from_file()
            
        else:
            index_map = nb_map_max-1
            self.map = maps[index_map]
            # change le map dans le fichier
            self.update_map(maps[index_map])

            # CHANGER LE map
            main_game.update_map_from_file()

    def update_map(self, map):
        # change le map dans le fichier
        fichier = open("current_map.txt", "r")
        contenu = fichier.read()
        #print("old map"+contenu+"----- new map"+str(map))

        nom_fichier = "current_map.txt"
        nouvelle_chaine = str(map)

        with open(nom_fichier, 'w') as f:
            # Écriture le nouveau map dans le fichier
            f.write(nouvelle_chaine)


#-------------------------------------------- DIFFICULTÉ --------------------------------------------
    

    def draw_diff_selector(self):
        # couleur texte
        couleur_bg = (255, 255, 255)
        couleur_texte = (0, 0, 0)
        couleur_titre_diff = (255, 255, 255)
        # elements
        zone_cliquable_droite = pygame.rect.Rect(55, 325, 50, 50)
        pygame.draw.rect(screen, (155, 155, 155), zone_cliquable_droite)
        zone_cliquable_gauche = pygame.rect.Rect(225, 325, 50, 50)
        pygame.draw.rect(screen, (155, 155, 155), zone_cliquable_gauche)

        bg_diff_selector = pygame.rect.Rect(105, 325, 120, 50)
        pygame.draw.rect(screen, couleur_bg, bg_diff_selector)

        # texte diff ("nom du diff")
        diff_text = str(self.difficulty)  # diff

        # titre skin
        diff_titre_text = str('difficlute')

        diff_surface = game_font_very_small.render(diff_text, True, couleur_texte)
        diff_rect = diff_surface.get_rect(center=(165, 353))
        # ------------------------------------------#
        diff_titre_surface = game_font_small.render(diff_titre_text, True, couleur_titre_diff)
        diff_titre_rect = diff_titre_surface.get_rect(center=(170, 300))

        # RENDER
        screen.blit(diff_titre_surface, diff_titre_rect)
        screen.blit(diff_surface, diff_rect)

    def change_diff_plus(self):
        diffs = ['aucun', 'vitesse +', 'obstacle-1', 'obstacle-2', 'extreme']
        # combien y a t'il de diff
        nb_diff_max = len(diffs)

        # chercher quel index on est
        for i in range(nb_diff_max):
            if diffs[i] == self.difficulty:
                index_diff = i

        # ajoute 1 au diff sauf si on est déja au dernier
        if index_diff < nb_diff_max-1:
            index_diff += 1
            self.difficulty = diffs[index_diff]
            # change le diff dans le fichier
            self.update_diff(diffs[index_diff])

            # CHANGER LE diff
            main_game.obstacles = OBSTACLE(self.difficulty)
            main_game.update_diff_from_file()
            
        else:
            index_diff = 0
            self.difficulty = diffs[index_diff]
            # change le diff dans le fichier
            self.update_diff(diffs[index_diff])

            # CHANGER LE diff
            main_game.obstacles = OBSTACLE(self.difficulty)
            main_game.update_diff_from_file()
    
    def change_diff_moins(self):
        diffs = ['aucun', 'vitesse +', 'obstacle-1', 'obstacle-2', 'extreme']
        # combien y a t'il de diff
        nb_diff_max = len(diffs)

        # chercher quel index on est
        for i in range(nb_diff_max):
            if diffs[i] == self.difficulty:
                index_diff = i

        # ajoute 1 au diff sauf si on est déja au dernier
        if index_diff > 0:
            index_diff -= 1
            self.difficulty = diffs[index_diff]
            # change le diff dans le fichier
            self.update_diff(diffs[index_diff])

            # CHANGER LE diff
            main_game.obstacles = OBSTACLE(self.difficulty)
            main_game.update_diff_from_file()
            
        else:
            index_diff = nb_diff_max-1
            self.difficulty = diffs[index_diff]
            # change le diff dans le fichier
            self.update_diff(diffs[index_diff])

            # CHANGER LE diff
            main_game.obstacles = OBSTACLE(self.difficulty)
            main_game.update_diff_from_file()

    def update_diff(self, diff):
        # change le diff dans le fichier
        fichier = open("current_diff.txt", "r")
        contenu = fichier.read()
        #print("old diff"+contenu+"----- new diff"+str(diff))

        nom_fichier = "current_diff.txt"
        nouvelle_chaine = str(diff)

        with open(nom_fichier, 'w') as f:
            # Écriture le nouveau diff dans le fichier
            f.write(nouvelle_chaine)

    #-------------------------------------------- PLAY --------------------------------------------

    def draw_play_button(self):
        # Couleur texte
        couleur_texte_menu = (240, 0, 0)
        couleur_texte_menu_hover = (255, 255, 255)

        # zone cliquable
        zone_cliquable = pygame.rect.Rect(325, 665, 150, 60)
        # pygame.draw.rect(screen, (0,0,0), zone_cliquable)

        # texte PLAY
        play_text = str('PLAY')  # PLAY

        # Bouton change de couleur si hover
        if zone_cliquable.collidepoint(pygame.mouse.get_pos()):
            couleur_texte = couleur_texte_menu_hover
        else:
            couleur_texte = couleur_texte_menu

        play_surface = game_font.render(play_text, True, couleur_texte)
        play_x = int(cell_size*cell_number/2)  # position x du bouton play
        play_y = int(7*cell_size*cell_number/8)  # position y du bouton play
        play_rect = play_surface.get_rect(center=(play_x, play_y))

        # RENDER
        screen.blit(play_surface, play_rect)
    
    #-------------------------------------------- RESET A CHAQUE FOIS --------------------------------------------

    def reset_files(self):
        # reset les valeurs des fichiers
        
        # 1 -skin
        nom_fichier = "current_skin.txt"
        reset_chaine = str('bleu')
        with open(nom_fichier, 'w') as f:
            f.write(reset_chaine)
        
        # 2 - map
        nom_fichier = "current_map.txt"
        reset_chaine = str('classic')
        with open(nom_fichier, 'w') as f:
            f.write(reset_chaine)
        
        # 3 - fruit
        nom_fichier = "current_fruit.txt"
        reset_chaine = str('pomme')
        with open(nom_fichier, 'w') as f:
            f.write(reset_chaine)
        
         # 4 - diff
        nom_fichier = "current_diff.txt"
        reset_chaine = str('aucun')
        with open(nom_fichier, 'w') as f:
            f.write(reset_chaine)
