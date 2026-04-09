import os

import numpy as np
import pygame
from cons import RECT_COLOR, SQUARE_LENGTH

class Labirinto:

    def __init__(self):
        self.board = np.zeros((8, 8))
        self.cores = [pygame.Color(RECT_COLOR), pygame.Color("gray")]
        self.tamanho_quadrado = SQUARE_LENGTH

    def desenhar(self, tela, player_xy):
        for linha in range(8):
            for coluna in range(8):
                cor = self.cores[(linha + coluna) % 2]
                
                rect = pygame.draw.rect(
                    tela, 
                    cor,
                    (coluna * (self.tamanho_quadrado), linha * (self.tamanho_quadrado), self.tamanho_quadrado, self.tamanho_quadrado)
                )

                if (linha, coluna) == player_xy:
                    cor = pygame.Color("red")
                    railsao = pygame.image.load(os.path.join("world_of_wumpus\\resources","railsao.png")).convert_alpha()
                    tela.blit(railsao, rect)
    
        

