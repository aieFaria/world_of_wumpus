import platform

import pygame, os
from cons import LARGURA_TELA, ALTURA_TELA2
from button import Button
from main import Main

class Index:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA2))
        pygame.display.set_caption("World of Wumpus")
        self.COLOR = (50, 50, 50)
        # self.main = Main() -> Removido para não causar sobrecarga
        self.directory_path = "world_of_wumpus" if platform.system() == "Windows" else ""

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        
        return pygame.font.Font(os.path.join(self.directory_path, "resources", "font", "font.ttf"), size)

    def iniciar(self, is_on=True):
        running = True
        while running:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            print("MENU_MOUSE_POS:", MENU_MOUSE_POS)

            MENU_TEXT = self.get_font(40).render("WORLD OF WUMPUS", True, "White")
            MENU_RECT = MENU_TEXT.get_rect(center=(LARGURA_TELA // 2, 100))
            
            self.screen.fill(self.COLOR)

            img = pygame.image.load(os.path.join(self.directory_path, "resources", "button_background.png")).convert_alpha()
            on_off_img = pygame.image.load(os.path.join(self.directory_path, "resources", "on_off_background.png")).convert_alpha()

            ON_BUTTON = Button(image=on_off_img, pos=(LARGURA_TELA // 2 + 170, 200), text_input="ON", font=self.get_font(15), base_color="#72eb62", hovering_color="#d7fcd4")
            OFF_BUTTON = Button(image=on_off_img, pos=(LARGURA_TELA // 2 + 170, 200), text_input="OFF", font=self.get_font(15), base_color="#f09184", hovering_color="#d7fcd4")
            PLAY_BUTTON = Button(image=img, pos=(LARGURA_TELA // 2, 200), text_input="PLAY", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=img, pos=(LARGURA_TELA // 2, 300), text_input="QUIT", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            if is_on:
                ON_BUTTON.changeColor(MENU_MOUSE_POS)
                ON_BUTTON.update(self.screen)
            else:
                OFF_BUTTON.changeColor(MENU_MOUSE_POS)
                OFF_BUTTON.update(self.screen)
            
            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if is_on:
                        if ON_BUTTON.checkForInput(MENU_MOUSE_POS):
                            print("ON")
                            is_on = False
                    else:
                        if OFF_BUTTON.checkForInput(MENU_MOUSE_POS):
                            print("OFF")
                            is_on = True

                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        print("Play")
                        self.main = Main() # Instanciar main apenas quando apertar play
                        if is_on:
                            # Iniciar o jogo com o agente ativado. is_on = True
                            self.main.executar(0, 0, is_on)
                        else:
                            # is_on = False, iniciar o jogo com o agente desativado
                            self.main.executar(0, 0, is_on)
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False
            
            pygame.display.update()
            # pygame.display.flip()

        pygame.quit()

index = Index()
index.iniciar(True)