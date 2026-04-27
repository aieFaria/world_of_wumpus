import time
import pygame
from labirinto import Labirinto
from collections import deque

class Agente:
    # Atributos de classe
    delayMove = 500

    def __init__(self, id):
        # Atributo de instância do agente
        self.id = id
        self.ultimo_move_time = pygame.time.get_ticks()
        self.finalizado = False
        self.perigosos = set() # Indica quais os locais com certeza agente não deve passar
        self.fila = deque() # pygame.K_RIGHT, pygame.K_LEFT
        self.pilha_caminho = [] # Consumida da direta para esquerda, pilha
        # self.contador_passos = {"atual": (-2, -2), "cont": 0, "antigo":(-1, -1), "contAntigo": -1}
        self.atual = None
        self.anterior = None
        self.tentou_movimento = False
        self.cont_bloqueio = 0

        self.historico = [] # Inicializa vazio

        self.labirinto = [] # Matriz flexivel para memória

        self.ctrl = {"direcao": "frente", "localizacao": (0, 0)}

        self.leituraLab = {} # Referente ao retorno do labirinto quando agente está ativo

    def executar(self):

        tempo_atual = pygame.time.get_ticks()

        if (not self.leituraLab):
            self.iniciar()

        pos_vinda_lab = self.leituraLab.get("bloco")

        if (self.atual is None):
            self.atual = pos_vinda_lab
            self.anterior = pos_vinda_lab
            
        self.tell( self.aux_convertDictBloco(self.leituraLab) )

        # print(self.labirinto)
        
        if ( self.leituraLab and not self.finalizado ):

            if (not self.pilha_caminho):
                # Tentativa de mitigar atrasos no pensamento
                self.ask()

            if tempo_atual - self.ultimo_move_time > self.delayMove:

                self.anterior = self.atual
                self.atual = pos_vinda_lab
                x, y = self.ctrl.get("localizacao")

                if (self.pilha_caminho):
                    destino = self.pilha_caminho[-1] # Lendo último valor da pilha para não precisar colocar novamente

                    if ((x, y) != destino):

                        if self.tentou_movimento and not self.mudando():
                            # Aqui! Indica que o agente encontrou parede
                            # Verificar como proceder
                            # Talvez salvar o tamanho do labirinto aqui para o agente saber
                            self.cont_bloqueio += 1
                            if self.cont_bloqueio >= 2:
                                # print(f"BLOQUEIO REAL: Removendo destino {destino} após 2 tentativas.")
                                self.pilha_caminho.pop()
                                self.cont_bloqueio = 0
                                self.tentou_movimento = False
                            else:
                                # Tenta novamente (pode ser o segundo passo após virar)
                                self.movimentacao_segura(x, y, destino)
                        else:
                            # Se moveu ou é o primeiro passo, reseta contador e move
                            self.cont_bloqueio = 0
                            self.movimentacao_segura(x, y, destino)
                            self.tentou_movimento = True  # Define como verdadeiro para indicar que foi tentado novo movimento

                    else:
                        self.cont_bloqueio = 0
                        self.pilha_caminho.pop()
                        self.tentou_movimento = False

                else:
                    # pensar para atribuir valores a pilha_caminho
                    # chamada da função ask aqui:
                    # self.ask()
                    print(self.pilha_caminho)
                    

                self.ultimo_move_time = tempo_atual
            
            print("Leitura: ", self.leituraLab)

    def mudando(self):
        print(f"Atual: {self.atual} | Anterior: {self.anterior}")
        return self.atual != self.anterior

    """
    Método ask, deve retornar a posição destino ou a sequencia de 'key' que leva ao destino
    mudar nome para "pensoLogoExisto" ao final
    """
    def ask(self):

        if ( self.ctrl["localizacao"] == (0, 0) ):
            
            self.pilha_caminho.append( (1, 2) )
            # self.pilha_caminho.append( (1, 1) )

        if (True):
            pass

    
    def iniciar(self):
        # Disposição inicial segura
        bloco = BlocoI((0, 0), [], False, "", False, False, False, "O")
        bloco1 = BlocoI((0, 1), [], False, "", False, False, False, "O")
        bloco2 = BlocoI((1, 0), [], False, "", False, False, False, "O")

        self.tell(bloco)
        self.tell(bloco1)
        self.tell(bloco2)

        # Testes da função tell
        # self.tell( BlocoI((2, 0), [], False, "", False, False, False, "O") )
        # self.tell( BlocoI((5, 5), [], False, "", False, False, False, "O") ) # Teleport linha e coluna diferente
        # # self.tell( BlocoI((0, 5), [], False, "", False, False, False, "O") ) # Teleport mesma coluna
        # # self.tell( BlocoI((5, 0), [], False, "", False, False, False, "O") ) # Teleport mesma linha
        # self.tell( BlocoI((2, 2), [], False, "", False, False, False, "O") )
        
    def tell(self, blocoPercebido): # Talvez uma variavel t para controle do tempo

        pos = self.leituraLab.get('bloco')
        if pos:
            self.ctrl["localizacao"] = pos

        x, y = blocoPercebido.posicao

        # Condicional para adicionar o bloco percebido ao labirinto interno
        # Leva em consideração que não haverá teleport -> Corrigir por conta do morcego
        contem = any(blocoPercebido in linha for linha in self.labirinto)
        if( not contem ):

            while len(self.labirinto) <= x:
                # Adiciona uma nova linha vazia
                self.labirinto.append([])
            
            for i in range(len(self.labirinto)):
                while len(self.labirinto[i]) <= y:
                    i = i
                    j = len(self.labirinto[i])
                    
                    if i == x and j == y:
                        self.labirinto[i].append( blocoPercebido )
                    else:
                        self.labirinto[i].append(
                            BlocoI((i, j), [], False, "", False, False, False)
                        )
            
        else:
            # Substitui o bloco caso já exista
            self.labirinto[x][y] = blocoPercebido

    def movimentacao_segura(self, x, y, bloco_alvo):
        target_x, target_y = bloco_alvo
        direcoes = [
            (x + 1, y, pygame.K_DOWN), (x - 1, y, pygame.K_UP),  
            (x, y + 1, pygame.K_RIGHT), (x, y - 1, pygame.K_LEFT)
        ]

        acao = None

        for vx, vy, direcao in direcoes:
            if 0 <= vx < bloco_alvo[0] and vy > 0:
                acao = pygame.K_DOWN
                
            if bloco_alvo[0] < vx and x != bloco_alvo[0]:
                acao = pygame.K_UP

            if 0 <= vy < bloco_alvo[1] and vx > 0:
                acao = pygame.K_RIGHT

            if bloco_alvo[1] < vy and y != bloco_alvo[1]:
                acao = pygame.K_LEFT

        #         # if( not self.foi_visitado(vx, vy) ):
        #             # self.pilha_caminho.append((x, y))

        if acao:
            self.movimentar(acao)


    def movimentar(self, tecla):

        if (tecla == pygame.K_DOWN):
            self.ctrl["direcao"] == "frente"
        elif (tecla == pygame.K_UP):
            self.ctrl["direcao"] == "costa"
        elif (tecla == pygame.K_RIGHT):
            self.ctrl["direcao"] == "direita"
        if (tecla == pygame.K_LEFT):
            self.ctrl["direcao"] == "esquerda"

        evento = pygame.event.Event(pygame.KEYDOWN, {
            'key': tecla,
            'mod': 0,
            'is_agent': True # Flag para identificar que o agente que moveu
        })

        pygame.event.post(evento)
        # return evento
        
    def base_conhecimento(self, atributos):
        for atr in atributos:
            if (atr == "Breeze"):
                pass

    def aux_convertDictBloco(self, dict):
        return BlocoI((dict.get('bloco', [0, 0])), 
                      dict.get('atributos', []),
                      dict.get('hasPit'),
                      dict.get('hasWumpus'),
                      dict.get('hasBats'),
                      dict.get('hasArrow'),
                      dict.get('hasGold'),
                      "O")

    

# Objeto interno para uso do agente
class BlocoI: 
    def __init__(self, posicao, atributos, hasPit, hasWumpus, hasBats, hasArrow, hasGold, ava="?"):
        self.posicao = posicao
        self.atributos = atributos
        self.hasPit = hasPit
        self.hasWumpus = hasWumpus
        self.hasBats = hasBats
        self.hasArrow = hasArrow
        self.hasGold = hasGold

        # Atributos para uso e classificação do agente:
        self.perigo = ava # Use: "O" - Seguro | "?" - Dúvida | "X" - Perigosissimo | "P" - Parede

    def __str__(self):
        return f"{self.posicao}.{self.perigo}\n         Atributos: {self.atributos}"
    
    __repr__ = __str__
    
    # Equivalente do equals do java
    def __eq__(self, other):
        if isinstance(other, BlocoI):
            return self.posicao == other.posicao
        return False
    
    def setPerigo(self, perigo):
        self.perigo = perigo

        