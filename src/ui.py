def ler_movimento(turno):
    while True:
        try:
            movimento = input(f"Jogador {'Brancas' if turno == 'B' else 'Pretas'}, digite o movimento (ex: 2,3-3,4): ").strip()
            origem_str, destino_str = movimento.split('-')
            origem = tuple(int(x) for x in origem_str.split(','))
            destino = tuple(int(x) for x in destino_str.split(','))

            if validar_posicao(origem) and validar_posicao(destino):
                return origem, destino
            else:
                print("Posição inválida! Use números entre 0 e 7 para linha e coluna.")
        except ValueError:
            print("Entrada inválida! Use o formato: linha,coluna-linha,coluna (ex: 2,3-3,4)")

def ler_movimento_continuacao(origem):
    while True:
        try:
            movimento = input(f"Você pode capturar novamente com a peça em {origem}. Digite o próximo destino (ex: 1,6): ")
            destino = tuple(int(x) for x in movimento.split(','))

            if validar_posicao(destino):
                return destino   # <-- Retorna só o destino, não (origem, destino)
            else:
                print("Posição inválida! Use números entre 0 e 7.")
        except:
            print("Entrada inválida! Use o formato: linha,coluna (ex: 1,6)")

def validar_posicao(pos):
    linha, col = pos
    return 0 <= linha <= 7 and 0 <= col <= 7
