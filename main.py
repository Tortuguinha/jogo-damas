from src.jogo import Jogo
from src.ui_pygame import UIPygame
from src.tabuleiro import Tabuleiro

if __name__ == "__main__":
    tabuleiro = Tabuleiro()
    ui = UIPygame()
    jogo = Jogo(ui, tabuleiro)
    jogo.jogar()