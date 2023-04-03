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

class TIMER:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        # Initialise la bibliothèque Pygame pour la gestion des polices d'écriture
        pygame.font.init()

        # Initialise la police d'écriture pour le texte du timer
        self.font = pygame.font.Font('Font/SuperMario256.ttf', 30)

    def draw_timer(self):
        # Mesure le temps écoulé depuis le début de la partie
        elapsed_time = pygame.time.get_ticks() - self.start_time

        # Convertit le temps en minutes et secondes
        elapsed_minutes = elapsed_time // 60000
        elapsed_seconds = (elapsed_time // 1000) % 60

        # Formatte le temps en une chaîne de caractères au format "mm:ss"
        time_text = self.font.render("{:02d}:{:02d}".format(elapsed_minutes, elapsed_seconds), True, (255, 255, 255))
        screen.blit(time_text, (700, 700))
        
        def get_start_time(self):
            return self.start_time