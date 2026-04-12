import pygame
import os
import platform

from cons import SQUARE_LENGTH

class Bloco:

    # Atributos de um bloco (sala):
    # - posição X e Y (linha e coluna)
    # - visibilidade (se o jogador já passou por ali ou não)
    # - Buraco (pit)
    # - Wumpus (wumpus)
    # - Morcegos (bats)
    # - Flecha (arrow)
    # - Ouro (gold)
    # - Atributos (blocos adjacentes a um buraco ou wumpus tem atributos de "Breeze" e "Stench", respectivamente)
                                   
    def __init__(self, pos_X, pos_Y, visible, pit, wumpus, bats=False, arrow=False, gold=False):
        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.visible = visible
        self.hasPit = pit
        self.hasWumpus = wumpus
        self.hasBats = bats
        self.hasArrow = arrow
        self.hasGold = gold

        self.attributes = []
        self.tamanho_quadrado = SQUARE_LENGTH
        self.font = pygame.font.SysFont('Arial', 18)
    
    # Método para visualização dos atributos do bloco
    # def __str__(self):
    #     return f"Linha: {self.pos_X} - Coluna: {self.pos_Y}\nVisibilidade: {self.visible}"

    def criar(self, linha, coluna, tela):
        cor = pygame.Color("gray")
        
        rect = pygame.draw.rect(
            tela,
            cor,
            (coluna * (self.tamanho_quadrado), linha * (self.tamanho_quadrado), self.tamanho_quadrado, self.tamanho_quadrado)
        )

        lista_atributos = []
        # Gambiarra temporária, para carregar imagem de fundo
        # Buracos, e adicionar propriedades.
        if (self.visible):
            bg = pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "background.png")).convert_alpha()
            if (self.hasPit):
                bg = pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "buraco.png")).convert_alpha()
                # Só aparece o texto se ele for utilizzado depois de tela.blit(bg, ...)
            elif (self.hasWumpus):
                bg = pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "wumpus.png")).convert_alpha()
            elif (self.hasBats):
                bg = pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "morcego.png")).convert_alpha()
            elif (self.hasArrow):
                bg = pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "flecha.png")).convert_alpha()
            if (self.hasGold):
                bg = pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "ouro.png")).convert_alpha()
            
        else:
            bg = pygame.image.load(os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources", "nevoa.png")).convert_alpha()
        
        tela.blit(bg, bg.get_rect(center=rect.center))
        
        if self.attributes and self.visible:
            text_surf = self.font.render(f"{''.join(self.attributes)}", True, pygame.Color("white"))
            text_rect = text_surf.get_rect(center=rect.center)
            tela.blit(text_surf, text_rect)

        return rect
    
    def isVisible(self):
        return self.visible

    def setVisible(self, param=False): 
        self.visible = param

    def setPit(self, param=False):
        self.hasPit = param

    def setWumpus(self, param=False):
        self.hasWumpus = param
    
    def removeAttributes(self):
        for attribute in self.attributes:
            self.attributes.remove(attribute)

    def hasStench(self):
        # Se o bloco é visivel retorna se te
        if(self.visible):
            return "Stench\n" in self.attributes
        else:
            return False
        
    def hasBreeze(self):
        if(self.visible):
            return "Breeze\n" in self.attributes
        else:
            return False
    
    def hasFlappings(self):
        if(self.visible):
            return "Flapping" in self.attributes
        else:
            return False
        
    # Reconfigurando bloco, todos parametros False por padrão
    def reconfigurar(self, visible=False, pit=False, wummpus=False, bats=False, arrow=False, gold=False):
        self.visible = visible
        self.hasPit = pit
        self.hasWumpus = wummpus
        self.hasBats = bats
        self.hasArrow = arrow
        self.hasGold = gold
