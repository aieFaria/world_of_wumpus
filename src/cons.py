# * Todas as classes
import os
import platform

LARGURA_TELA = 700
ALTURA_TELA = 700
ALTURA_TELA2 = 500
ALTURA_BARRA = 60

# Diretório
DIR_PATH = os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources")

# - Labirinto
RECT_COLOR = "skyblue"
TAMANHO_LAB = 6
TAMANHO_QUADRADO = ALTURA_TELA
# TAMANHO_QUADRADO = LARGURA_TELA // TAMANHO_LAB
PRINCIPAL_COLOR = (50, 50, 50)

# Fonte pixel
#FONTE_P = pygame.font.Font(os.path.join(self.directory_path, "resources", "font", "font.ttf"), size)