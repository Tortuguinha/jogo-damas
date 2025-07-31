class Tabuleiro:
    def __init__(self):
        self.tamanho = 8
        self.tabuleiro = self.criar_tabuleiro()

    def criar_tabuleiro(self):
        tab = [[None for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.posicionar_pecas_pretas(tab)
        self.posicionar_pecas_brancas(tab)
        return tab

    def posicionar_pecas_pretas(self, tab):
        for linha in range(3):
            for col in range(self.tamanho):
                if (linha + col) % 2 != 0:
                    tab[linha][col] = Peao('P')

    def posicionar_pecas_brancas(self, tab):
        for linha in range(5, 8):
            for col in range(self.tamanho):
                if (linha + col) % 2 != 0:
                    tab[linha][col] = Peao('B')

    def posicao_valida(self, pos):
        linha, col = pos
        return 0 <= linha < self.tamanho and 0 <= col < self.tamanho

    def mover_peca(self, origem, destino):
        if not (self.posicao_valida(origem) and self.posicao_valida(destino)):
            raise ValueError("Posição inválida")

        peca = self.tabuleiro[origem[0]][origem[1]]
        self.tabuleiro[destino[0]][destino[1]] = peca
        self.tabuleiro[origem[0]][origem[1]] = None

    def estado_texto(self):
        linhas = []
        for linha in self.tabuleiro:
            linha_str = ''.join([str(p) if p else '.' for p in linha])
            linhas.append(linha_str)
        return '\n'.join(linhas)

    def mostrar(self):
            print("  0 1 2 3 4 5 6 7")  # cabeçalho das colunas
            for i, linha in enumerate(self.tabuleiro):
                linha_str = ''
                for peca in linha:
                    if peca is None:
                        linha_str += '. '
                    else:
                        linha_str += str(peca) + ' '
                print(f"{i} {linha_str}")

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
        # Aqui você pode implementar regras de movimento específicas para peão
        pass


class Dama(Peca):
    def __str__(self):
        return self.cor + 'D'

    def movimentos_validos(self, pos, tabuleiro):
        # Implementar movimentos válidos para dama
        pass
