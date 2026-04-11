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
        

    def executar(self, posicao_inicial=[0, 0]):
        # Alteração: uso da posição como sendo tupla substituído para lista
        # isso otimiza o código e dispensa necessidade de repetição de uma dimensão
        # que não foi alterada na movimentação
        self.posicao_inicial = posicao_inicial
        self.direcao = "frente"
        
        # Alterações: Modificada forma como eram modificadas as posições para se adequar a um lista;
        #             Adicionando estrutura "elif" juntamente aos "break" para impedir movimentação 
        #             na diagonal e respeitar a situação de um clique por vez;
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.KEYDOWN:
                    # Condicional modificada para inalterar posição quando personagem não estiver olhando 
                    # para direção correta
                    if evento.key == pygame.K_RIGHT:
                        print(self.posicao_inicial[1])
                        if self.direcao == "direita":
                            if self.posicao_inicial[1] < 7:
                                self.posicao_inicial[1] += 1
                        else:
                            self.direcao = "direita"
                        break

                    elif evento.key == pygame.K_LEFT:
                        print(self.posicao_inicial[1])
                        if self.direcao == "esquerda":
                            if self.posicao_inicial[1] > 0:
                                self.posicao_inicial[1] -= 1
                        else:
                            self.direcao = "esquerda"
                        break

                    elif evento.key == pygame.K_DOWN:
                        print(self.posicao_inicial[0])
                        if self.direcao == "frente":
                            if self.posicao_inicial[0] < 7:
                                self.posicao_inicial[0] += 1
                        else:
                            self.direcao = "frente"
                        break

                    elif evento.key == pygame.K_UP:
                        print(self.posicao_inicial[0])
                        if self.direcao == "costas":
                            if self.posicao_inicial[0] > 0:
                                self.posicao_inicial[0] -= 1
                        else:
                            self.direcao = "costas"
                        break

            
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

            self.labirinto.desenhar(self.tela, self.posicao_inicial, self.direcao)
            
            pygame.display.flip()
            self.clock.tick(5)

        pygame.quit()

index = Main()
index.executar()