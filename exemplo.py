import pygame
import random
import sys

# 1. Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Esquiva")

# Cores (RGB)
AZUL = (50, 150, 255)
VERMELHO = (255, 50, 50)
PRETO = (0, 0, 0)

# Configurações do Jogador
jogador_tam = 50
jogador_x = LARGURA // 2
jogador_y = ALTURA - jogador_tam - 10
velocidade_jogador = 7

# Configurações do Inimigo
inimigo_tam = 50
inimigo_x = random.randint(0, LARGURA - inimigo_tam)
inimigo_y = -inimigo_tam
velocidade_inimigo = 5

# Controle de FPS (Frames por segundo)
clock = pygame.time.Clock()

# Loop Principal do Jogo
rodando = True
while rodando:
    # 2. Gerenciar Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 3. Movimentação do Jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jogador_x > 0:
        jogador_x -= velocidade_jogador
    if teclas[pygame.K_RIGHT] and jogador_x < LARGURA - jogador_tam:
        jogador_x += velocidade_jogador

    # 4. Movimentação do Inimigo
    inimigo_y += velocidade_inimigo
    if inimigo_y > ALTURA:
        inimigo_y = -inimigo_tam
        inimigo_x = random.randint(0, LARGURA - inimigo_tam)
        velocidade_inimigo += 0.2  # Aumenta a dificuldade

    # 5. Detecção de Colisão
    jogador_rect = pygame.Rect(jogador_x, jogador_y, jogador_tam, jogador_tam)
    inimigo_rect = pygame.Rect(inimigo_x, inimigo_y, inimigo_tam, inimigo_tam)

    if jogador_rect.colliderect(inimigo_rect):
        print("Game Over!")
        rodando = False

    # 6. Desenhar na Tela
    tela.fill(PRETO)  # Limpa a tela com fundo preto
    
    # Desenha o jogador e o inimigo
    pygame.draw.rect(tela, AZUL, jogador_rect)
    pygame.draw.rect(tela, VERMELHO, inimigo_rect)

    # Atualiza a tela
    pygame.display.flip()
    
    # Define a taxa de quadros (60 FPS)
    clock.tick(60)

pygame.quit()