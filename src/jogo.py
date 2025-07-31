from .tabuleiro import Tabuleiro
from .ui import ler_movimento, ler_movimento_continuacao, validar_posicao

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

        # Se for dama
        if p_origem in ['BD', 'PD']:
            if not self.validar_movimento_dama(origem, destino, p_origem):
                print("Movimento inválido para dama.")
                return False
            return True

        # Movimento normal para peões comuns:
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

            if p_meio is not None and p_meio[0] != p_origem[0]:
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
        peca = pecas[linha_o][col_o]  # peça antes de mover

        pecas[linha_d][col_d] = peca
        pecas[linha_o][col_o] = None

        # Captura para peões (movimento de 2 casas)
        if abs(linha_d - linha_o) == 2 and peca in ['B', 'P']:
            meio_linha = (linha_o + linha_d) // 2
            meio_coluna = (col_o + col_d) // 2
            pecas[meio_linha][meio_coluna] = None

        # Captura para damas (movimento maior)
        if peca in ['BD', 'PD']:
            valido, pos_peca_capturada = self._caminho_livre_e_captura(origem, destino, peca)
            if valido and pos_peca_capturada:
                pecas[pos_peca_capturada[0]][pos_peca_capturada[1]] = None

        # Promoção
        if peca == 'B' and linha_d == 0:
            pecas[linha_d][col_d] = 'BD'
            print("Peça branca promovida a Dama!")
        elif peca == 'P' and linha_d == 7:
            pecas[linha_d][col_d] = 'PD'
            print("Peça preta promovida a Dama!")

    def verificar_captura_disponivel(self, pos):
        linha, col = pos
        pecas = self.tabuleiro.tabuleiro
        peca = pecas[linha][col]

        if peca in ['BD', 'PD']:
            return self.pode_capturar_dama(pos)
        else:
            # lógica dos peões
            direcoes = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
            for d_l, d_c in direcoes:
                nova_linha = linha + d_l
                nova_col = col + d_c

                meio_linha = linha + d_l // 2
                meio_col = col + d_c // 2

                if 0 <= nova_linha < 8 and 0 <= nova_col < 8:
                    destino = pecas[nova_linha][nova_col]
                    meio = pecas[meio_linha][meio_col]

                    if destino is None and meio is not None and meio.lower() != peca.lower():
                        return True
            return False

    def pode_capturar_novamente(self, posicao):
        linha, col = posicao
        pecas = self.tabuleiro.tabuleiro
        peca = pecas[linha][col]

        if peca in ['BD', 'PD']:
            return self.pode_capturar_dama(posicao)

        direcao = -1 if self.turno == 'B' else 1
        for delta_col in [-2, 2]:
            nova_linha = linha + 2 * direcao
            nova_coluna = col + delta_col
            meio_linha = linha + direcao
            meio_coluna = col + (delta_col // 2)

            if 0 <= nova_linha < 8 and 0 <= nova_coluna < 8:
                destino = pecas[nova_linha][nova_coluna]
                meio = pecas[meio_linha][meio_coluna]

                if destino is None and meio is not None and meio.lower() != peca.lower():
                    return True
        return False

    def jogar(self):
        while True:
            self.tabuleiro.mostrar()
            origem, destino = ler_movimento(self.turno)

            # Verifica se o usuário pediu para sair
            if origem is None or destino is None:
                print("Jogo encerrado pelo usuário.")
                break

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

    def _caminho_livre_e_captura(self, origem, destino, peca):
        pecas = self.tabuleiro.tabuleiro
        linha_o, col_o = origem
        linha_d, col_d = destino
        delta_linha = linha_d - linha_o
        delta_coluna = col_d - col_o

        if abs(delta_linha) != abs(delta_coluna):
            return False, None

        step_linha = 1 if delta_linha > 0 else -1
        step_coluna = 1 if delta_coluna > 0 else -1

        pecas_no_caminho = 0
        pos_peca_capturada = None

        linha_atual = linha_o + step_linha
        col_atual = col_o + step_coluna

        while (linha_atual, col_atual) != (linha_d, col_d):
            atual = pecas[linha_atual][col_atual]
            if atual is not None:
                if atual[0] == peca[0]:
                    return False, None
                pecas_no_caminho += 1
                pos_peca_capturada = (linha_atual, col_atual)
                if pecas_no_caminho > 1:
                    return False, None
            linha_atual += step_linha
            col_atual += step_coluna

        if pecas_no_caminho <= 1:
            return True, pos_peca_capturada
        else:
            return False, None
    def validar_movimento_dama(self, origem, destino, peca):
        valido, _ = self._caminho_livre_e_captura(origem, destino, peca)
        return valido

    def pode_capturar_dama(self, pos):
        linha, col = pos
        pecas = self.tabuleiro.tabuleiro
        peca = pecas[linha][col]

        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d_l, d_c in direcoes:
            l, c = linha + d_l, col + d_c
            encontrou_adversaria = False
            while 0 <= l < 8 and 0 <= c < 8:
                if pecas[l][c] is not None:
                    if pecas[l][c][0] != peca[0]:
                        if not encontrou_adversaria:
                            encontrou_adversaria = True
                        else:
                            break
                    else:
                        break
                else:
                    if encontrou_adversaria:
                        return True
                l += d_l
                c += d_c
        return False
