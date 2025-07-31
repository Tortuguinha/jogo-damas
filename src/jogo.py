from .tabuleiro import Tabuleiro, Peao, Dama
from .ui import ler_movimento, ler_movimento_continuacao

class Jogo:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.turno = 'B'  # 'B' para brancas, 'P' para pretas

    def alternar_turno(self):
        self.turno = 'P' if self.turno == 'B' else 'B'

    def validar_movimento(self, origem, destino):
        peca = self.tabuleiro.obter_peca(origem)
        if not peca:
            print("Não há peça na posição de origem.")
            return False
        if peca.cor != self.turno:
            print("Você só pode mover suas próprias peças.")
            return False
        if not self.tabuleiro.movimento_valido(origem, destino):
            print("Movimento inválido para essa peça.")
            return False
        return True

    def mover_peca(self, origem, destino):
        peca = self.tabuleiro.obter_peca(origem)
        if not peca:
            print("Não há peça na origem")
            return False

        self.tabuleiro.mover_peca(origem, destino)

        # Promoção é tratada dentro do Tabuleiro.mover_peca, mas se quiser imprimir aqui:
        linha_d, _ = destino
        if isinstance(peca, Peao):
            if (peca.cor == 'B' and linha_d == 0) or (peca.cor == 'P' and linha_d == self.tabuleiro.tamanho -1):
                print(f"Peça {peca.cor} promovida a Dama!")

        return True

    def verificar_captura_disponivel(self, pos):
        peca = self.tabuleiro.obter_peca(pos)
        if not peca:
            return False

        movimentos = peca.movimentos_validos(pos, self.tabuleiro)
        # Captura é quando o deslocamento é > 1 na linha (pulo)
        for mov in movimentos:
            if abs(mov[0] - pos[0]) > 1:
                return True
        return False

    def jogar(self):
        while True:
            self.tabuleiro.mostrar()
            origem, destino = ler_movimento(self.turno)

            if origem is None or destino is None:
                print("Jogo encerrado pelo usuário.")
                break

            if self.validar_movimento(origem, destino):
                self.mover_peca(origem, destino)

                linha_o, col_o = origem
                linha_d, col_d = destino
                if abs(linha_d - linha_o) == 2:  # movimento de captura
                    nova_origem = destino

                    while self.verificar_captura_disponivel(nova_origem):
                        self.tabuleiro.mostrar()
                        print("Você pode capturar outra peça!")
                        novo_destino = ler_movimento_continuacao(nova_origem)

                        if novo_destino is None:
                            print("Jogo encerrado pelo usuário.")
                            return

                        if self.validar_movimento(nova_origem, novo_destino):
                            self.mover_peca(nova_origem, novo_destino)
                            nova_origem = novo_destino
                        else:
                            print("Movimento inválido na sequência de capturas.")
                            break

                self.alternar_turno()

            else:
                print("Movimento inválido, tente novamente.")