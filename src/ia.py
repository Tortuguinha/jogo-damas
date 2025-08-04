import random

def escolher_movimento_aleatorio(tabuleiro, cor):
    """
    Recebe o tabuleiro atual e a cor do jogador ('B' ou 'P').
    Retorna uma tupla (origem, destino) de um movimento válido aleatório.
    """
    movimentos_possiveis = []

    for linha in range(tabuleiro.tamanho):
        for coluna in range(tabuleiro.tamanho):
            peca = tabuleiro.obter_peca((linha, coluna))
            if peca and peca.cor == cor:
                movimentos = tabuleiro.movimentos_validos_para_peca((linha, coluna))
                for destino in movimentos:
                    movimentos_possiveis.append(((linha, coluna), destino))

    if not movimentos_possiveis:
        return None, None

    return random.choice(movimentos_possiveis)
