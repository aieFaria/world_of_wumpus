import pygame
"""

pygame.init()

# Configurações
tela = pygame.display.set_mode((400, 200))
fonte = pygame.font.Font(None, 32)
caixa = pygame.Rect(50, 50, 300, 40)
cor_ativa = pygame.Color('lightskyblue3')
cor_passiva = pygame.Color('chartreuse4')
cor = cor_passiva
texto = ''
ativo = False

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ativa a caixa se clicar nela
            if caixa.collidepoint(event.pos):
                ativo = True
                cor = cor_ativa
            else:
                ativo = False
                cor = cor_passiva
        if event.type == pygame.KEYDOWN:
            if ativo:
                if event.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                else:
                    texto += event.unicode
    
    tela.fill((255, 255, 255))
    
    # Desenha caixa e texto
    pygame.draw.rect(tela, cor, caixa, 2)
    superficie_texto = fonte.render(texto, True, (0, 0, 0))
    tela.blit(superficie_texto, (caixa.x + 5, caixa.y + 5))
    
    caixa.w = max(100, superficie_texto.get_width() + 10)
    pygame.display.flip()

pygame.quit()


"""

# Inicialização
pygame.init()
tela = pygame.display.set_mode((300, 200))
fonte = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

# Estado da caixa
caixa_rect = pygame.Rect(50, 50, 30, 30)
checado = False

# Loop Principal
rodando = True
while rodando:
    tela.fill((255, 255, 255)) # Fundo branco

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        
        # Detecção do clique
        if event.type == pygame.MOUSEBUTTONDOWN:
            if caixa_rect.collidepoint(event.pos):
                checado = not checado
                print(f"Marcado: {checado}")

    # Desenhar Caixa
    cor_caixa = (0, 255, 0) if checado else (200, 200, 200)
    pygame.draw.rect(tela, cor_caixa, caixa_rect)
    pygame.draw.rect(tela, (0, 0, 0), caixa_rect, 2) # Borda

    # Texto opcional
    texto = fonte.render("Selecionar", True, (0, 0, 0))
    tela.blit(texto, (90, 55))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

#"""