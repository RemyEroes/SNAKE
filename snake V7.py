import pygame
import sys
import random
from pygame.math import Vector2
import re


""" ---------------------------------------------------------- """
class TIMMER:
    def init(self):
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        # Initialise la bibliothèque Pygame pour la gestion des polices d'écriture
        pygame.font.init()

        # Initialise la police d'écriture pour le texte du timer
        self.font = pygame.font.Font(None, 36)

    def draw_timer(self):
        # Mesure le temps écoulé depuis le début de la partie
        elapsed_time = pygame.time.get_ticks() - self.start_time

        # Convertit le temps en minutes et secondes
        elapsed_minutes = elapsed_time // 60000
        elapsed_seconds = (elapsed_time // 1000) % 60

        # Formatte le temps en une chaîne de caractères au format "mm:ss"
        time_text = self.font.render("Temps écoulé : {:02d}:{:02d}".format(elapsed_minutes, elapsed_seconds), True, (0, 0, 0))
        screen.blit(time_text, (10, 10))


    def get_start_time(self):
        return self.start_time

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
        

    
    # def update_skin_from_file(self):
    #     fichier = open("current_skin.txt", "r")
    #     contenu = fichier.read()
    #     print(contenu)

    #     skin=contenu
    #     self.skin=str(skin)
    #     print('le skin est:'+str(self.skin))
    #     print('le contenu est:'+contenu)


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


    
class MAIN:
    # creation du fruit et du serpent
    def __init__(self):
        self.snake = SNAKE(self.update_skin_from_file())
        self.fruit = FRUIT(self.update_fruit_from_file())
        self.difficulty = self.update_diff_from_file() #----------------------------------------------------------------------------------- DIFFICULTÉ DU JEU
        ## ON DEFINIT QUELLE DIFFOCULTE ON UTILISE
        #if self.difficulty == 'obstacle-1' or self.difficulty == 'obstacle-2' or self.difficulty == 'extreme':
        self.obstacles = OBSTACLE(self.difficulty)
        
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
timmer = TIMMER()



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
