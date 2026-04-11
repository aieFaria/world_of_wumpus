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
