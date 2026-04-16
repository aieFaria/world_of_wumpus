import os, random, pygame
import numpy as np

from cons import *
from bloco import Bloco

class Labirinto:

    def __init__(self, tamanho_lab=None):
        self.tamanho_lab = tamanho_lab # or TAMANHO_LAB # cons.TAMANHO_LAB
        self.board = np.zeros((tamanho_lab, tamanho_lab))
        self.cores = [pygame.Color(RECT_COLOR), pygame.Color("gray")]
        # TAMANHO_QUADRADO não está sendo dividido em cons.py, possui mesmo tamanho que ALTURA_TELA
        self.tamanho_quadrado = TAMANHO_QUADRADO // tamanho_lab
        self.blocos = np.zeros((tamanho_lab, tamanho_lab), dtype=object) # Tamanho do labirinto, quantidade de quadrados
        self.visitadosLabirinto = set()
        self.vis = (-1, -1) # Variavel de controle para saber se acabou de pisar no bloco
        self.pontuacao = 0
        self.hasArrow = False # Indica se o jogador possui a flecha
        self.qtd_flechas = 0 
        self.olhandoWumpus = [] # array de tupla que contém as possibilidades de olhar para wumpus
        # Definição das quantidades de cada coisa no mapa: Configuração padrão Labirinto 6x6
        self.dic_quantidades = {"morcegos": 2, "ouro": 3, "wumpus": 2, "flecha": 2, "buracos": 4 }

        self.esperando_morcego = False
        self.tempo_morcego = 0
        self.pos_morcego = (0, 0)
        
        # Carregamento único das imagens, economizando CPU e processamento
        self.imagens_player = {
            "frente": pygame.image.load(os.path.join(DIR_PATH, "player", "railsao_frente_p.png")).convert_alpha(),
            "costas": pygame.image.load(os.path.join(DIR_PATH, "player", "railsao_costas.png")).convert_alpha(),
            "direita": pygame.image.load(os.path.join(DIR_PATH, "player", "railsao_direita.png")).convert_alpha(),
            "esquerda": pygame.image.load(os.path.join(DIR_PATH, "player", "railsao_esquerda.png")).convert_alpha()
        }

        self.sons_lab = {
            "bafo": pygame.mixer.Sound(os.path.join(DIR_PATH, "sounds", "bafoDeBosta.mp3")),
            "brisa": pygame.mixer.Sound(os.path.join(DIR_PATH, "sounds", "brisa.mp3"))
        }

        # Geração do labirinto ao iniciar, serve para acessar os blocos apenas quando for necessário
        # gera apenas uma vez
        self.gerar_labirinto()

    # Adicionando novo parametro "direcao" para indicar para qual lado personagem está olhando
    # Modificação: player_xy -> player_x, player_y
    def desenhar(self, tela, player_x, player_y, direcao, acao, offset_y, largura_janela, altura_janela):

        

        linhas, colunas = self.blocos.shape
        
        tamanho_original = 87 # Define o tamanho original para adequação a redução de escala
        
        largura_virtual = colunas * tamanho_original
        altura_virtual = linhas * tamanho_original
        
        # Cria uma tela virtual com o tamanho perfeito original
        tela_virtual = pygame.Surface((largura_virtual, altura_virtual))
        tela_virtual.fill(PRINCIPAL_COLOR)

        # Lógica de espera do Gemini
        if self.esperando_morcego:
            # 1000 = 1 segundo de espera. Se quiser mais rápido/lento, altere este valor!
            if pygame.time.get_ticks() - self.tempo_morcego >= 1000: 
                player_x, player_y = 0, 0
                self.vis = (-1, -1)
                self.esperando_morcego = False
            else:
                # Prende o jogador na posição atual do morcego enquanto o tempo passa
                player_x, player_y = self.pos_morcego

        mudou_de_bloco = False
        if (player_x, player_y) != self.vis:
            # Para todos os sons
            self.sons_lab["bafo"].stop()
            self.sons_lab["brisa"].stop()
            
            # Atualiza a visita e marca a flag para tocar som neste frame
            self.vis = (player_x, player_y)
            mudou_de_bloco = True

        # Alteração: Considerando tamanho da matriz para os laços de repetição
        for linha in range(self.blocos.__len__()):
            for coluna in range(self.blocos[0].__len__()):
                bloco = self.blocos[linha][coluna]
                
                bloco.tamanho_quadrado = tamanho_original
                # print("linha ", linha, " | coluna ", coluna)
                # print(self.blocos[linha][coluna],"\n")

                if [linha, coluna] == [player_x, player_y]:
                    bloco.setVisible(True)
                        
                    if( self.hasArrow and acao):
                        # Executar disparo da flecha com base na direção
                        # print("acao: ", self.qtd_flechas)
                        self.qtd_flechas -= 1
                        if self.qtd_flechas == 0:
                            self.hasArrow = False
                        #print(self.olhandoWumpus)
                        if( self.olhando_para_Wumpus(player_x, player_y, direcao) ): #Verifica se está virado para o Wumpus
                            # Se for modificar para indicar que wumpus está morto faça aqui dentro
                            self.pontuacao += 1000

                    # Condicional para verificar se acabei de pisar no bloco
                    # Será verdadeiro por uma única iteração e as demais seram falsas
                    # ou seja, o som dará "play" apenas uma vez
                    if mudou_de_bloco:
                        if 'Stench\n' in bloco.attributes:
                            self.sons_lab["bafo"].play() # Toca apenas uma vez
                        if 'Breeze\n' in bloco.attributes:
                            # A flag "loops=-1" indica que o som será tocado indefinidamente até que o 
                            # método "stop()" seja chamado
                            self.sons_lab["brisa"].play(loops=-1)

                        # Lógica de espera do Gemini
                        if bloco.hasBats and not self.esperando_morcego:
                            print("Swoosh! Os morcegos te levaram!")
                            self.esperando_morcego = True
                            self.tempo_morcego = pygame.time.get_ticks()
                            self.pos_morcego = (player_x, player_y)
                            

                # Cria o bloco na tela virtual
                rect = bloco.criar(linha, coluna, tela_virtual)

                # Alterado para comparar Listas
                # variavel player_xy agora é uma lista :: A comparação continua sendo entre uma lista, podemos modifiar.
                if [linha, coluna] == [player_x, player_y]:
                                       
                    # Redução do uso da memória, chama a imagem ja gerada que foi salva na memória
                    # ao invés de criar uma sempre
                    #railsao = self.imagens_player[direcao]
                    railsao = self.imagens_player[direcao]
                    
                    tela_virtual.blit(railsao, railsao.get_rect(center=rect.center))
                    
                    # Condicionais para definição da pontuação
                    if ( bloco.hasWumpus and not (player_x, player_y) in self.visitadosLabirinto ):
                        self.visitadosLabirinto.add((player_x, player_y))
                        self.pontuacao -= 1000
                        # Adicionar efeito sonoro, se houver, bem aqui!
                    
                    # Coleta automatica do ouro
                    if ( bloco.hasGold and not (player_x, player_y) in self.visitadosLabirinto):
                        self.visitadosLabirinto.add((player_x, player_y))
                        self.pontuacao += 1000
                        # Adicionar efeito sonoro, se houver, bem aqui!
                    
                    # Coleta automatica da flecha
                    if ( bloco.hasArrow and not (player_x, player_y) in self.visitadosLabirinto ):
                        self.visitadosLabirinto.add((player_x, player_y))
                        self.qtd_flechas += 1 # Soma 1 na mochila do jogador
                        # print("flechas: ", self.qtd_flechas)
                        self.hasArrow = True # Indica que o jogador tem flecha
                        #bloco.hasArrow = False
                        # Adicionar efeito sonoro, se houver, bem aqui!

                    if ( bloco.hasBats and mudou_de_bloco ):
                        
                        # Sortear nova posição após oisar em morcegos
                        player_x = 0
                        player_y = 0
                        # print("teleport")

        pygame.draw.rect(tela_virtual, (0, 0, 0), tela_virtual.get_rect(), 6)

        area_util_h = altura_janela - offset_y
        area_util_w = largura_janela
        
        tamanho_escala_w = max(1, area_util_w - 5)
        tamanho_escala_h = max(1, area_util_h - 5)
        
        escala = min(tamanho_escala_w / largura_virtual, tamanho_escala_h / altura_virtual)
        nova_largura = int(largura_virtual * escala)
        nova_altura = int(altura_virtual * escala)
        
        labirinto_comprimido = pygame.transform.smoothscale(tela_virtual, (nova_largura, nova_altura))
        
        inicio_x = (largura_janela - nova_largura) // 2
        inicio_y = offset_y + (area_util_h - nova_altura) // 2
        
        tela.blit(labirinto_comprimido, (inicio_x, inicio_y))

        return player_x, player_y # Retorna posição em caso de alteração pelos morcegos

                    
    # Modificar a função "def gerar_labirinto(self, tamanho_labirinto)". "tamanho_labirinto" será um par ordernado (linha, coluna)
    # Tamanho padrão, aumentando a cada vitória ou definido pelo usuário.
    def gerar_labirinto(self):
        for linha in range(self.tamanho_lab):
            for coluna in range(self.tamanho_lab):
                # ParÂmetros de Bloco: 
                # 1 -> posicao_X  | 2 -> posicao_Y  | 3 -> visivel?
                # 4 -> tem buraco?  | 5 -> tem wumpus?  | 6 -> tem morcegos?  | 7 -> tem flecha?  | 8 -> tem ouro?
                if ( [linha, coluna] == [0, 1] ) or ( [linha, coluna] == [1, 0] ) or ( [linha, coluna] == [0, 0] ):
                    
                    self.blocos[linha][coluna] = Bloco(linha, coluna, True, False, False, False, False, False)

                    if( [linha, coluna] == [0, 0] ): self.blocos[linha][coluna].caracteristica["casa"]
                else:
                    self.blocos[linha][coluna] = Bloco(linha, coluna, False, False, False, False, False, False)

        #  Tornar qtd de morcegos maior que 1, a depender do tamanho do labirinto.
        # limite_buracos = (self.blocos.__len__() * self.blocos.__len__()) // 10
        # limite_wumpus = limite_buracos + 1
        # limite_morcegos = limite_wumpus + 1
        # limite_arrow = limite_morcegos + 1
        # limite_gold = limite_arrow + 1


        limite_buracos = self.dic_quantidades["buracos"]
        limite_wumpus = limite_buracos + self.dic_quantidades["wumpus"]
        limite_morcegos = limite_wumpus + self.dic_quantidades["morcegos"]
        limite_arrow = limite_morcegos + self.dic_quantidades["flecha"]
        limite_gold = limite_arrow + self.dic_quantidades["ouro"]

        backup_list = []

        # Os dados abaixo são configurados somente uma vez, por isto estão neste método
        for i in range(limite_gold):
            num_x = random.randint(0, self.tamanho_lab-1)
            num_y = random.randint(0, self.tamanho_lab-1)

            # Verificar caso em que números aleatórios iguais são gerados (bem raro, imagino)
            if (self.verificar_num_aleatorios(num_x, num_y, backup_list)):
                while (self.verificar_num_aleatorios(num_x, num_y, backup_list)):
                    num_x = random.randint(0, self.tamanho_lab-1)
                    num_y = random.randint(0, self.tamanho_lab-1)
                # É possível que o número gerado seja igual novamente
                # Ou caia em uma posição inicial: (0,0), (0,1), (1,0) ou (1,1)
                # Solução: utilizar o While
                backup_list.append([num_x, num_y])
            else:
                backup_list.append([num_x, num_y])
                #print(f"backup_list: {backup_list}")
            if (i < limite_buracos):
                self.blocos[num_x][num_y].reconfigurar(False, True, False, False, False, False)
                self.blocos[num_x][num_y].attributes = [] # Limpar atributos quando for buraco, morcego, ou wumpus
                self.conf_blocos_adjacentes(num_x, num_y, "Breeze\n")
            elif (i < limite_wumpus):
                self.blocos[num_x][num_y].reconfigurar(False, False, True, False, False, False)
                self.blocos[num_x][num_y].attributes = [] # Limpar atributos quando for buraco, morcego, ou wumpus
                self.conf_blocos_adjacentes(num_x, num_y, "Stench\n")
            elif (i < limite_morcegos):
                self.blocos[num_x][num_y].reconfigurar(False, False, False, True, False, False)
                self.blocos[num_x][num_y].attributes = [] # Limpar atributos quando for buraco, morcego, ou wumpus
                self.conf_blocos_adjacentes(num_x, num_y, "Flapping")
            elif (i < limite_arrow):
                self.blocos[num_x][num_y].reconfigurar(False, False, False, False, True, False)
            elif (i < limite_gold):
                self.blocos[num_x][num_y].reconfigurar(False, False, False, False, False, True)
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
                if (attribute == "Stench\n"): self.olhandoWumpus.append((linha-1, coluna, "frente"))
        if linha < self.tamanho_lab-1:
            self.bloco = self.blocos[linha + 1][coluna] # Cima
            if not (self.verificar_bloco(self.bloco, attribute)):
                self.bloco.attributes.append(attribute)
                if (attribute == "Stench\n"): self.olhandoWumpus.append((linha+1, coluna, "costas"))
        if coluna > 0:
            self.bloco = self.blocos[linha][coluna - 1]  # Esquerda
            if not (self.verificar_bloco(self.bloco, attribute)):
                self.bloco.attributes.append(attribute)
                if (attribute == "Stench\n"): self.olhandoWumpus.append((linha, coluna-1, "direita"))
        if coluna < self.tamanho_lab-1:
            self.bloco = self.blocos[linha][coluna + 1]  # Direita
            if not (self.verificar_bloco(self.bloco, attribute)):
                self.bloco.attributes.append(attribute)
                if (attribute == "Stench\n"): self.olhandoWumpus.append((linha, coluna+1, "esquerda"))

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

    def olhando_para_Wumpus(self, x, y, direcao):
        if( (x, y, direcao) in self.olhandoWumpus ):
            return True
        return False
            
        
