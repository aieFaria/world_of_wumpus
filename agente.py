import time
import pygame
from labirinto import Labirinto

class Agente:
    # Atributos de classe
    delayMove = 100

    def __init__(self, id, labirinto: Labirinto):
        # Atributo de instância do agente
        self.id = id
        self.labirinto = labirinto
        self.ponteiro = 0
        self.finalizado = False
        self.visitados = set()
        self.pilha_caminho = []
        self.historico = [] # Inicializa vazio

    """
    Este método precisa retornar quais comando executar para mover o jogador baseado na lógica
    do labirinto visível.

    Coloque na pilha 'historico' o movimento que deseja realizar duas vezes: uma para girar e outra para mover
    Exemplo: "direita", "direita" = jogador move para direita
    """
    def mapear(self, posicaoXY, direcao_atual):

        x, y = posicaoXY
        self.visitados.add((x, y))
        #print(self.visitados)
        bloco = self.labirinto.blocos[x][y]
        tamanhoLabirinto = 64

        #print("tam: ",len(self.visitados))
        # if( posicaoXY == [0, 0] and len(self.visitados) >= tamanhoLabirinto ):
        #     # Executar comando para sair do labirinto
        #     print("Labirinto concluído")
        #     return[]
        
        # Condicional que verifca sempre se o labirinto foi completo com sucesso
        # 40 é o tamanho dos visitados quando labirinto está completo
        #print( len(self.visitados) )
        #if( len(self.visitados) >= tamanhoLabirinto ):
            #print(self.caminhoCurto(posicaoXY, [0,0]))
            # Substituir pela geração de um caminho que desvie dos perigos
            #return self.caminhoCurto(posicaoXY, [0,0])

        # Condicional para verifcação de perigos
        if ( bloco.hasBreeze() or bloco.hasStench() or bloco.hasFlappings() ):
      
            return self.saida(posicaoXY, direcao_atual)

        return self.buscar_vizinho_seguro(posicaoXY, direcao_atual)

    def buscar_vizinho_seguro(self, posicaoXY, direcao_atual):
        x, y = posicaoXY

        # Sugestão do Gemini criar um array que contém as possiveis direções de movimento
        direcoes = [
            (x + 1, y, "frente"), (x - 1, y, "costas"),  
            (x, y + 1, "direita"), (x, y - 1, "esquerda")
        ]

        for vx, vy, direcao in direcoes:
            if 0 <= vx < 8 and 0 <= vy < 8:
                # Se o bloco é não visivel e não foi visitado
                if( not self.foi_visitado(vx, vy) ):
                    self.pilha_caminho.append((x, y))

                    if direcao_atual == direcao:
                        return [direcao] # Já está virado, só precisa dar o passo
                    else:
                        return [direcao, direcao]
                
        # Se não achou nenhum vizinho novo e seguro, volta uma casa
        return self.saida(posicaoXY, direcao_atual)

    def saida(self, posicaoXY, direcao_atual):
        # Verifica se a pilha do caminho tem elementos, evita NoneException
        if self.pilha_caminho:
            destino_volta = self.pilha_caminho.pop()
            return self.caminhoCurto(posicaoXY, destino_volta, direcao_atual)
        self.finalizado = True
        return []

    """
    Método que simplemente retorna caminho mais curto entre a posição atual e o destino definido
    """
    def caminhoCurto(self, atual, destino, direcao_atual):
        diferencialX = destino[0] - atual[0]
        diferencialY = destino[1] - atual[1]
        
        if diferencialX >= 1: comando = "frente"
        elif diferencialY >= 1: comando = "direita"
        elif diferencialY < 0: comando = "esquerda"
        elif diferencialX < 0: comando = "costas"
        else: return []

        if direcao_atual == comando:
            return [comando]
        else:
            return [comando, comando]


    def foi_visitado(self, x, y):
        return (x, y) in self.visitados

    def executar(self, main):

        # Variável que indica que o jogo foi finalizado
        terminar = False
        if not self.historico:
            self.historico.extend(self.mapear([main.player_x, main.player_y], main.direcao))
            #print(self.historico)

            if not self.historico:
                return
  
        if len(self.historico) > 0:
            
            pygame.time.delay(self.delayMove)
            self.mover(main, self.historico.pop(0))
            # print(self.historico)
        

    """
    Método auxiliar para executar o movimento do personagem
    """
    def mover(self, main, direcao):
        if main.direcao == direcao:
            match direcao:
                case "direita":
                    if main.player_y < 7:
                        main.player_y += 1
                case "esquerda":
                    if main.player_y > 0:
                        main.player_y -= 1
                case "costas":
                    if main.player_x > 0:
                        main.player_x -= 1
                case "frente":
                    if main.player_x < 7:
                        main.player_x += 1
            
            self.ponteiro += 1
        else:
            main.direcao = direcao  
        

            
        
    