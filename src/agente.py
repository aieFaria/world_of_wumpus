import time
import pygame
from labirinto import Labirinto

class Agente:
    # Atributos de classe
    delayMove = 200

    def __init__(self, id):
        # Atributo de instância do agente
        self.id = id
        self.ponteiro = 0
        self.last_move_time = 0
        self.finalizado = False
        self.visitados = set((3, 3))
        self.pilha_caminho = [(3, 3)]
        self.historico = [] # Inicializa vazio

        self.ctrl = {"direcao": "frente", "posicao": (0, 0)}

        self.leituraLab = {} # Referente ao retorno do labirinto quando agente está ativo

    def executar(self):

        current_time = pygame.time.get_ticks()
        
        if self.leituraLab and not self.finalizado:
            if current_time - self.last_move_time > self.delayMove:
                x, y = self.leituraLab.get("bloco")
                #  = bloco
                
                if (self.pilha_caminho):
                    teste = self.pilha_caminho.pop()

                    if ((x, y) != teste):
                        self.movimentacao_segura(x, y, teste)
                        self.pilha_caminho.append(teste)

                self.last_move_time = current_time

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
            if (atr == "Breeze/n"):
                