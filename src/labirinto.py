import os
import random
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
        self.blocos = np.zeros((8, 8), dtype=object) # Tamanho do labirinto, quantidade de quadrados
        self.visitadosLabirinto = set()
        
        # Carregamento único das imagens, economizando CPU e processamento
        self.imagens_player = {
            "frente": pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "player", "railsao_frente.png")).convert_alpha(),
            "costas": pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "player", "railsao_costas.png")).convert_alpha(),
            "direita": pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "player", "railsao_direita.png")).convert_alpha(),
            "esquerda": pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "player", "railsao_esquerda.png")).convert_alpha()
        }

        self.sons_lab = {
            "bafo": pygame.mixer.Sound(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "bafoDeBosta.mp3"))
            #"brisa": pygame.mixer.Sound("pulo.wav")
        }

        # Geração do labirinto ao iniciar, serve para acessar os blocos apenas quando for necessário
        # gera apenas uma vez
        self.gerar_labirinto()

    # Adicionando novo parametro "direcao" para indicar para qual lado personagem está olhando
    # Modificação: player_xy -> player_x, player_y
    def desenhar(self, tela, player_x, player_y, direcao):

        # Alteração: Considerando tamanho da matriz para os laços de repetição
        for linha in range(self.blocos.__len__()):
            for coluna in range(self.blocos[0].__len__()):
                self.bloco = self.blocos[linha][coluna]
                
                # print("linha ", linha, " | coluna ", coluna)
                # print(self.blocos[linha][coluna],"\n")

                rect = self.bloco.criar(linha, coluna, tela)

                # Alterado para comparar Listas
                # variavel player_xy agora é uma lista :: A comparação continua sendo entre uma lista, podemos modifiar.
                if [linha, coluna] == [player_x, player_y]:
                    self.bloco.setVisible(True)
                    

                    # Redução do uso da memória, chama a imagem ja gerada que foi salva na memória
                    # ao invés de criar uma sempre
                    railsao = self.imagens_player[direcao]
                    
                    tela.blit(railsao, railsao.get_rect(
                                       center=rect.center))
                    
                    # Incrementar efeito sonoro aqui ou na movimentação
                    # Exemplo:
                    
                    if( 'Stench\n' in self.bloco.attributes and not (player_x, player_y) in self.visitadosLabirinto):
                        self.visitadosLabirinto.add((player_x, player_y))
                        som_pulo = self.sons_lab["bafo"]
                        som_pulo.play()

                    
    # Modificar a função "def gerar_labirinto(self, tamanho_labirinto)". "tamanho_labirinto" será um par ordernado (linha, coluna)
    # Tamanho padrão, aumentando a cada vitória ou definido pelo usuário.
    def gerar_labirinto(self):
        for linha in range(8):
            for coluna in range(8):
                # ParÂmetros de Bloco: 
                # 1 -> posicao_X  | 2 -> posicao_Y  | 3 -> visivel?
                # 4 -> tem buraco?  | 5 -> tem wumpus?  | 6 -> tem morcegos?  | 7 -> tem flecha?  | 8 -> tem ouro?
                if ( [linha, coluna] == [0, 1] ) or ( [linha, coluna] == [1, 0] ) or ( [linha, coluna] == [0, 0] ):
                    self.blocos[linha][coluna] = Bloco(linha, coluna, True, False, False, False, False, False)
                else:
                    self.blocos[linha][coluna] = Bloco(linha, coluna, False, False, False, False, False, False)

        #  Tornar qtd de morcegos maior que 1, a depender do tamanho do labirinto.
        qtd_buracos = (self.blocos.__len__() * self.blocos.__len__()) // 10
        qtd_wumpus = qtd_buracos + 1
        qtd_morcegos = qtd_wumpus + 1
        ind_arrow = qtd_morcegos + 1
        ind_gold = ind_arrow + 1

        backup_list = []

        # Os dados abaixo são configurados somente uma vez, por isto estão neste método
        for i in range(ind_gold):
            num_x = random.randint(0, 7)
            num_y = random.randint(0, 7)

            # Verificar caso em que números aleatórios iguais são gerados (bem raro, imagino)
            if (self.verificar_num_aleatorios(num_x, num_y, backup_list)):
                while (self.verificar_num_aleatorios(num_x, num_y, backup_list)):
                    num_x = random.randint(0, 7)
                    num_y = random.randint(0, 7)
                # É possível que o número gerado seja igual novamente
                # Ou caia em uma posição inicial: (0,0), (0,1), (1,0) ou (1,1)
                # Solução: utilizar o While
                backup_list.append([num_x, num_y])
            else:
                backup_list.append([num_x, num_y])
                #print(f"backup_list: {backup_list}")

            if (i == ind_arrow-1):
                self.blocos[num_x][num_y].reconfigurar(False, False, False, False, True, False)
            if (i == ind_gold-1):
                self.blocos[num_x][num_y].reconfigurar(False, False, False, False, False, True)
            if (i < qtd_buracos):
                self.blocos[num_x][num_y].reconfigurar(False, True, False, False, False, False)
                self.blocos[num_x][num_y].attributes = [] # Limpar atributos quando for buraco, morcego, ou wummpus
                self.conf_blocos_adjacentes(num_x, num_y, "Breeze\n")
            if (i == qtd_wumpus-1):
                self.blocos[num_x][num_y].reconfigurar(False, False, True, False, False, False)
                self.blocos[num_x][num_y].attributes = [] # Limpar atributos quando for buraco, morcego, ou wummpus
                self.conf_blocos_adjacentes(num_x, num_y, "Stench\n")
            if (i == qtd_morcegos-1):
                self.blocos[num_x][num_y].reconfigurar(False, False, False, True, False, False)
                self.blocos[num_x][num_y].attributes = [] # Limpar atributos quando for buraco, morcego, ou wummpus
                self.conf_blocos_adjacentes(num_x, num_y, "Flapping")
            

            #print(f"{i} - número x: {num_x}")
            #print(f"{i} - número y: {num_y}")

    # Verificar se os números aleatórios gerados são iguais, caso sejam, 
    # gerar novos números. Utiliza recursão, mas acredito que será bem raro de acontecer.
    def verificar_num_aleatorios(self, num_x, num_y, backup_list):
        aux = False
        if (num_x == 0 or num_x == 1) and (num_y == 0 or num_y == 1):
            aux = True
        elif [num_x, num_y] in backup_list:
            aux = True
        return aux

    # Método para configurar os blocos adjacentes a um bloco com buraco ou wumpus, 
    # adicionando os atributos "Breeze" e "Stench", respectivamente
    def conf_blocos_adjacentes(self, linha, coluna, attribute):

        if linha > 0:
            self.bloco = self.blocos[linha - 1][coluna] # Baixo
            if not (self.verificar_bloco(self.bloco, attribute)):
                self.bloco.attributes.append(attribute)
        if linha < 7:
            self.bloco = self.blocos[linha + 1][coluna] # Cima
            if not (self.verificar_bloco(self.bloco, attribute)):
                self.bloco.attributes.append(attribute)
        if coluna > 0:
            self.bloco = self.blocos[linha][coluna - 1]  # Esquerda
            if not (self.verificar_bloco(self.bloco, attribute)):
                self.bloco.attributes.append(attribute)
        if coluna < 7:
            self.bloco = self.blocos[linha][coluna + 1]  # Direita
            if not (self.verificar_bloco(self.bloco, attribute)):
                self.bloco.attributes.append(attribute)

    # Método para verificar se o bloco adjacente tem um Buraco, Wumpus ou Morcego
    # Ou se já possui o atributo que será escrito.
    # Se tiver, não escreverá nenhum dos atributos "Breeze", "Stench" ou "Flapping"
    def verificar_bloco(self, bloco, attribute):
        aux = False
        if bloco.hasPit or bloco.hasWumpus or bloco.hasBats:
            aux = True
        elif attribute in bloco.attributes:
            aux = True
        return aux

            
        
