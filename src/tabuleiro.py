class Tabuleiro:
    tamanho = 8
    def __init__(self):
        self.tabuleiro = self.criar_tabuleiro()

    def criar_tabuleiro(self):
        tab = [[None for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        for linha in range(3):
            for col in range(self.tamanho):
                if (linha + col) % 2 != 1:  # Casas escuras para peças
                    continue
                tab[linha][col] = Peao('P')
        for linha in range(5, 8):
            for col in range(self.tamanho):
                if (linha + col) % 2 != 1:
                    continue
                tab[linha][col] = Peao('B')
        return tab
    

    def mostrar(self):
        print("  " + " ".join(str(i) for i in range(self.tamanho)))
        for i, linha in enumerate(self.tabuleiro):
            linha_str = ""
            for peca in linha:
                linha_str += (str(peca) if peca else '.') + " "
            print(f"{i} {linha_str}")


    def posicao_valida(self, pos):
        linha, col = pos
        return 0 <= linha < self.tamanho and 0 <= col < self.tamanho

    def obter_peca(self, pos):
        if self.posicao_valida(pos):
            return self.tabuleiro[pos[0]][pos[1]]
        return None

    def destino_livre(self, pos):
        return self.obter_peca(pos) is None

    def movimentos_validos_para_peca(self, pos):
        peca = self.obter_peca(pos)
        if not peca:
            return []
        return peca.movimentos_validos(pos, self)

    def movimento_valido(self, origem, destino):
        return destino in self.movimentos_validos_para_peca(origem)

    def mover_peca(self, origem, destino):
        if not (self.posicao_valida(origem) and self.posicao_valida(destino)):
            raise ValueError("Posição inválida")

        peca = self.obter_peca(origem)
        if peca is None:
            raise ValueError("Não há peça na posição de origem")

        linha_o, col_o = origem
        linha_d, col_d = destino

        # Se for captura, remover peça adversária no caminho
        if abs(linha_d - linha_o) > 1 and abs(col_d - col_o) > 1:
            step_linha = 1 if linha_d > linha_o else -1
            step_col = 1 if col_d > col_o else -1
            i, j = linha_o + step_linha, col_o + step_col

            while (i, j) != (linha_d, col_d):
                peca_caminho = self.obter_peca((i, j))
                if peca_caminho is not None and peca_caminho.cor != peca.cor:
                    self.tabuleiro[i][j] = None  # remove peça capturada
                    break
                i += step_linha
                j += step_col

        # Atualiza posições da peça
        self.tabuleiro[destino[0]][destino[1]] = peca
        self.tabuleiro[origem[0]][origem[1]] = None

        # ---- Promoção a dama ----
        if isinstance(peca, Peao):
            if (peca.cor == 'B' and linha_d == 0) or (peca.cor == 'P' and linha_d == self.tamanho - 1):
                self.tabuleiro[destino[0]][destino[1]] = Dama(peca.cor)

class Peca:
    def __init__(self, cor):
        self.cor = cor  # 'B' ou 'P'

    def __str__(self):
        return self.cor

    # Pode adicionar método para movimentos válidos (a ser implementado nas subclasses)
    def movimentos_validos(self, pos, tabuleiro):
        raise NotImplementedError


class Peao(Peca):
    def movimentos_validos(self, pos, tabuleiro):
        movimentos = []
        linha, col = pos

        direcao = -1 if self.cor == 'B' else 1  # peões brancos sobem (linha -1), pretos descem (linha +1)
        tamanho = tabuleiro.tamanho

        # Movimento simples (andar uma casa na diagonal)
        for d_col in [-1, 1]:
            nova_pos = (linha + direcao, col + d_col)
            if tabuleiro.posicao_valida(nova_pos) and tabuleiro.destino_livre(nova_pos):
                movimentos.append(nova_pos)

        # Captura (pular uma casa na diagonal sobre peça adversária)
        for d_col in [-2, 2]:
            nova_pos = (linha + 2 * direcao, col + d_col)
            meio_pos = (linha + direcao, col + d_col // 2)

            if (tabuleiro.posicao_valida(nova_pos) and tabuleiro.destino_livre(nova_pos)):
                peca_meio = tabuleiro.obter_peca(meio_pos)
                if peca_meio is not None and peca_meio.cor != self.cor:
                    movimentos.append(nova_pos)

        return movimentos


class Dama(Peca):
    def __str__(self):
        return self.cor + 'D'

    def movimentos_validos(self, pos, tabuleiro):
        movimentos = []
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        linha, col = pos

        for d_linha, d_col in direcoes:
            i, j = linha + d_linha, col + d_col
            encontrou_adversaria = False
            while 0 <= i < tabuleiro.tamanho and 0 <= j < tabuleiro.tamanho:
                peca = tabuleiro.obter_peca((i, j))
                if peca is None:
                    if not encontrou_adversaria:
                        movimentos.append((i, j))  # movimento livre
                    else:
                        movimentos.append((i, j))  # possível captura
                        break  # não pode seguir após captura
                elif peca.cor != self.cor and not encontrou_adversaria:
                    encontrou_adversaria = True
                else:
                    break  # encontrou peça própria ou já capturou alguém

                i += d_linha
                j += d_col

        return movimentos