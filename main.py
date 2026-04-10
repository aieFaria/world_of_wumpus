# Example file showing a basic pygame "game loop"
import pygame
from labirinto import Labirinto

class Main:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((700, 700))
        pygame.display.set_caption("World of Wumpus")
        self.clock = pygame.time.Clock()
        self.labirinto = Labirinto()

    def executar(self, posicao_inicial=(0, 0)):
        self.posicao_inicial = posicao_inicial
        
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RIGHT and self.posicao_inicial[1] < 7:
                        print(self.posicao_inicial[1])
                        self.posicao_inicial = (self.posicao_inicial[0], self.posicao_inicial[1] + 1)
                    if evento.key == pygame.K_LEFT and self.posicao_inicial[1] > 0:
                        print(self.posicao_inicial[1])
                        self.posicao_inicial = (self.posicao_inicial[0], self.posicao_inicial[1] - 1)
                    if evento.key == pygame.K_DOWN and self.posicao_inicial[0] < 7:
                        print(self.posicao_inicial[0])
                        self.posicao_inicial = (self.posicao_inicial[0] + 1, self.posicao_inicial[1])
                    if evento.key == pygame.K_UP and self.posicao_inicial[0] > 0:
                        print(self.posicao_inicial[0])
                        self.posicao_inicial = (self.posicao_inicial[0] - 1, self.posicao_inicial[1])

            
            # teclas = pygame.key.get_pressed()
            # if teclas[pygame.K_RIGHT] and self.posicao_inicial[1] < 8:
            #     print(self.posicao_inicial[1])
            #     self.posicao_inicial = (0, self.posicao_inicial[1] + 1)
            # if teclas[pygame.K_LEFT] and self.posicao_inicial[1] > 0:
            #     self.posicao_inicial = (0, self.posicao_inicial[1] - 1)
            # if teclas[pygame.K_DOWN] and self.posicao_inicial[0] < 8:
            #     self.posicao_inicial = (self.posicao_inicial[0] + 1, 0)
            # if teclas[pygame.K_UP] and self.posicao_inicial[0] > 0:
            #     self.posicao_inicial = (self.posicao_inicial[0] - 1, 0)

            self.labirinto.desenhar(self.tela, self.posicao_inicial)
            
            pygame.display.flip()
            self.clock.tick(5)

        pygame.quit()

index = Main()
index.executar()