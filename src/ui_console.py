from .tabuleiro import Tabuleiro
from .ui_base import UIBase

class UIConsole(UIBase):
    def __init__(self, tabuleiro):
        super().__init__(tabuleiro)

    def ler_movimento(self, turno):
        while True:
            try:
                movimento = input(f"Jogador {'Brancas' if turno == 'B' else 'Pretas'}, digite o movimento (ex: 2,3-3,4) ou 'sair' para terminar: ").strip().replace(" ", "")
                if movimento.lower() == 'sair':
                    return None, None

                origem_str, destino_str = movimento.split('-')
                origem = tuple(int(x) for x in origem_str.split(','))
                destino = tuple(int(x) for x in destino_str.split(','))

                if self.tabuleiro.posicao_valida(origem) and self.tabuleiro.posicao_valida(destino):
                    return origem, destino
                else:
                    self.mostrar_mensagem("Posição inválida! Use números entre 0 e 7 para linha e coluna.")
            except ValueError:
                self.mostrar_mensagem("Entrada inválida! Use o formato: linha,coluna-linha,coluna (ex: 2,3-3,4)")

    def ler_movimento_continuacao(self, origem):
        while True:
            try:
                movimento = input(f"Você pode capturar novamente com a peça em {origem}. Digite o próximo destino (ex: 1,6) ou 'sair' para terminar: ").strip()
                if movimento.lower() == 'sair':
                    return None

                destino = tuple(int(x) for x in movimento.split(','))

                if self.tabuleiro.posicao_valida(destino):
                    return destino
                else:
                    self.mostrar_mensagem("Posição inválida! Use números entre 0 e 7 para linha e coluna.")
            except ValueError:
                self.mostrar_mensagem("Entrada inválida! Use o formato: linha,coluna (ex: 1,6)")

    def mostrar_mensagem(self, mensagem):
        print(mensagem)