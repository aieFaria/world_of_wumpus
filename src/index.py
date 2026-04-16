import pygame, os
from cons import *
from button import Button
from main import Main

class Index:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA2))
        pygame.display.set_caption("World of Wumpus")
        self.tamanho_lab = TAMANHO_LAB
        self.main = None

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        
        return pygame.font.Font(os.path.join(DIR_PATH, "font", "font.ttf"), size)

    def iniciar(self, is_on=True):
        running = True

        while running:

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(40).render("WORLD OF WUMPUS", True, "White")
            MENU_RECT = MENU_TEXT.get_rect(center=(LARGURA_TELA // 2, 80))
            SIZE_TEXT = self.get_font(10).render(f"Tamanho do labirinto: {self.tamanho_lab}x{self.tamanho_lab}", True, "White")
            SIZE_RECT = SIZE_TEXT.get_rect(center=(LARGURA_TELA // 2, 480))
            
            self.screen.fill(PRINCIPAL_COLOR)

            img = pygame.image.load(os.path.join(DIR_PATH, "button_background.png")).convert_alpha()
            on_off_img = pygame.image.load(os.path.join(DIR_PATH, "on_off_background.png")).convert_alpha()

            ON_BUTTON = Button(image=on_off_img, pos=(LARGURA_TELA // 2 + 170, 200), text_input="ON", font=self.get_font(15), base_color="#72eb62", hovering_color="#d7fcd4")
            OFF_BUTTON = Button(image=on_off_img, pos=(LARGURA_TELA // 2 + 170, 200), text_input="OFF", font=self.get_font(15), base_color="#f09184", hovering_color="#d7fcd4")
            PLAY_BUTTON = Button(image=img, pos=(LARGURA_TELA // 2, 200), text_input="PLAY", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=img, pos=(LARGURA_TELA // 2, 300), text_input="OPTIONS", font=self.get_font(29), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=img, pos=(LARGURA_TELA // 2, 400), text_input="QUIT", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)
            self.screen.blit(SIZE_TEXT, SIZE_RECT)

            if is_on:
                ON_BUTTON.changeColor(MENU_MOUSE_POS)
                ON_BUTTON.update(self.screen)
            else:
                OFF_BUTTON.changeColor(MENU_MOUSE_POS)
                OFF_BUTTON.update(self.screen)
            
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if is_on:
                        if ON_BUTTON.checkForInput(MENU_MOUSE_POS):
                            is_on = False
                    else:
                        if OFF_BUTTON.checkForInput(MENU_MOUSE_POS):
                            is_on = True

                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.main = Main(self.tamanho_lab)
                        self.main.executar(0, 0, is_on)
                        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA2))
                        pygame.display.set_caption("World of Wumpus")

                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.tamanho_lab = self.show_options()
                        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA2))
                        pygame.display.set_caption("World of Wumpus")

                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False
            
            pygame.display.flip()

        pygame.quit()

    """
    Método que desenha a tela de opções
    """
    def show_options(self):
        tamanho_lab = self.tamanho_lab
        clock = pygame.time.Clock()
        running = True

        OPTIONS_TEXT = self.get_font(40).render("OPTIONS", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(LARGURA_TELA // 2, 80))
        SIZE_TEXT = self.get_font(30).render(f"Tamanho: {tamanho_lab}x{tamanho_lab}", True, "White")
        SIZE_RECT = SIZE_TEXT.get_rect(center=(LARGURA_TELA // 2, 180))
        HELP_TEXT = self.get_font(20).render("↑/↓ mudar tamanho\n\n ENTER salvar\n\n ESC voltar", True, "White")
        HELP_RECT = HELP_TEXT.get_rect(center=(LARGURA_TELA // 2, 260))

        while running:
            # self.screen.fill(PRINCIPAL_COLOR)
            self.screen.blit(pygame.image.load(os.path.join(DIR_PATH, "endgame_bg.png")), (0, 0))

            # TECLA ENTER E ESC voltam e salvam, ambas
            
            self.screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
            self.screen.blit(SIZE_TEXT, SIZE_RECT)
            self.screen.blit(HELP_TEXT, HELP_RECT)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        tamanho_lab += 1
                    elif event.key == pygame.K_DOWN and tamanho_lab > TAMANHO_LAB: 
                        # Tamanho padrão -> 6, aparentemente, tamanho = 4 trava o jogo. E tamanho = 5 funciona normalmente.
                        tamanho_lab -= 1
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN: # TECLA ESC ou ENTER
                        running = False
                        break

            pygame.display.flip()
            clock.tick(30)

        return tamanho_lab

index = Index()
index.iniciar(True)