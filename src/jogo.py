from .tabuleiro import Tabuleiro, Peao, Dama
from .ui_base import UIBase

class Jogo:
    def __init__(self, ui: UIBase, tabuleiro=None, regras=None):
        self.tabuleiro = tabuleiro if tabuleiro else Tabuleiro()
        self.turno = 'B'
        self.ui = ui
        self.ui.tabuleiro = self.tabuleiro  # UI pode validar posições

        regras = regras or {}
        self.captura_obrigatoria = regras.get("captura_obrigatoria", True)
        self.dama_multi_captura = regras.get("dama_multi_captura", True)
        self.multiplas_capturas = regras.get("multiplas_capturas", True)

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

        # Captura obrigatória: se há captura para o turno, movimento deve ser captura
        if self.captura_obrigatoria and self.tabuleiro.existe_captura(self.turno):
            linha_o, col_o = origem
            linha_d, col_d = destino
            if abs(linha_d - linha_o) <= 1:  # movimento simples, não captura
                self.ui.mostrar_mensagem("Captura obrigatória! Você deve capturar uma peça.")
                return False

        if not self.tabuleiro.movimento_valido(origem, destino):
            self.ui.mostrar_mensagem("Movimento inválido para essa peça.")
            return False
        return True

    def verificar_captura_disponivel(self, pos):
        peca = self.tabuleiro.obter_peca(pos)
        if not peca:
            return False

        for mov in peca.movimentos_validos(pos, self.tabuleiro):
            if abs(mov[0] - pos[0]) > 1:
                return True
        return False

    def fim_de_jogo(self, cor):
        for linha in range(self.tabuleiro.tamanho):
            for coluna in range(self.tabuleiro.tamanho):
                peca = self.tabuleiro.obter_peca((linha, coluna))
                if peca and peca.cor == cor:
                    if peca.movimentos_validos((linha, coluna), self.tabuleiro):
                        return False
        return True

    def jogar(self):
        while True:
            self.tabuleiro.mostrar()
            origem, destino = self.ui.ler_movimento(self.turno)

            if origem is None or destino is None:
                self.ui.mostrar_mensagem("Jogo encerrado pelo usuário.")
                break

            if not self.validar_movimento(origem, destino):
                continue

            linha_o, col_o = origem
            linha_d, col_d = destino

            promovido = self.tabuleiro.mover_peca(origem, destino)
            if promovido:
                self.ui.mostrar_mensagem(f"Peça {self.turno} promovida a Dama!")

            # Verifica se houve captura (2 ou mais casas de distância)
            if abs(linha_d - linha_o) > 1:
                nova_origem = destino
                peca = self.tabuleiro.obter_peca(nova_origem)

                if self.multiplas_capturas:
                    # Se for Peao, ou Dama e regra dama_multi_captura ativada, pode continuar capturando
                    if isinstance(peca, Peao) or (self.dama_multi_captura and isinstance(peca, Dama)):
                        while not promovido and self.verificar_captura_disponivel(nova_origem):
                            self.tabuleiro.mostrar()
                            self.ui.mostrar_mensagem("Você pode capturar outra peça!")
                            novo_destino = self.ui.ler_movimento_continuacao(nova_origem)

                            if novo_destino is None:
                                self.ui.mostrar_mensagem("Jogo encerrado pelo usuário.")
                                return

                            if self.validar_movimento(nova_origem, novo_destino):
                                promovido = self.tabuleiro.mover_peca(nova_origem, novo_destino)
                                nova_origem = novo_destino
                                if promovido:
                                    self.ui.mostrar_mensagem(f"Peça {self.turno} promovida a Dama!")
                                    break
                            else:
                                self.ui.mostrar_mensagem("Movimento inválido na sequência de capturas.")
                                break
                else:
                    # múltiplas capturas desativadas, não permite sequência
                    pass

            self.alternar_turno()
            if self.fim_de_jogo(self.turno):
                self.ui.mostrar_mensagem(f"\nJogador {'Brancas' if self.turno == 'B' else 'Pretas'} não tem mais movimentos.")
                self.ui.mostrar_mensagem(f"Jogador {'Pretas' if self.turno == 'B' else 'Brancas'} venceu!")
                break