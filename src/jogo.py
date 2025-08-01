from .tabuleiro import Tabuleiro, Peao, Dama
from .ui_base import UIBase  # Importar a interface base

class Jogo:
    def __init__(self, ui: UIBase, tabuleiro=None):
        if tabuleiro is None:
            self.tabuleiro = Tabuleiro()
        else:
            self.tabuleiro = tabuleiro
        self.turno = 'B'
        self.ui = ui
        # Sincroniza o tabuleiro da UI com o do jogo
        self.ui.tabuleiro = self.tabuleiro

    def alternar_turno(self):
        self.turno = 'P' if self.turno == 'B' else 'B'

    def validar_movimento(self, origem, destino):
        peca = self.tabuleiro.obter_peca(origem)
        if not peca:
            self.ui.mostrar_mensagem("Não há peça na posição de origem.")
            return False
        if peca.cor != self.turno:
            self.ui.mostrar_mensagem("Você só pode mover suas próprias peças.")
            return False
        if not self.tabuleiro.movimento_valido(origem, destino):
            self.ui.mostrar_mensagem("Movimento inválido para essa peça.")
            return False
        return True

    def mover_peca(self, origem, destino):
        peca = self.tabuleiro.obter_peca(origem)
        if not peca:
            self.ui.mostrar_mensagem("Não há peça na origem")
            return False, False  # Não moveu, sem promoção

        self.tabuleiro.mover_peca(origem, destino)

        linha_d, _ = destino
        promovido = False
        if isinstance(peca, Peao):
            if (peca.cor == 'B' and linha_d == 0) or (peca.cor == 'P' and linha_d == self.tabuleiro.tamanho -1):
                self.ui.mostrar_mensagem(f"Peça {peca.cor} promovida a Dama!")
                promovido = True

        return True, promovido

    def verificar_captura_disponivel(self, pos):
        peca = self.tabuleiro.obter_peca(pos)
        if not peca:
            return False

        movimentos = peca.movimentos_validos(pos, self.tabuleiro)
        for mov in movimentos:
            if abs(mov[0] - pos[0]) > 1:
                return True
        return False

    def fim_de_jogo(self, cor):
        for linha in range(self.tabuleiro.tamanho):
            for coluna in range(self.tabuleiro.tamanho):
                peca = self.tabuleiro.obter_peca((linha, coluna))
                if peca and peca.cor == cor:
                    movimentos = peca.movimentos_validos((linha, coluna), self.tabuleiro)
                    if movimentos:
                        return False
        return True

    def jogar(self):
        while True:
            self.tabuleiro.mostrar()
            origem, destino = self.ui.ler_movimento(self.turno)

            if origem is None or destino is None:
                self.ui.mostrar_mensagem("Jogo encerrado pelo usuário.")
                break

            if self.validar_movimento(origem, destino):
                moveu, promovido = self.mover_peca(origem, destino)

                linha_o, col_o = origem
                linha_d, col_d = destino

                # Só continua a captura múltipla se NÃO houve promoção
                if not promovido and abs(linha_d - linha_o) == 2:
                    nova_origem = destino

                    while self.verificar_captura_disponivel(nova_origem):
                        self.tabuleiro.mostrar()
                        self.ui.mostrar_mensagem("Você pode capturar outra peça!")
                        novo_destino = self.ui.ler_movimento_continuacao(nova_origem)

                        if novo_destino is None:
                            self.ui.mostrar_mensagem("Jogo encerrado pelo usuário.")
                            return

                        if self.validar_movimento(nova_origem, novo_destino):
                            self.mover_peca(nova_origem, novo_destino)
                            nova_origem = novo_destino
                        else:
                            self.ui.mostrar_mensagem("Movimento inválido na sequência de capturas.")
                            break

                self.alternar_turno()
                if self.fim_de_jogo(self.turno):
                    self.ui.mostrar_mensagem(f"\nJogador {'Brancas' if self.turno == 'B' else 'Pretas'} não tem mais movimentos.")
                    self.ui.mostrar_mensagem(f"Jogador {'Pretas' if self.turno == 'B' else 'Brancas'} venceu!")
                    break
            else:
                self.ui.mostrar_mensagem("Movimento inválido, tente novamente.")