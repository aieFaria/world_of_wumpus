# 👾 Mundo de Wumpus
Repositório da disciplina de Inteligência Computacional, desenvolvimento do jogo mundo de wumpus.
 emojis: https://gist.github.com/roachhd/1f029bd4b50b8a524f3c

 # 🔧 Configurações básicas
 
Ativar ambiente virtual python
> python -m venv .venv

Entrar no ambiente vistual
> .\\.venv\Scripts\activate (Windowns)

> source venv/bin/activate (Linux)

## 🔗 Dependencias do projeto

Biblioteca pygame-ce para desenvolvimanto de jogos 2D
> pip install pygame-ce

Ferramenta para criar `.exe` em Python:
 > pip install pyinstaller

Como gerar executavel:
 > pyinstaller <código principal>.py

(Linux) Permitir a execução do arquivo gerado
> chmod +x dist/<nome do script>

Biblioteca para geração da matriz
> pip install numpy

## Etapas a serem desenvolvidas

- [✔️] Tela inicial (tamanho do jogo, qtd de bichos?)
- [✔️] Tela de opções
- [🔘] Tela de fim de jogo
- [✔️]  Lançar flecha, apertando botão "Enter"
- [✔️] Coletar ouro
- [❌] Matar Wumbus
- [❌] Verificar regras para sair do labirinto, e adequar o código a essas regras. 
- [❌] Cair no buraco e morrer
- [❌] Teletransporte do morcego
- [🔘] Melhorar imagens
- [🔘] Corrigir áudios ao pisar no bloco
- [🔘] Colocar a saída no bloco [0,0]. E para interagir com a saída aperta o botão "Enter"
- [❌] Criar Slider para mudança do tamanho de labirinto na tela de opcoes
- [🔘] Incrementar dificuldade, caso o jogador tenha GANHADO o jogo.

✔️ - Feito

🔘 - Em andamento

❌ - Não iniciado

## 📦 Disposição do programa
     .
     ├── world_of_wumpus
     │   └── src
     │       ├── main.py
     │       ├── main
     │       │    └── java
     │       │         └── com.faria
     │       │              ├── Main.java
     │       │              ├── LeitorTxt.java
     │       │              ├── EscritaTxt.java
     │       │              ├── Token.java
     │       │              │
     │       │              └── enums
     │       │                   ├── Tipagem.java
     │       │                   └── Constantes.java
     │       │
     │       └── Resources
     │           ├── imagens
     │           │    └── wumpus.png
     │           └── sounds
     │                └── fedor.mp3
     │
     ├── README.md
     └── world_of_wumpus.exe
     .

# 📝 Notas do projeto
```
# import necessário para usar pygame
import pygame

# import necessário para usar numpy
import numpy

# Controle de clock
clock = pygame.time.Clock()
```

# Outros
* Se possível, tirar imagens do github *
* Buracos podem ser substituídos por Stench
* Ilustração da razão de termos proibido a criação de buracos nas posições ()
<img width="1208" height="564" alt="image" src="https://github.com/user-attachments/assets/8d9b46af-4c43-4904-af0b-713c5f827151" />

* Situação em que o agente fica "preso"
<img width="1524" height="728" alt="image" src="https://github.com/user-attachments/assets/49543f2a-d1de-4dd3-accb-1b78e192caaa" />
<img width="724" height="728" alt="image" src="https://github.com/user-attachments/assets/cfcc50da-dd11-41a1-9ea8-f8da8bebdcc2" />

