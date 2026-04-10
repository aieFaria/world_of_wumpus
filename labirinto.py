import os

import numpy as np
import pygame
from cons import RECT_COLOR, SQUARE_LENGTH
from bloco import Bloco

class Labirinto:

    def __init__(self):
        self.board = np.zeros((8, 8))
        self.cores = [pygame.Color(RECT_COLOR), pygame.Color("gray")]
        self.tamanho_quadrado = SQUARE_LENGTH
        # self.blocos = [[None for _ in range(8)] for _ in range(8)]

    def desenhar(self, tela, player_xy):
        # self.blocos = [[None for _ in range(8)] for _ in range(8)]
        self.blocos = np.zeros((8, 8), dtype=object)
        for linha in range(8):
            for coluna in range(8):
                self.bloco = Bloco(linha, coluna, True, (linha, coluna))
                self.blocos[linha][coluna] = self.bloco
                # if (player_xy == (0, 0)):
                # if (linha >= 0 and linha <= 7) and (coluna >= 0 and coluna <= 7):
                #     self.bloco = Bloco(0, 1, True, (0, 1))
                #     self.bloco = Bloco(1, 0, True, (1, 0))
                #     print(coluna)
                #     self.blocos[linha][coluna] = self.bloco
                # else:
                #     self.bloco = Bloco(linha, coluna, False, (linha, coluna))
                    # 40 blocos.
                    # self.blocos.append(self.bloco)
                
                print(self.blocos.__len__())
                print(self.blocos[linha][coluna])

                # rect = pygame.draw.rect(
                #     tela, 
                #     cor,
                #     (coluna * (self.tamanho_quadrado), linha * (self.tamanho_quadrado), self.tamanho_quadrado, self.tamanho_quadrado)
                # )

                rect = self.bloco.criar(linha, coluna, tela)

                if (linha, coluna) == player_xy:
                    self.bloco = Bloco(linha, coluna, True, (linha, coluna))
                    railsao = pygame.image.load(os.path.join("world_of_wumpus\\resources","railsao.png")).convert_alpha()
                    tela.blit(railsao, rect)

                
    
        

