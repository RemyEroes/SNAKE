import pygame
import sys
import random
from pygame.math import Vector2
import re


""" ---------------------------------------------------------- """


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        # les positions sont déterminées pas un certain nombre de fois la taille d'une cellule
        fruit_rect = pygame.Rect(
            int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)  # image de pomme
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
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        # for block in self.body:
        #     x_pos=int(block.x*cell_size)
        #     y_pos=int(block.y*cell_size)
        #     block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
        #     pygame.draw.rect(screen,(78,170,188),block_rect)

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

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset_snake(self):
        self.body = [Vector2(3, 7), Vector2(2, 7), Vector2(1, 7)]

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
        nb_obstacles = len(self.obstacles)

        for index in range(nb_obstacles):
            #print(index, "x: "+str(self.obstacles[index].x),"y: "+str(self.obstacles[index].y))
            obstacle_rect = pygame.Rect(int(self.obstacles[index].x*cell_size), int(
                self.obstacles[index].y*cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (199, 57, 48), obstacle_rect)

    def randomize(self, dif):  # creer un element a une position random
        nb_obstacles = self.get_nb_obstacles_from_difficulty(dif)
        # SI ON EST PAS EN MODE AUCUN OBSTACLE
        if (self.difficulty != 'aucun'):
            for i in range(int(nb_obstacles)):
                self.x = random.randint(1, cell_number-1)  # random x
                self.y = random.randint(1, cell_number-1)  # random y
                
                # pas en bas droite
                if (Vector2(self.x, self.y)!=Vector2(19,19) and Vector2(self.x, self.y)!=Vector2(19,18) and Vector2(self.x, self.y)!=Vector2(19,17) and Vector2(self.x, self.y)!=Vector2(18,19) and Vector2(self.x, self.y)!=Vector2(18,17) and Vector2(self.x, self.y)!=Vector2(17,17)):
                    self.pos = Vector2(self.x, self.y)
                    self.obstacles.append(self.pos)
                    i += 1
            

    def get_nb_obstacles_from_difficulty(self, dif):
        if (dif == 'aucun'):
            nb_obstacles = 0
        elif (dif == 'facile'):
            nb_obstacles = 2
        elif (dif == 'moyen'):
            nb_obstacles = 4
        elif (dif == 'difficile'):
            nb_obstacles = 6
        elif (dif == 'extreme'):
            nb_obstacles = 10
        return nb_obstacles


class MENU:
    def __init__(self):
        self.volume = 0.5
        self.difficulty = 'facile'
        self.map = 'classic'
        self.skin = 'bleu'
        self.fruit = 'pomme'

    def update(self):
        self.draw_elements_menu()

    def draw_elements_menu(self):
        self.draw_background_menu()
        self.draw_titre_menu()
        self.draw_high_score()
        self.draw_skin_selector()
        self.draw_snake_preview()
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

    def draw_snake_preview(self):
        localisation_skin = 'Graphics/skin/' + \
            str(self.skin)+'/preview/'+str(self.skin)+'.png'
        skin_actuel = pygame.image.load(
            localisation_skin).convert_alpha()  # image skin à utiliser
        # SKIN
        skin_actuel_rect = skin_actuel.get_rect(
            center=(cell_size*cell_number/2, cell_size*cell_number/2))

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


class GAMEOVER:
    def __init__(self):
        self.volume = .5
        self.difficulty = 'facile'
        self.skin = 'bleu'
        self.facondemourir = 'mur'

    # def draw_menu(self):
    #     #fond noir avec tete de mort

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

    def draw_background_menu(self):
        background_menu_color = (10, 10, 10)
        bg_menu_rect = pygame.Rect(
            0, 0, cell_size*cell_number, cell_number*cell_size)

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
        dead_text = str('Vous etes Mort')  # vous etes mort
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
        self.fruit = FRUIT()
        self.difficulty = 'difficile'
        self.obstacles = OBSTACLE(self.difficulty)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.obstacles.draw_obstacle() #obstacles

    def check_collision(self):
        # check si la tete touche le fruit
        if self.fruit.pos == self.snake.body[0]:
            # repositionner le fruit
            self.fruit.randomize()
            # ajouter un block au serpent
            self.snake.add_block()
            # jouer le son crunch
            self.snake.play_crunch_sound()

        # si le fruit apparait sur le corps du serpent
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        # si le serpent sort du jeu
        if not 0 <= self.snake.body[0].x < cell_number:  # gauche et droite
            self.game_over()
        if not 0 <= self.snake.body[0].y < cell_number:  # haut et bas
            self.game_over()

        # si le serpent se touche
        for block in self.snake.body[1:]:
            # si un block est identique à la tete du serpent c'ets qu'il s'est rentré dedans
            if block == self.snake.body[0]:
                self.game_over()
        
        # si le serpent touche une case obstacle
        nb_obstacles = len(main_game.obstacles.obstacles)
        for index in range(int(nb_obstacles)):
            if (self.snake.body[0].x == main_game.obstacles.obstacles[index].x and self.snake.body[0].y == main_game.obstacles.obstacles[index].y ) :
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
        # score
        # score en fonction de la taille du serpent (-3 du corps du début)
        score_text = str(len(self.snake.body)-3)
        score_surface = game_font.render(score_text, True, (0, 0, 0))
        score_x = int(cell_size*cell_number - 60)  # position x du score
        score_y = int(cell_size*cell_number - 40)  # position y du score
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)
        # fuit a coté
        apple_rect = apple.get_rect(
            midright=(score_rect.left, score_rect.centery))
        # background score
        # bg_rect =pygame.Rect(apple_rect.left,apple_rect.top-10,int(apple_rect.width+score_rect.width)+20,apple_rect.height+10)

        # RENDER
        # pygame.draw.rect(screen,(255,255,255),bg_rect)
        screen.blit(apple, apple_rect)
        screen.blit(score_surface, score_rect)

    def update_skin_from_file(self):
        fichier = open("current_skin.txt", "r")
        contenu = fichier.read()
        print(contenu)

        skin = contenu
        return skin


