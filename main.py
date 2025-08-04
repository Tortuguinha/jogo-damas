from src.jogo import Jogo
from src.ui_pygame import UIPygame
from src.tabuleiro import Tabuleiro
from src.menu import mostrar_menu
from src.menu_regras import mostrar_menu_regras

if __name__ == "__main__":
    if mostrar_menu():
        regras = mostrar_menu_regras()
        tabuleiro = Tabuleiro()
        ui = UIPygame(tabuleiro)
        jogo = Jogo(ui, tabuleiro, regras)
        jogo.jogar()
