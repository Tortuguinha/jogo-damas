from src.jogo import Jogo
from src.ui_console import UIConsole

if __name__ == "__main__":
    ui_console = UIConsole()
    jogo = Jogo(ui_console)
    jogo.jogar()