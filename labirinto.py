import os
import platform

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
        self.blocos = np.zeros((8, 8), dtype=object) # Tamanho do labirinto, quantidade de quadrados
        
        # Carregamento único das imagens, economizando CPU e processamento
        self.imagens_player = {
            "frente": pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "" "resources", "railsao_frente.png")).convert_alpha(),
            "costas": pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "railsao_costas.png")).convert_alpha(),
            "direita": pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "railsao_direita.png")).convert_alpha(),
            "esquerda": pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "railsao_esquerda.png")).convert_alpha()
        }

        # Geração do labirinto ao iniciar, serve para acessar os blocos apenas quando for necessário
        # gera apenas uma vez
        self.gerar_labirinto()

    # Adicionando novo parametro "direcao" para indicar para qual lado personagem está olhando
    def desenhar(self, tela, player_xy, direcao):
        # self.blocos = [[None for _ in range(8)] for _ in range(8)]
        # self.blocos = np.zeros((8, 8), dtype=object)

        # Alteração: Considerando tamanho da matriz para os laços de repetição
        for linha in range(self.blocos.__len__()):
            for coluna in range(self.blocos[0].__len__()):
                #self.bloco = Bloco(linha, coluna, True, (linha, coluna))
                self.bloco = self.blocos[linha][coluna]
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
                
                print(self.blocos.__len__()) ; print("linha ", linha, " | coluna ", coluna)
                print(self.blocos[linha][coluna],"\n")

                # rect = pygame.draw.rect(
                #     tela, 
                #     cor,
                #     (coluna * (self.tamanho_quadrado), linha * (self.tamanho_quadrado), self.tamanho_quadrado, self.tamanho_quadrado)
                # )

                rect = self.bloco.criar(linha, coluna, tela)

                # Alterado para comparar Listas
                # variavel player_xy agora é uma lista
                if [linha, coluna] == player_xy:
                    #self.bloco = Bloco(linha, coluna, True, (linha, coluna)) -> Não é mais necessário
                    self.bloco.setVisible(True)

                    # Redução do uso da memória, chama a imagem ja gerada que foi salva na memória
                    # ao invés de criar uma sempre
                    railsao = self.imagens_player[direcao]
                
                    # Criando forma de centralização da imagem no bloco
                    tela.blit(railsao, railsao.get_rect(
                                       center=self.bloco.criar(linha, coluna, tela).center))
    
    def gerar_labirinto(self):
        for linha in range(8):
            for coluna in range(8):
                self.blocos[linha][coluna] = Bloco(linha, coluna, False, (linha, coluna))
                
    
        

