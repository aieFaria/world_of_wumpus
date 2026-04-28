import time
import pygame
from labirinto import Labirinto
from collections import deque

class Agente:
    # Atributos de classe
    delayMove = 300 

    def __init__(self, id):
        self.id = id
        self.ultimo_move_time = pygame.time.get_ticks()
        self.finalizado = False
        self.perigosos = set() # Set de coordenadas (x, y) que o BFS deve evitar
        self.pilha_caminho = [] # Lista de destinos seguros ("O") para exploração
        
        self.atual = None
        self.anterior = None
        self.tentou_movimento = False
        self.cont_bloqueio = 0
        self.tamanho_lab = 99 
        self.tamanho_real_descoberto = False

        # Metas e Descobertas (Valores padrão iniciais)
        self.quantidades_alvo = {
            "morcegos": 2, 
            "ouro": 3, 
            "wumpus": 2, 
            "flecha": 2, 
            "buracos": 4
        }
        self.quantidades_encontradas = {
            "morcegos": 0, 
            "ouro": 0, 
            "wumpus": 0, 
            "flecha": 0, 
            "buracos": 0
        }

        self.visitados = set()
        self.labirinto = [] # Memória global (Matriz de objetos BlocoI)
        self.ctrl = {"direcao": "frente", "localizacao": (0, 0)}
        self.leituraLab = {} 

        # Atributos para Inferência e Combate
        self.pistas_fedor = set()
        self.casas_limpas = set()
        self.wumpus_confirmado = None
        self.wumpus_morto = False

    def recalcular_metas(self):
        """ Ajusta as quantidades alvo com base no tamanho real descoberto do labirinto """
        escala = self.tamanho_lab / 6.0
        self.quantidades_alvo = {
            "morcegos": max(1, int(2 * escala)),
            "ouro": max(1, int(3 * escala)),
            "wumpus": max(1, int(2 * escala)),
            "flecha": max(1, int(2 * escala)),
            "buracos": max(1, int(4 * escala))
        }
        print(f"Metas recalculadas para tamanho {self.tamanho_lab}: {self.quantidades_alvo}")

    def executar(self):
        tempo_atual = pygame.time.get_ticks()
        x, y = self.ctrl.get("localizacao", (0, 0))

        if not self.leituraLab:
            self.iniciar()
            return

        pos_vinda_lab = self.leituraLab.get("bloco")

        if self.atual is None:
            self.atual = pos_vinda_lab
            self.anterior = pos_vinda_lab

        # Condição de encerramento: Pontuação alta ou atingiu a meta de ouros inferida
        if (self.leituraLab.get("pontuacao", 0) >= 3000):
            self.finalizado = True
            
        self.tell(self.aux_convertDictBloco(self.leituraLab))

        if tempo_atual - self.ultimo_move_time > self.delayMove:
            self.anterior = self.atual
            self.atual = pos_vinda_lab
            
            if self.mudando():
                self.visitados.add(self.atual)
                self.cont_bloqueio = 0
                self.tentou_movimento = False
                
                if self.pilha_caminho and self.atual == self.pilha_caminho[-1]:
                    self.pilha_caminho.pop()
                
                if not self.finalizado:
                    self.ask()
                self.otimizarPilha()
            
            elif self.tentou_movimento:
                self.cont_bloqueio += 1
                if self.cont_bloqueio >= 3:
                    if self.pilha_caminho:
                        destino_bloqueado = self.pilha_caminho[-1]
                        
                        bx, by = destino_bloqueado
                        if bx < len(self.labirinto) and by < len(self.labirinto[bx]):
                            self.labirinto[bx][by].setPerigo("P")
                        
                        self.perigosos.add(destino_bloqueado)
                        self.pilha_caminho.pop()
                        
                        # Atualiza tamanho do labirinto e recalcula metas
                        novo_tamanho = 99
                        if destino_bloqueado[0] > x: novo_tamanho = destino_bloqueado[0]
                        if destino_bloqueado[1] > y: novo_tamanho = destino_bloqueado[1]
                        
                        if novo_tamanho < self.tamanho_lab:
                            self.tamanho_lab = novo_tamanho
                            self.tamanho_real_descoberto = True
                            self.recalcular_metas()
                    
                    self.cont_bloqueio = 0
                    self.tentou_movimento = False
                    self.otimizarPilha()
                    self.ask()

            # LÓGICA DE COMBATE: Prioridade se soubermos onde o Wumpus está e tivermos flechas
            # (IMPORTANTE) Lógica completamente quebrada, precisa modificar
            qtd_flechas = self.leituraLab.get("qtd_flechas", 0)
            if self.wumpus_confirmado and qtd_flechas > 0 and not self.wumpus_morto:
                self.atacar_wumpus(x, y)
            elif not self.finalizado:
                if self.pilha_caminho:
                    destino = self.pilha_caminho[-1] 
                    if (x, y) != destino:
                        self.movimentacao_segura(x, y, destino)
                    else:
                        self.pilha_caminho.pop()
                        self.otimizarPilha()
                else:
                    self.ask()
            else:
                # Caminho de volta para casa
                if (x, y) != (0, 0):
                    self.movimentacao_segura(x, y, (0, 0))
                else:
                    self.finalizar_jogo()

            self.ultimo_move_time = tempo_atual

    # (IMPORTANTE) Não funciona corretamente, mas possivelmente a lógica pode ser aproveitada
    def atacar_wumpus(self, x, y):
        wx, wy = self.wumpus_confirmado
        
        # Casas visitadas que oferecem linha de tiro (mesma linha ou coluna)
        opcoes_tiro = [v for v in self.visitados if v[0] == wx or v[1] == wy]
        
        if not opcoes_tiro:
            # Se não houver linha de tiro em locais visitados, tenta se aproximar
            self.movimentacao_segura(x, y, (wx, wy))
            return

        # Escolhe o ponto de disparo mais próximo
        alvo_disparo = min(opcoes_tiro, key=lambda p: abs(p[0]-x) + abs(p[1]-y))

        if (x, y) != alvo_disparo:
            self.movimentacao_segura(x, y, alvo_disparo)
        else:
            # Estamos na linha de tiro. Determinar direção necessária.
            direcao_alvo = ""
            tecla_olhar = None
            
            if wx > x: direcao_alvo, tecla_olhar = "frente", pygame.K_DOWN
            elif wx < x: direcao_alvo, tecla_olhar = "costa", pygame.K_UP
            elif wy > y: direcao_alvo, tecla_olhar = "direita", pygame.K_RIGHT
            elif wy < y: direcao_alvo, tecla_olhar = "esquerda", pygame.K_LEFT
            
            if self.ctrl["direcao"] != direcao_alvo:
                # Ciclo 1: Vira o personagem
                print(f"Alinhando para disparar em {self.wumpus_confirmado}...")
                self.movimentar(tecla_olhar)
            else:
                # Ciclo 2: Dispara (já está virado)
                print(f"DISPARANDO CONTRA WUMPUS!")
                evento = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN, 'mod': 0, 'is_agent': True})
                pygame.event.post(evento)
                
                self.wumpus_morto = True
                self.quantidades_encontradas["wumpus"] += 1
                
                # O local do Wumpus agora pode ser considerado passável
                if self.wumpus_confirmado in self.perigosos:
                    self.perigosos.remove(self.wumpus_confirmado)

    def mudando(self):
        return self.atual != self.anterior

    def otimizarPilha(self):

        nova_pilha = []
        vistos_na_pilha = set()

        for coord in self.pilha_caminho:
            if (coord not in self.visitados and 
                coord not in self.perigosos and 
                coord[0] < self.tamanho_lab and coord[1] < self.tamanho_lab and
                coord not in vistos_na_pilha):
                nova_pilha.append(coord)
                vistos_na_pilha.add(coord)
        self.pilha_caminho = nova_pilha

    # (IMPORTANTE) Não funciona corretamente
    def inferir_wumpus(self):
        if self.wumpus_confirmado or not self.pistas_fedor:
            return
        possibilidades = None
        for px, py in self.pistas_fedor:
            viz_pista = set()
            for nx, ny in [(px-1, py), (px+1, py), (px, py-1), (px, py+1)]:
                if 0 <= nx < self.tamanho_lab and 0 <= ny < self.tamanho_lab:
                    e_segura = False
                    for lx, ly in [(nx-1, ny), (nx+1, ny), (nx, ny-1), (nx, ny+1)]:
                        if (lx, ly) in self.casas_limpas:
                            e_segura = True; break
                    if not e_segura: viz_pista.add((nx, ny))
            if possibilidades is None: possibilidades = viz_pista
            else: possibilidades &= viz_pista
        if possibilidades and len(possibilidades) == 1:
            self.wumpus_confirmado = list(possibilidades)[0]
            print(f"WUMPUS LOCALIZADO EM: {self.wumpus_confirmado}")
            self.perigosos.add(self.wumpus_confirmado)

    # (IMPORTANTE) Está funcionando como esperado mas necessita de atenção
    #              pois o código esta ilegível
    def ask(self):
        x, y = self.ctrl.get("localizacao")
        atributos = self.leituraLab.get("atributos", [])
        
        if not atributos: 
            self.casas_limpas.add((x, y))
        if "stench" in atributos: 
            self.pistas_fedor.add((x, y))

        self.inferir_wumpus()

        for vx, vy in list(self.visitados):
            if vx < len(self.labirinto) and vy < len(self.labirinto[vx]):
                if not self.labirinto[vx][vy].atributos:
                    for nx, ny in [(vx-1, vy), (vx+1, vy), (vx, vy-1), (vx, vy+1)]:
                        if 0 <= nx < self.tamanho_lab and 0 <= ny < self.tamanho_lab:
                            if nx >= len(self.labirinto) or ny >= len(self.labirinto[nx]):
                                self.expandir_memoria(nx, ny)

        self.classificar_mapa()
        
        novos_destinos = []
        for linha in self.labirinto:
            for bloco in linha:
                if bloco.perigo == "O" and bloco.posicao not in self.visitados:
                    if bloco.posicao not in self.pilha_caminho:
                        novos_destinos.append(bloco.posicao)
        
        for destino in novos_destinos:
            self.pilha_caminho.append(destino)

    # (IMPORTANTE) Segue o mesmo problema da ask, está ilegivel
    def classificar_mapa(self):

        seguros = set([(0, 0)])

        for vx, vy in self.visitados:
            if vx < len(self.labirinto) and vy < len(self.labirinto[vx]):
                if not self.labirinto[vx][vy].atributos:
                    for nx, ny in [(vx-1, vy), (vx+1, vy), (vx, vy-1), (vx, vy+1)]:
                        if 0 <= nx < self.tamanho_lab and 0 <= ny < self.tamanho_lab:
                            seguros.add((nx, ny))

        for x in range(len(self.labirinto)):
            for y in range(len(self.labirinto[x])):
                bloco = self.labirinto[x][y]
                pos = bloco.posicao
                
                if bloco.perigo == "P":
                    self.perigosos.add(pos)
                    continue

                if pos in seguros or pos in self.visitados:
                    bloco.setPerigo("O")
                    if pos in self.perigosos and pos != self.wumpus_confirmado:
                        self.perigosos.remove(pos)
                else:
                    eh_duvida = False
                    for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                        if (nx, ny) in self.visitados:
                            if self.labirinto[nx][ny].atributos:
                                eh_duvida = True; break
                    
                    if eh_duvida or pos == self.wumpus_confirmado:
                        bloco.setPerigo("X" if pos == self.wumpus_confirmado else "?")
                        self.perigosos.add(pos)
                    else:
                        bloco.setPerigo("?")
                        self.perigosos.add(pos)

    def expandir_memoria(self, x, y):

        while len(self.labirinto) <= x:
            self.labirinto.append([])
        for i in range(len(self.labirinto)):
            while len(self.labirinto[i]) <= y:
                nova_pos = (i, len(self.labirinto[i]))
                self.labirinto[i].append(BlocoI(nova_pos, [], False, False, False, False, False, "?"))

    def movimentacao_segura(self, x, y, bloco_alvo):

        if (x, y) == bloco_alvo:
            return

        # Variaveis de controle para Busca em Largura
        fila_busca = deque( [( (x, y), [] )] )
        visitados_bfs = set([(x, y)])
        
        while fila_busca:
            (curr_x, curr_y), path = fila_busca.popleft()
            
            if (curr_x, curr_y) == bloco_alvo:
                if path:
                    proximo_passo, tecla = path[0]
                    self.movimentar(tecla)
                return

            # Possíveis movimentos
            vizinhos = [
                ((curr_x + 1, curr_y), pygame.K_DOWN),
                ((curr_x - 1, curr_y), pygame.K_UP),
                ((curr_x, curr_y + 1), pygame.K_RIGHT),
                ((curr_x, curr_y - 1), pygame.K_LEFT)
            ]

            for pos_prox, prox_tecla in vizinhos:
                px, py = pos_prox

                if ( (0 <= px < self.tamanho_lab) 
                    and (0 <= py < self.tamanho_lab) 
                    and (pos_prox not in self.perigosos) 
                    and (pos_prox not in visitados_bfs) ):
                    
                    visitados_bfs.add(pos_prox)
                    fila_busca.append((pos_prox, path + [(pos_prox, prox_tecla)]))


    def movimentar(self, tecla):
        direcoes = {
            pygame.K_DOWN: "frente", 
            pygame.K_UP: "costa", 
            pygame.K_RIGHT: "direita", 
            pygame.K_LEFT: "esquerda"
        }

        self.ctrl["direcao"] = direcoes.get(tecla, self.ctrl["direcao"])

        evento = pygame.event.Event(pygame.KEYDOWN, {
            'key': tecla, 
            'mod': 0, 
            'is_agent': True
            })

        pygame.event.post(evento)
        self.tentou_movimento = True

    def finalizar_jogo(self):
        evento = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN, 'mod': 0, 'is_agent': True})
        pygame.event.post(evento)

    def iniciar(self):
        bloco_init = BlocoI((0, 0), [], False, False, False, False, False, "O")
        self.tell(bloco_init)
        self.visitados.add((0, 0))
        self.ask()
        
    def tell(self, bloco):
        pos = self.leituraLab.get('bloco')
        if pos: self.ctrl["localizacao"] = pos
        x, y = bloco.posicao
        
        # Contabilizar novos elementos encontrados
        # (IMPORTANTE) Corrigir essa contagem de elementos
        if (x, y) not in self.visitados:
            if bloco.hasGold: self.quantidades_encontradas["ouro"] += 1
            if bloco.hasBats: self.quantidades_encontradas["morcegos"] += 1
            if bloco.hasPit: self.quantidades_encontradas["buracos"] += 1
            if bloco.hasArrow: self.quantidades_encontradas["flecha"] += 1

        self.expandir_memoria(x, y)
        self.labirinto[x][y] = bloco

    def aux_convertDictBloco(self, d):
        return BlocoI(d.get('bloco', (0, 0)), 
                      d.get('atributos', []), 
                      d.get('hasPit'), 
                      d.get('hasWumpus'), 
                      d.get('hasBats'), 
                      d.get('hasArrow'), 
                      d.get('hasGold'), 
                      "O")

class BlocoI: 
    def __init__(self, posicao, atributos, hasPit, hasWumpus, hasBats, hasArrow, hasGold, ava="?"):
        self.posicao = posicao
        self.atributos = atributos
        self.hasPit = hasPit
        self.hasWumpus = hasWumpus
        self.hasBats = hasBats
        self.hasArrow = hasArrow
        self.hasGold = hasGold
        self.perigo = ava 
    def setPerigo(self, perigo):
        self.perigo = perigo
    def __eq__(self, other):
        return self.posicao == other.posicao if isinstance(other, BlocoI) else False
    def __repr__(self):
        return f"\n{self.posicao}.{self.perigo}"