# Example file showing a basic pygame "game loop"
import pygame
from labirinto import Labirinto
from agente import Agente

class Main:
    def __init__(self):
        pygame.init()
        # Janela de tamanho fixo
        self.LARGURA_TELA = 700
        self.ALTURA_TELA = 700
        self.ALTURA_BARRA = 60

        self.tela = pygame.display.set_mode((self.LARGURA_TELA, self.ALTURA_TELA))
        pygame.display.set_caption("World of Wumpus")
        self.clock = pygame.time.Clock()
        self.labirinto = Labirinto()
        self.agente = Agente(1, self.labirinto)
        self.ativa_agente = True
        self.fonte = pygame.font.SysFont("Arial", 20, bold=True)

    def desenhar_barra(self):
        # Fundo da barra completamente branco
        pygame.draw.rect(self.tela, (255, 255, 255), (0, 0, self.LARGURA_TELA, self.ALTURA_BARRA))
        
        tamanho_slot = 40
        espaco_slot = 10
        y_slot = (self.ALTURA_BARRA - tamanho_slot) // 2
        
        # Desenhando 3 slots como exemplo (para flecha, ouro, etc.)
        for i in range(1):
            x_slot = 20 + i * (tamanho_slot + espaco_slot)
            # Fundo do slot (cinza claro para destacar do branco)
            pygame.draw.rect(self.tela, (220, 220, 220), (x_slot, y_slot, tamanho_slot, tamanho_slot))
            # Borda do slot (preto)
            pygame.draw.rect(self.tela, (0, 0, 0), (x_slot, y_slot, tamanho_slot, tamanho_slot), 2)
            
            if( self.labirinto.hasArrow ):
                img_arco = self.labirinto.bloco.caracteristica["arco"]
                self.tela.blit(img_arco, (x_slot + 5, y_slot + 5))
#           img_arco, img_arco.get_rect(center=rect.center)

        # --- Lado Direito: Pontuação ---
        # Renderiza o texto na cor preta para contrastar com o fundo branco
        texto_pontos = self.fonte.render(f"Pontos: {self.labirinto.pontuacao}", True, (0, 0, 0)) #{self.pontuacao}
        text_rect = texto_pontos.get_rect()
        
        # Centraliza verticalmente e alinha à direita com uma margem de 20px
        text_rect.centery = self.ALTURA_BARRA // 2
        text_rect.right = self.LARGURA_TELA - 20
        
        self.tela.blit(texto_pontos, text_rect)

    def executar(self, player_x, player_y):
        # Alteração: uso da posição como sendo tupla substituído para lista
        # isso otimiza o código e dispensa necessidade de repetição de uma dimensão
        # que não foi alterada na movimentação
        self.player_x = player_x
        self.player_y = player_y
        self.direcao = "frente"
        
        tamanho_original_lab = 64 #self.tamanho_mapa * self.labirinto.tamanho_quadrado
        #tela_virtual = pygame.Surface((tamanho_original_lab, tamanho_original_lab))

        rodando = True
        while rodando:

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.KEYDOWN and not self.ativa_agente:

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
                    
            # Executa o agente caso ele esteja ativo
            # self.ativa_agente define isso
            if self.ativa_agente:
                self.agente.executar(self)
                # if self.agente.finalizado:
                #     print()
                        
            self.labirinto.desenhar(self.tela, self.player_x, self.player_y, self.direcao, self.ALTURA_BARRA, self.LARGURA_TELA, self.ALTURA_TELA)
            
            self.desenhar_barra()
            
            pygame.display.flip()
            self.clock.tick(5)

        pygame.quit()

index = Main()
index.executar(0, 0)