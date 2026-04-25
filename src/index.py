import pygame, os
from cons import *
from button import Button
from main import Main

class Index:
    def __init__(self):
        # Forma de centralizar tela independentemente da navegação entre as telas
        os.environ['SDL_VIDEO_CENTERED'] = '1'

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
            # Falta configurar o botão de como jogar
            HELP_BUTTON = Button(None, pos=(80, ALTURA_TELA2-30), text_input="Como jogar?", font=self.get_font(10), base_color="#ff7e7e", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)
            self.screen.blit(SIZE_TEXT, SIZE_RECT)

            if is_on:
                ON_BUTTON.changeColor(MENU_MOUSE_POS)
                ON_BUTTON.update(self.screen)
            else:
                OFF_BUTTON.changeColor(MENU_MOUSE_POS)
                OFF_BUTTON.update(self.screen)
            
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, HELP_BUTTON]:
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
                        # self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA2))
                        # Removido para evitar da janela descer sempre que fechar as opções
                        pygame.display.set_caption("World of Wumpus")

                    if HELP_BUTTON.checkForInput(MENU_MOUSE_POS):
                        # definir o que vai acontecer quando clicar em "Como jogar?"
                        self.mostrar_teclas()
                        print("Como jogar?")

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
        dragging = False
        
        OPTIONS_TEXT = self.get_font(40).render("OPTIONS", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(LARGURA_TELA // 2, 80))
        HELP_TEXT = self.get_font(12).render("↑/↓ mudar tamanho\n\n ENTER salvar\n\n ESC voltar", True, "White")
        HELP_RECT = HELP_TEXT.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA2 - 50))

        while running:
            # self.screen.fill(PRINCIPAL_COLOR)
            self.screen.blit(pygame.image.load(os.path.join(DIR_PATH, "endgame_bg.png")), (0, 0))

            # Alterado a posição de declaração para atualizar sempre que clicar nas setinhas
            SIZE_TEXT = self.get_font(30).render(f"Tamanho: {tamanho_lab}x{tamanho_lab}", True, "White")
            SIZE_RECT = SIZE_TEXT.get_rect(center=(LARGURA_TELA // 2, 180))
            # TECLA ENTER E ESC voltam e salvam, ambas

            self.screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
            self.screen.blit(SIZE_TEXT, SIZE_RECT)
            self.screen.blit(HELP_TEXT, HELP_RECT)
            self.draw_slider(tamanho_lab)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    # Definindo limite superior para 20x20 que testei e funciona corretamente
                    if event.key == pygame.K_UP and tamanho_lab < 20:
                        tamanho_lab += 1
                    elif event.key == pygame.K_DOWN and tamanho_lab > TAMANHO_LAB: 
                        # Tamanho padrão -> 6, aparentemente, tamanho = 4 trava o jogo. E tamanho = 5 funciona normalmente.
                        # e tamanho = 40 também trava o jogo
                        tamanho_lab -= 1
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN: # TECLA ESC ou ENTER
                        running = False
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    x_slider_start = LARGURA_TELA // 2 - SL_RECT_LARGURA // 2
                    x_slider_end = LARGURA_TELA // 2 + SL_RECT_LARGURA // 2
                    y_slider = ALTURA_TELA2 // 2 + SL_RECT_ALTURA // 2
                    # Check if click is within slider bounds and handle (radius 13)
                    if (x_slider_start - 30 <= mx <= x_slider_end + 30) and (y_slider - 15 <= my <= y_slider + 15):
                        dragging = True
                if event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                if event.type == pygame.MOUSEMOTION and dragging:
                    x_slider_start = LARGURA_TELA // 2 - SL_RECT_LARGURA // 2
                    x_slider_end = LARGURA_TELA // 2 + SL_RECT_LARGURA // 2
                    mx = max(x_slider_start, min(event.pos[0], x_slider_end))
                    # Map mouse position to tamanho_lab range (6 to 20)
                    relative_pos = (mx - x_slider_start) / SL_RECT_LARGURA
                    tamanho_lab = int(TAMANHO_LAB + relative_pos * (20 - TAMANHO_LAB))
            
            pygame.display.flip()
            clock.tick(30)

        return tamanho_lab
    
    def draw_slider(self, value):
        x = LARGURA_TELA // 2 - SL_RECT_LARGURA // 2
        y = ALTURA_TELA2 // 2

        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, SL_RECT_LARGURA, SL_RECT_ALTURA), border_radius=13)
        min_size = TAMANHO_LAB
        max_size = 20
        handle_x = x + int(((value - min_size) / (max_size - min_size)) * SL_RECT_LARGURA)
        pygame.draw.circle(self.screen, (0, 0, 0), (handle_x, y+SL_RECT_ALTURA//2), 11)

    """
    Método que desenha a tela de tutorial/teclas permitidas no jogo
    """
    def mostrar_teclas(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.blit(pygame.image.load(os.path.join(DIR_PATH, "endgame_bg.png")), (0, 0))
            self.screen.blit(pygame.image.load(os.path.join(DIR_PATH, "teclas", "setas.png")), (10, 10))

            self.screen.blit(pygame.image.load(os.path.join(DIR_PATH, "teclas", "enter.png")), (400, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            pygame.display.flip()
            clock.tick(30)

index = Index()
index.iniciar(True)