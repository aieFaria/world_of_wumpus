# * Todas as classes
import os
import platform

LARGURA_TELA = 700
ALTURA_TELA = 700
ALTURA_TELA2 = 400
ALTURA_BARRA = 60

# Diretório
DIR_PATH = os.path.join("world_of_wumpus" if platform.system() == "Windows" else "", "resources")

# - Labirinto
RECT_COLOR = "skyblue"
QUADRADO_TAMANHO = 700 // 8
PRINCIPAL_COLOR = (50, 50, 50)

# Fonte pixel
#FONTE_P = pygame.font.Font(os.path.join(self.directory_path, "resources", "font", "font.ttf"), size)
