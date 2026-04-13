import pygame, os
from cons import WINDOW_LENGTH
from button import Button
from main import Main

class Index:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_LENGTH, WINDOW_LENGTH))
        self.COLOR = (50, 50, 50)
        self.main = Main()

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font(os.path.join("world_of_wumpus", "resources", "font", "font.ttf"), size)

    def iniciar(self, is_on=True):
        running = True
        while running:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            print("MENU_MOUSE_POS:", MENU_MOUSE_POS)

            MENU_TEXT = self.get_font(40).render("WORLD OF WUMPUS", True, "White")
            MENU_RECT = MENU_TEXT.get_rect(center=(WINDOW_LENGTH // 2, 100))
            
            self.screen.fill(self.COLOR)

            img = pygame.image.load(os.path.join("world_of_wumpus", "resources", "button_background.png")).convert_alpha()
            on_off_img = pygame.image.load(os.path.join("world_of_wumpus", "resources", "on_off_background.png")).convert_alpha()

            ON_BUTTON = Button(image=on_off_img, pos=(WINDOW_LENGTH // 2 + 170, 200), text_input="ON", font=self.get_font(15), base_color="#d7fcd4", hovering_color="#f09184")
            OFF_BUTTON = Button(image=on_off_img, pos=(WINDOW_LENGTH // 2 + 170, 200), text_input="OFF", font=self.get_font(15), base_color="#d7fcd4", hovering_color="#f09184")
            PLAY_BUTTON = Button(image=img, pos=(WINDOW_LENGTH // 2, 200), text_input="PLAY", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=img, pos=(WINDOW_LENGTH // 2, 400), text_input="QUIT", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")

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