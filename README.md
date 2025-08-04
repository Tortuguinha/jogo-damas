# ♟️ Jogo de Damas em Python

Este é um projeto pessoal de um jogo de damas programado em Python. O objetivo é criar um jogo funcional com:

* Modo PvP local no terminal e interface gráfica com Pygame
* IA oponente simples (movimentos aleatórios)
* Menus gráficos para iniciar partidas, configurar regras e visualizar histórico

---

## 🚀 Funcionalidades implementadas

* Tabuleiro 8x8 com posicionamento inicial correto das peças
* Peças pretas e brancas (Peão e Dama) com regras completas de movimentação e captura
* Promoção automática a Dama ao atingir a última linha
* Captura obrigatória e múltiplas capturas (configuráveis via menu)
* Interface gráfica interativa usando Pygame para seleção de peças e movimentos
* Menus gráficos para:

  * Tela principal com opções Jogar, Histórico e Sair
  * Configuração customizável das regras do jogo
  * Exibição do histórico de partidas salvas em JSON
* IA básica que escolhe movimentos válidos aleatórios para o adversário (configurável)
* Interface alternativa para jogar via terminal (console)

---

## 🛠️ Tecnologias utilizadas

* **Python 3.x** — Linguagem principal do projeto
* **Pygame** — Biblioteca para interface gráfica, menus e interação via mouse
* **JSON** — Armazenamento do histórico de partidas
* **VS Code** — Ambiente de desenvolvimento utilizado
* **Git & GitHub** — Controle de versão e hospedagem do código

---

## 🧠 Conceitos aplicados

* Programação orientada a objetos (classes para peças, tabuleiro, jogo e UI)
* Modularização e organização do código em vários arquivos e pacotes
* Manipulação de eventos e interface gráfica com Pygame
* Lógica de jogo para movimentação, captura, promoção e fim de partida
* Entrada e saída de dados via terminal e GUI
* Salvamento e leitura de histórico de partidas com JSON
* Inteligência artificial básica para movimentos automáticos

---

## 📂 Como rodar o projeto

1. Clone este repositório:

   ```bash
   git clone https://github.com/Tortuguinha/jogo-damas.git
   cd jogo-damas
   ```

2. Instale as dependências (recomendo usar um ambiente virtual):

   ```bash
   pip install pygame
   ```

3. Execute o jogo:

   ```bash
   python main.py
   ```

4. Use o menu para iniciar uma partida, configurar regras e jogar.

---

## 📋 Estrutura do projeto

* `main.py` — Ponto de entrada que inicia a aplicação
* `src/` — Código fonte do jogo

  * `tabuleiro.py` — Implementação das regras e estado do tabuleiro
  * `jogo.py` — Controle da lógica do jogo e fluxo da partida
  * `ui_base.py` — Interface abstrata para UI
  * `ui_console.py` — UI para terminal
  * `ui_pygame.py` — UI gráfica com Pygame
  * `ia.py` — IA para movimentos automáticos
  * `menu.py`, `menu_regras.py`, `menu_historico.py` — Menus gráficos e histórico

