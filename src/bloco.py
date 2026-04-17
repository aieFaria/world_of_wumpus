import os, pygame

from cons import TAMANHO_QUADRADO, DIR_PATH

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
        self.hasWumpus = wumpus # Trocando de verdadeiro e falso para "vivo" ou "morto", para false usar ""
        self.hasBats = bats
        self.hasArrow = arrow
        self.hasGold = gold

        self.attributes = []
        self.tamanho_quadrado = TAMANHO_QUADRADO
        self.font = pygame.font.SysFont('Arial', 20)

        self.caracteristica = {
            "background": pygame.image.load(os.path.join(DIR_PATH, "background.png")).convert_alpha(),
            "buraco": pygame.image.load(os.path.join(DIR_PATH, "buraco.png")).convert_alpha(),
            "wumpus": pygame.image.load(os.path.join(DIR_PATH, "wumpusVivo2.png")).convert_alpha(),
            "morcego": pygame.image.load(os.path.join(DIR_PATH, "morcego.png")).convert_alpha(),
            "flecha": pygame.image.load(os.path.join(DIR_PATH, "flecha.png")).convert_alpha(),
            "ouro": pygame.image.load(os.path.join(DIR_PATH, "ouro.png")).convert_alpha(),
            "nevoa": pygame.image.load(os.path.join(DIR_PATH, "nevoa.png")).convert_alpha(),
            "arco": pygame.image.load(os.path.join(DIR_PATH, "arco.png")).convert_alpha(),
            "casa": pygame.image.load(os.path.join(DIR_PATH, "home.png")).convert_alpha(),
            "wumpusMorto": pygame.image.load(os.path.join(DIR_PATH, "wumpusMorto2.png")).convert_alpha()
        }
    
    # Método para visualização dos atributos do bloco
    # def __str__(self):
    #     return f"Linha: {self.pos_X} - Coluna: {self.pos_Y}\nVisibilidade: {self.visible}"

    def criar(self, linha, coluna, tela):
        rect = pygame.draw.rect(
            tela,
            pygame.Color("gray"),
            (coluna * (self.tamanho_quadrado), linha * (self.tamanho_quadrado), self.tamanho_quadrado, self.tamanho_quadrado)
        )

        # lista_atributos = []
        # Alteração para economizar processamento
        if (self.visible):
            bg = self.caracteristica["background"]
            if( self.hasPit ): bg = self.caracteristica["buraco"]
            elif( self.hasWumpus ): bg = self.caracteristica["wumpus" if self.hasWumpus == "vivo" else "wumpusMorto"]
            elif( self.hasBats ): bg = self.caracteristica["morcego"]
            elif( self.hasArrow ): bg = self.caracteristica["flecha"]
            elif( self.hasGold ): bg = self.caracteristica["ouro"]
            if( [linha, coluna] == [0, 0] ): bg = self.caracteristica["casa"]
            
        else:
            bg = self.caracteristica["nevoa"]
        
        tela.blit(bg, bg.get_rect(center=rect.center))
        
        if self.attributes and self.visible:
            text_surf = self.font.render(f"{''.join(self.attributes)}", True, pygame.Color("Black"))
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
    def reconfigurar(self, visible=False, pit=False, wumpus=False, bats=False, arrow=False, gold=False):
        self.visible = visible
        self.hasPit = pit
        self.hasWumpus = wumpus
        self.hasBats = bats
        self.hasArrow = arrow
        self.hasGold = gold