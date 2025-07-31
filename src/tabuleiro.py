class Tabuleiro:
    def __init__(self):
        self.tamanho = 8
        self.tabuleiro = self.criar_tabuleiro()

    def criar_tabuleiro(self):
        # Criar matriz 8x8 preenchida com None
        tab = [[None for _ in range(self.tamanho)] for _ in range(self.tamanho)]

        # Posicionar peças pretas (linha 0,1,2 nas casas "escuras")
        for linha in range(3):
            for col in range(self.tamanho):
                if (linha + col) % 2 != 0:
                    tab[linha][col] = 'P'  # peça preta

        # Posicionar peças brancas (linha 5,6,7 nas casas "escuras")
        for linha in range(5, 8):
            for col in range(self.tamanho):
                if (linha + col) % 2 != 0:
                    tab[linha][col] = 'B'  # peça branca

        return tab

    def mostrar(self):
        print("  " + " ".join(str(i) for i in range(self.tamanho)))
        for i, linha in enumerate(self.tabuleiro):
            linha_str = []
            for casa in linha:
                if casa is None:
                    linha_str.append(".")
                else:
                    linha_str.append(casa)
            print(f"{i} " + " ".join(linha_str))


if __name__ == "__main__":
    tab = Tabuleiro()
    tab.mostrar()
