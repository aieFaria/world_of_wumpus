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
        self.ultimo_move_time = 0
        self.finalizado = False
        self.perigosos = set() # Indica quais os locais com certeza agente não deve passar
        self.fila = deque() # pygame.K_RIGHT, pygame.K_LEFT
        self.pilha_caminho = [] # Consumida da direta para esquerda, pilha

        self.historico = [] # Inicializa vazio

        self.labirinto = [] # Matriz flexivel para memória

        self.ctrl = {"direcao": "frente", "localizacao": (0, 0)}

        self.leituraLab = {} # Referente ao retorno do labirinto quando agente está ativo

    def executar(self):

        tempo_atual = pygame.time.get_ticks()

        if (not self.leituraLab):
            self.iniciar()
            
        self.tell( self.aux_convertDictBloco(self.leituraLab) )

        # print(self.labirinto)
        
        if ( self.leituraLab and not self.finalizado ):
            if tempo_atual - self.ultimo_move_time > self.delayMove:

                x, y = self.leituraLab.get("bloco")

                if (self.pilha_caminho):
                    destino = self.pilha_caminho.pop()

                    if ((x, y) != destino):
                        self.movimentacao_segura(x, y, destino)
                        self.pilha_caminho.append(destino)
                else:
                    # pensar para atribuir valores a pilha_caminho
                    # chamada da função ask aqui:
                    # self.ask()
                    pass

                self.ultimo_move_time = tempo_atual

    """
    Método ask, deve retornar a posição destino ou a sequencia de 'key' que leva ao destino
    mudar nome para "pensoLogoExisto" ao final
    """
    def ask(self):
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
        direcoes = [
            (x + 1, y, pygame.K_DOWN), (x - 1, y, pygame.K_UP),  
            (x, y + 1, pygame.K_RIGHT), (x, y - 1, pygame.K_LEFT)
        ]

        for vx, vy, direcao in direcoes:
            if 0 <= vx < bloco_alvo[0]:
                self.movimentar(pygame.K_DOWN)
                
            if bloco_alvo[0] < vx:
                self.movimentar(pygame.K_UP)

            if 0 <= vy < bloco_alvo[1]:
                self.movimentar(pygame.K_RIGHT)

            if bloco_alvo[1] < vy:
                self.movimentar(pygame.K_LEFT)

                # if( not self.foi_visitado(vx, vy) ):
                    # self.pilha_caminho.append((x, y))

    def movimentar(self, tecla):
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
        return BlocoI((dict.get('bloco', [-1, -1])), 
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
        return f"{self.posicao}.{self.perigo}"
    
    __repr__ = __str__
    
    # Equivalente do equals do java
    def __eq__(self, other):
        if isinstance(other, BlocoI):
            return self.posicao == other.posicao
        return False
    
    def setPerigo(self, perigo):
        self.perigo = perigo

        