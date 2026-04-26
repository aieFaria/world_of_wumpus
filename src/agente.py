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
        self.visitados = set()
        self.pilha_caminho = []
        self.historico = [] # Inicializa vazio

        self.ctrl = {"direcao": "frente", "posicao": (0, 0)}

        self.leituraLab = {} # Referente ao retorno do labirinto quando agente está ativo

    def executar(self):

        current_time = pygame.time.get_ticks()
        
        if self.leituraLab and not self.finalizado:
            if current_time - self.last_move_time > self.delayMove:

                # Evento personalizado para enviar ação do agente no labirinto
                evento = pygame.event.Event(pygame.KEYDOWN, {
                    'key': pygame.K_RIGHT,
                    'mod': 0,
                    'is_agent': True # Flag para identificar que o agente que moveu
                })
                
                pygame.event.post(evento)
                self.last_move_time = current_time
        
