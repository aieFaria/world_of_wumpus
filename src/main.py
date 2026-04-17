# Example file showing a basic pygame "game loop"
import base64
import os, pygame

from button import Button
from cons import *
from labirinto import Labirinto
from agente import Agente

class Main:
    def __init__(self, tamanho_lab=TAMANHO_LAB):
        pygame.init()
        self.tamanho_lab = tamanho_lab
        
        # Janela de tamanho fixo
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self.tela.fill(PRINCIPAL_COLOR)
        pygame.display.set_caption("World of Wumpus")
        self.clock = pygame.time.Clock()
        
        self.labirinto = Labirinto(self.tamanho_lab) # TAMANHO_LAB = 6 PADRÃO
        self.agente = Agente(1, self.labirinto)
        #pygame.font.Font(os.path.join(self.directory_path, "resources", "font", "font.ttf"), size)
        self.fonte = pygame.font.Font(os.path.join(DIR_PATH, "font", "font.ttf"), 20)
        self.acao = False      

        img_btn_central = pygame.image.load(os.path.join(DIR_PATH, "pause.png")).convert_alpha()
        #img_btn_central.fill((255, 255, 255))
        self.botao_central = Button(
            image=img_btn_central.copy(), 
            pos=((LARGURA_TELA)//2, ALTURA_BARRA // 2)
        )
        # Para funcionamento correta da tela de execução e de pausa
        self.rodando = True
        self.pause = False # Variável para controlar a pausa do jogo.

    """
    Método que desenha a barra de status na tela de execução
    """
    def desenhar_barra(self):
        pygame.draw.rect(self.tela, PRINCIPAL_COLOR, (0, 0, LARGURA_TELA, ALTURA_BARRA))
        
        tamanho_slot = 40
        espaco_slot = 10
        y_slot = (ALTURA_BARRA - tamanho_slot) // 2
        
        # Desenhando slot
        for i in range(1):
            x_slot = 20 + i * (tamanho_slot + espaco_slot)
            # Fundo do slot (cinza claro para destacar do branco)
            pygame.draw.rect(self.tela, (220, 220, 220), (x_slot, y_slot, tamanho_slot, tamanho_slot))
            # Borda do slot (preto)
            pygame.draw.rect(self.tela, (0, 0, 0), (x_slot, y_slot, tamanho_slot, tamanho_slot), 2)
            
            if( self.labirinto.hasArrow ):
                img_arco = self.labirinto.bloco.caracteristica["arco"]
                self.tela.blit(img_arco, (x_slot + 5, y_slot + 5))

                self.fonte_pequena = pygame.font.Font(os.path.join(DIR_PATH, "font", "font.ttf"), 10)

                base_x = x_slot + tamanho_slot - 2
                base_y = y_slot + tamanho_slot - 2
                
                # Geração de contorno, gera um texto branco
                texto_contorno = self.fonte_pequena.render( "x" + str(self.labirinto.qtd_flechas) 
                                                           , True, (255, 255, 255))
                offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
                for ox, oy in offsets:
                    self.tela.blit(texto_contorno, 
                                   texto_contorno.get_rect(bottomright=(base_x + ox, base_y + oy)))

                # Passo final colocar texto preto por cima do branco
                texto_qtd = self.fonte_pequena.render("x" + str(self.labirinto.qtd_flechas)
                                                      , True, (0, 0, 0))
                self.tela.blit(texto_qtd, texto_qtd.get_rect(bottomright=(base_x, base_y)))
#           img_arco, img_arco.get_rect(center=rect.center)
        
        # Exemplo de bloco centralizado
        # pygame.draw.rect(self.tela, (255, 255, 255), ((LARGURA_TELA-tamanho_slot)//2, y_slot, tamanho_slot, tamanho_slot))
        mouse_pos = pygame.mouse.get_pos()
        self.botao_central.changeColorImagem(mouse_pos)
        self.botao_central.update(self.tela)

        # Mostrando a Pontuação
        texto_pontos = self.fonte.render(f"Pontos: {self.labirinto.pontuacao}", True, (255, 255, 255)) #{self.pontuacao}
        text_rect = texto_pontos.get_rect()
        
        # Centraliza verticalmente e alinha à direita com uma margem de 20px
        text_rect.centery = ALTURA_BARRA // 2
        text_rect.right = LARGURA_TELA - 20
        
        self.tela.blit(texto_pontos, text_rect)

    """
    Método que desenha a tela de execução do jogo
    """
    def executar(self, player_x, player_y, ativar_agente=False):
        # Alteração: uso da posição como sendo tupla substituído para lista
        # isso otimiza o código e dispensa necessidade de repetição de uma dimensão
        # que não foi alterada na movimentação
        self.player_x = player_x
        self.player_y = player_y
        self.ativa_agente = ativar_agente
        self.direcao = "frente"
        
        tamanho_original_lab = 64 #self.tamanho_mapa * self.labirinto.tamanho_quadrado
        #tela_virtual = pygame.Surface((tamanho_original_lab, tamanho_original_lab))

        # rodando = True
        while self.rodando:
            
            self.acao = False
            mouse_pos = pygame.mouse.get_pos() # Verificar se pode tirar daqui

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    # Finalizar index
                    self.labirinto.aux_parar_sons()
                    self.rodando = False

                # Captura do evento "Apertar no botão de pause"
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.botao_central.checkForInput(mouse_pos):
                        print("Botão central clicado!")
                        self.pause = True
                        self.rodando = False
                        self.paused()
                        # Exemplo: Fechar o jogo e voltar para o Menu Principal

                if evento.type == pygame.KEYDOWN and not self.ativa_agente:

                    # Condicional modificada para inalterar posição quando personagem não estiver olhando 
                    # para direção correta
                    if evento.key == pygame.K_RIGHT:
                        # player_y substitui posicao_inicial[1]
                        # print(self.player_y)
                        if self.direcao == "direita":
                            if self.player_y < self.tamanho_lab-1:
                                self.player_y += 1
                        else:
                            self.direcao = "direita"
                        break

                    elif evento.key == pygame.K_LEFT:
                        # print(self.player_y)
                        if self.direcao == "esquerda":
                            if self.player_y > 0:
                                self.player_y -= 1
                        else:
                            self.direcao = "esquerda"
                        break

                    elif evento.key == pygame.K_DOWN:
                        # player_x substitui posicao_inicial[0]
                        # print(self.player_x)
                        if self.direcao == "frente":
                            if self.player_x < self.tamanho_lab-1:
                                self.player_x += 1
                        else:
                            self.direcao = "frente"
                        break

                    elif evento.key == pygame.K_UP:
                        # print(self.player_x)
                        if self.direcao == "costas":
                            if self.player_x > 0:
                                self.player_x -= 1
                        else:
                            self.direcao = "costas"
                        break

                    elif evento.key == pygame.K_KP_ENTER or evento.key == pygame.K_RETURN:
                        #print("acao")
                        self.acao = True
                    
            # Executa o agente caso ele esteja ativo
            # self.ativa_agente define isso
            if self.ativa_agente:
                self.agente.executar(self)
                # if self.agente.finalizado:
                #     print()
       
            resposta = self.labirinto.desenhar(self.tela, self.player_x, self.player_y, self.direcao, self.acao, ALTURA_BARRA, LARGURA_TELA, ALTURA_TELA)
            self.player_x, self.player_y = resposta.get("bloco", (-1, -1))

            """
            # Mostra no console o retorno do método desenhar:
            # Serve de exemplo para como o agente irá tratar os dados de retorno
            print(f"Bloco: {resposta.get('bloco')}\n",
                  f"Atributos: {resposta.get('atributos', [])}\n",
                  f"Pontuacao: {resposta.get('pontuacao', 0)}\n"
                  f"Caracteristicas: \n",
                  f"  - Tem Wumpus: {resposta.get('hasWumpus')}\n",
                  f"  - Tem Morcegos: {resposta.get('hasBats')}\n",
                  f"  - Tem Buraco: {resposta.get('hasPit')}\n",
                  f"  - Tem Flecha: {resposta.get('hasArrow')}\n",
                  f"  - Tem Gold: {resposta.get('hasGold')}\n",
                  f"Status: " {resposta.get('status')})
            """

            self.desenhar_barra()
            if( resposta.get('status') != 0 ):

                self.labirinto.desenhar(self.tela, self.player_x, self.player_y, self.direcao, False, ALTURA_BARRA, LARGURA_TELA, ALTURA_TELA)
                pygame.display.flip()

                textoFinal = ""

                if(resposta.get('status') == 1):
                    textoFinal = "Perdeuuu!"
                elif( resposta.get('status') == 2 ):
                    if ( resposta.get('pontuacao') < 1000 ):
                        textoFinal = "Fraco..."
                    elif ( resposta.get('pontuacao') > 2000 ):
                        textoFinal = self.geraTexto('paiNosso')
                    else:
                        textoFinal = " Saiu do labirinto!\n Pelo meno tá vivo"

                self.endgame(textoFinal)

            pygame.display.flip()
            self.clock.tick(10)

        #pygame.quit()

    """
    Método que desenha a tela de pausa
    """
    def paused(self):

        fundo_pausado = self.tela.copy()
        # self.tela.blit(pygame.image.load(os.path.join(DIR_PATH, "endgame_bg.png")), (0, 0))

        pelicula = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        pelicula.set_alpha(170) # Nível de escurecimento (0 a 255)
        pelicula.fill((0, 0, 0)) 

        # Carregando constantes apenas uma vez
        FONT = pygame.font.Font(os.path.join(DIR_PATH, "font", "font.ttf"), 35)
        PAUSED_TEXT = FONT.render("Jogo pausado", True, "White")
        PAUSED_RECT = PAUSED_TEXT.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 59*2 +50)) # 
        # 59 PIXELS
        # -(59 + 100 + 59 - 35)
        img = pygame.image.load(os.path.join(DIR_PATH, "button_background.png")).convert_alpha()

        PLAY_BUTTON = Button(image=img, pos=(LARGURA_TELA // 2, ALTURA_TELA // 2 + (50-35)), text_input="BACK", font=FONT, base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=img, pos=(LARGURA_TELA // 2, ALTURA_TELA // 2 + (200-35-59)), text_input="QUIT", font=FONT, base_color="#d7fcd4", hovering_color="White")

        rodando = True
        while rodando:
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Colocando fundo pausado!
            self.tela.blit(fundo_pausado, (0, 0))
            self.tela.blit(pelicula, (0, 0))
            
            self.tela.blit(PAUSED_TEXT, PAUSED_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.tela)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        # Incrementar dificuldade, caso o jogador tenha GANHADO o jogo e não pausado.
                        # Voltar ao jogo, caso o jogador tenha PARADO o jogo
                        if (self.pause == True):
                            self.pause = False
                            self.rodando = True
                            rodando = False
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        rodando = False

            pygame.display.flip()


    
    def endgame(self, texto):
        
        fundo_pausado = self.tela.copy()
        
        try:
            bg_pause = pygame.image.load(os.path.join(DIR_PATH, "endgame_bg.png")).convert()
            bg_pause = pygame.transform.scale(bg_pause, (LARGURA_TELA, ALTURA_TELA))
        except:
            bg_pause = fundo_pausado

        pelicula = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        pelicula.set_alpha(150) 
        pelicula.fill((0, 0, 0)) 

        # Carregando fontes
        FONT_TITULO = pygame.font.Font(os.path.join(DIR_PATH, "font", "font.ttf"), 35)
        FONT_TEXTO = pygame.font.Font(os.path.join(DIR_PATH, "font", "font.ttf"), 20)

        popup_largura = 400
        popup_altura = 350
        popup_x = (LARGURA_TELA - popup_largura) // 2
        popup_y = (ALTURA_TELA - popup_altura) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_largura, popup_altura)

        titulo_text = FONT_TITULO.render("GAME OVER", True, "Black")
        titulo_rect = titulo_text.get_rect(center=(LARGURA_TELA // 2, popup_y + 50))

        resultado_text = FONT_TEXTO.render(f"{texto}", True, "Black")
        resultado_rect = resultado_text.get_rect(center=(LARGURA_TELA // 2, popup_y + 110))

        pontuacao_text = FONT_TEXTO.render(f"Pontuacao: {self.labirinto.pontuacao}", True, "Black")
        pontuacao_rect = pontuacao_text.get_rect(center=(LARGURA_TELA // 2, popup_y + 160))

        img = pygame.image.load(os.path.join(DIR_PATH, "button_background.png")).convert_alpha()
        olho = pygame.image.load(os.path.join(DIR_PATH, "olhoBranco.png")).convert_alpha()
        # Botões do Popup
        VIEW_GAME_BTN = Button(image=img, pos=(LARGURA_TELA // 2, popup_y + 230), text_input="VIEW", font=FONT_TEXTO, base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=img, pos=(LARGURA_TELA // 2, popup_y + 300), text_input="QUIT", font=FONT_TEXTO, base_color="#d7fcd4", hovering_color="White")

        # Botão exclusivo para a vista do tabuleiro limpo (fora do popup)
        VOLTAR_MENU_BTN = Button(image=img, pos=(LARGURA_TELA // 2, ALTURA_TELA - 60), text_input="VOLTAR", font=FONT_TEXTO, base_color="#d7fcd4", hovering_color="White")

        mostrar_jogo = False
        rodando = True
        
        while rodando:
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            if mostrar_jogo:
                self.tela.blit(fundo_pausado, (0, 0))
                self.tela.blit(pelicula, (0, 0))
                botoes_ativos = [VOLTAR_MENU_BTN]
            else:
                self.tela.blit(bg_pause, (0, 0))
                
                pygame.draw.rect(self.tela, (255, 255, 255), popup_rect, border_radius=15)
                pygame.draw.rect(self.tela, (0, 0, 0), popup_rect, 4, border_radius=15)

                self.tela.blit(titulo_text, titulo_rect)
                self.tela.blit(resultado_text, resultado_rect)
                self.tela.blit(pontuacao_text, pontuacao_rect)
                
                botoes_ativos = [VIEW_GAME_BTN, QUIT_BUTTON]

            for button in botoes_ativos:
                button.changeColor(MENU_MOUSE_POS)
                button.changeColorImagem(MENU_MOUSE_POS)
                button.update(self.tela)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                    self.rodando = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in botoes_ativos:
                        if button.checkForInput(MENU_MOUSE_POS):
                            if button == QUIT_BUTTON:
                                rodando = False
                                self.rodando = False
                            elif button == VIEW_GAME_BTN:
                                mostrar_jogo = True  # Oculta o quadrado branco e mostra o labirinto
                            elif button == VOLTAR_MENU_BTN:
                                mostrar_jogo = False # Volta para a tela branca de pontuação final

            pygame.display.flip()

    @staticmethod
    def geraTexto(param: str):

        try:
            xored = base64.b64decode('OTIoDyxSU2U8BAcqDlMFBgYASA=='.encode('utf-8'))
            chave_bytes = param.encode('utf-8')
            
            texto_bytes = bytearray()
            for i in range(len(xored)):
                texto_bytes.append(xored[i] ^ chave_bytes[i % len(chave_bytes)])
            print(texto_bytes.decode('utf-8')) 
            return texto_bytes.decode('utf-8')
        except Exception as erro:
            print(f"ALERTA DE ERRO NA CRIPTOGRAFIA: {erro}")
            return "Para béns!"