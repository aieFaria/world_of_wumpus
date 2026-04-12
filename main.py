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

    def executar(self, player_x, player_y):
        # Alteração: uso da posição como sendo tupla substituído para lista
        # isso otimiza o código e dispensa necessidade de repetição de uma dimensão
        # que não foi alterada na movimentação
        self.player_x = player_x
        self.player_y = player_y
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
                        # player_y substitui posicao_inicial[1]
                        print(self.player_y)
                        if self.direcao == "direita":
                            if self.player_y < 7:
                                self.player_y += 1
                        else:
                            self.direcao = "direita"
                        break

                    elif evento.key == pygame.K_LEFT:
                        print(self.player_y)
                        if self.direcao == "esquerda":
                            if self.player_y > 0:
                                self.player_y -= 1
                        else:
                            self.direcao = "esquerda"
                        break

                    elif evento.key == pygame.K_DOWN:
                        # player_x substitui posicao_inicial[0]
                        print(self.player_x)
                        if self.direcao == "frente":
                            if self.player_x < 7:
                                self.player_x += 1
                        else:
                            self.direcao = "frente"
                        break

                    elif evento.key == pygame.K_UP:
                        print(self.player_x)
                        if self.direcao == "costas":
                            if self.player_x > 0:
                                self.player_x -= 1
                        else:
                            self.direcao = "costas"
                        break

            self.labirinto.desenhar(self.tela, self.player_x, self.player_y, self.direcao)
            
            pygame.display.flip()
            self.clock.tick(5)

        pygame.quit()

index = Main()
index.executar(0, 0)