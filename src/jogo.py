from tabuleiro import Tabuleiro
from ui import ler_movimento, ler_movimento_continuacao, validar_posicao

class Jogo:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.turno = 'B'  # 'B' para brancas, 'P' para pretas

    def alternar_turno(self):
        self.turno = 'P' if self.turno == 'B' else 'B'

    def validar_movimento(self, origem, destino):
        linha_o, col_o = origem
        linha_d, col_d = destino

        pecas = self.tabuleiro.tabuleiro
        p_origem = pecas[linha_o][col_o]
        p_destino = pecas[linha_d][col_d]

        if p_origem is None:
            print("Não há peça na posição de origem.")
            return False

        if self.turno == 'B' and p_origem not in ['B', 'BD']:
            print("Você só pode mover suas próprias peças.")
            return False
        elif self.turno == 'P' and p_origem not in ['P', 'PD']:
            print("Você só pode mover suas próprias peças.")
            return False


        if p_destino is not None:
            print("Posição de destino já está ocupada.")
            return False

        direcao = -1 if self.turno == 'B' else 1
        delta_linha = linha_d - linha_o
        delta_coluna = col_d - col_o

        # Movimento simples
        if delta_linha == direcao and abs(delta_coluna) == 1:
            return True

        # Captura
        if delta_linha == 2 * direcao and abs(delta_coluna) == 2:
            meio_linha = linha_o + direcao
            meio_coluna = col_o + (delta_coluna // 2)
            p_meio = pecas[meio_linha][meio_coluna]

            if p_meio is not None and p_meio != self.turno:
                return True
            else:
                print("Não há peça adversária para capturar.")
                return False

        print("Movimento inválido.")
        return False

    def mover_peca(self, origem, destino):
        linha_o, col_o = origem
        linha_d, col_d = destino

        pecas = self.tabuleiro.tabuleiro
        peca = pecas[linha_o][col_o]  # <-- pegar peça antes de mover

        pecas[linha_d][col_d] = peca
        pecas[linha_o][col_o] = None

        # Verificar se foi uma captura
        if abs(linha_d - linha_o) == 2:
            meio_linha = (linha_o + linha_d) // 2
            meio_coluna = (col_o + col_d) // 2
            pecas[meio_linha][meio_coluna] = None
        
        # Verificar promoção
        if peca == 'B' and linha_d == 0:
            pecas[linha_d][col_d] = 'BD'  # dama branca
            print("Peça branca promovida a Dama!")
        elif peca == 'P' and linha_d == 7:
            pecas[linha_d][col_d] = 'PD'  # dama preta
            print("Peça preta promovida a Dama!")

    def verificar_captura_disponivel(self, pos):
        linha, col = pos
        pecas = self.tabuleiro.tabuleiro
        peca = pecas[linha][col]

        direcoes = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # diagonais com salto
        for d_l, d_c in direcoes:
            nova_linha = linha + d_l
            nova_col = col + d_c

            meio_linha = linha + d_l // 2
            meio_col = col + d_c // 2

            if 0 <= nova_linha < 8 and 0 <= nova_col < 8:
                destino = pecas[nova_linha][nova_col]
                meio = pecas[meio_linha][meio_col]

                if destino is None and meio is not None and meio.lower() != peca.lower():
                    return True  # existe captura disponível

        return False

    def pode_capturar_novamente(self, posicao):
        linha, col = posicao
        direcao = -1 if self.turno == 'B' else 1
        pecas = self.tabuleiro.tabuleiro

        for delta_col in [-2, 2]:
            nova_linha = linha + 2 * direcao
            nova_coluna = col + delta_col
            meio_linha = linha + direcao
            meio_coluna = col + (delta_col // 2)

            if 0 <= nova_linha < 8 and 0 <= nova_coluna < 8:
                destino = pecas[nova_linha][nova_coluna]
                meio = pecas[meio_linha][meio_coluna]

                if destino is None and meio is not None and meio.lower() != self.turno:
                    return True
        return False

    def jogar(self):
        while True:
            self.tabuleiro.mostrar()
            origem, destino = ler_movimento(self.turno)

            if self.validar_movimento(origem, destino):
                self.mover_peca(origem, destino)

                linha_o, col_o = origem
                linha_d, col_d = destino
                if abs(linha_d - linha_o) == 2:  # movimento de captura
                    nova_origem = destino  # define aqui, só se for captura

                    while self.verificar_captura_disponivel(nova_origem):
                        self.tabuleiro.mostrar()
                        print("Você pode capturar outra peça!")
                        novo_destino = ler_movimento_continuacao(nova_origem)

                        if self.validar_movimento(nova_origem, novo_destino):
                            self.mover_peca(nova_origem, novo_destino)
                            nova_origem = novo_destino
                        else:
                            print("Movimento inválido na sequência de capturas.")
                            break

                self.alternar_turno()

            else:
                print("Movimento inválido, tente novamente.")

if __name__ == "__main__":
    jogo = Jogo()
    jogo.jogar()
