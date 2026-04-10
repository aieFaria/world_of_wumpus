import pygame

from cons import RECT_COLOR, SQUARE_LENGTH

class Bloco:

    def __init__(self, pos_X, pos_Y, visible, teste):
        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.visible = visible
        self.teste = teste
        self.tamanho_quadrado = SQUARE_LENGTH

    def criar(self, linha, coluna, tela):
        if (self.visible):
            cor = [pygame.Color(RECT_COLOR), pygame.Color("gray")][(linha + coluna) % 2]
        else:
            cor = pygame.Color("black")

        rect = pygame.draw.rect(
            tela, 
            cor,
            (coluna * (self.tamanho_quadrado), linha * (self.tamanho_quadrado), self.tamanho_quadrado, self.tamanho_quadrado)
        )

        return rect