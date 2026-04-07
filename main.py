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

    def executar(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

            self.labirinto.desenhar(self.tela)
            
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

index = Main()
index.executar()