pygame.mixer.pre_init(44100, -16, 2, 512)  # preload le son
pygame.init()

cell_size = 40
cell_number = 20
screen = pygame.display.set_mode(
    (cell_number*cell_size, cell_number*cell_size))
clock = pygame.time.Clock()  # objet clock
apple = pygame.image.load(
    'Graphics/apple.png').convert_alpha()  # image de pomme
game_font = pygame.font.Font('Font/SuperMario256.ttf', 50)
game_font_small = pygame.font.Font('Font/SuperMario256.ttf', 30)
tete_de_mort = pygame.image.load(
    'Graphics/death-skull.png').convert_alpha()  # image tete de mort

grass = pygame.image.load(
    'Graphics/map/classic/classic.jpeg').convert_alpha()  # image grass

SCREEN_UPDATE = pygame.USEREVENT
# TIMER qui fait le screen update toutes les 150 ms
pygame.time.set_timer(SCREEN_UPDATE, 150)


menu_game = MENU()
main_game = MAIN()
game_over = GAMEOVER()


def play_game():
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
    while True:
        # zones cliquables
        zone_cliquable_play = pygame.rect.Rect(325, 665, 150, 60)
        zone_skin_plus = pygame.rect.Rect(235, 565, 50, 50)
        zone_skin_moins = pygame.rect.Rect(55, 565, 50, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # si on click sur la croix on quite le jeu
                pygame.quit()
                sys.exit()  # quite tous les sytemes restants
            if event.type == SCREEN_UPDATE:
                game_over.update()

            # Vérifier si l'utilisateur a cliqué sur le bouton play
            if event.type == pygame.MOUSEBUTTONUP and zone_cliquable_play.collidepoint(event.pos):
                play_game()

            # Vérifier si l'utilisateur a cliqué sur le bouton skin plus
            if event.type == pygame.MOUSEBUTTONUP and zone_skin_plus.collidepoint(event.pos):
                menu_game.change_skin_plus()

            # Vérifier si l'utilisateur a cliqué sur le bouton skin moins
            if event.type == pygame.MOUSEBUTTONUP and zone_skin_moins.collidepoint(event.pos):
                menu_game.change_skin_moins()

            # Vérifier si l'utilisateur a cliqué sur le bouton 'relancer' pendant le game over
            # if event.type == pygame.MOUSEBUTTONUP and zone_cliquable_relancer.collidepoint(event.pos):
                # play_game()

        menu_game.draw_elements_menu()
        pygame.display.update()
        clock.tick(60)  # framerate maximal du jeu


# LANCER LE MENU DE DÉPART
menu_du_jeu()
# ecran_game_over()
