from .tabuleiro import Tabuleiro

TABULEIRO = Tabuleiro()  # Instância fixa só para validar posições

def ler_movimento(turno):
    """
    Lê o movimento completo: origem e destino no formato 'linha,coluna-linha,coluna'.
    Retorna tupla (origem, destino) ou (None, None) para sair.
    """
    while True:
        try:
            movimento = input(f"Jogador {'Brancas' if turno == 'B' else 'Pretas'}, digite o movimento (ex: 2,3-3,4) ou 'sair' para terminar: ").strip().replace(" ", "")
            if movimento.lower() == 'sair':
                return None, None

            origem_str, destino_str = movimento.split('-')
            origem = tuple(int(x) for x in origem_str.split(','))
            destino = tuple(int(x) for x in destino_str.split(','))

            if TABULEIRO.posicao_valida(origem) and TABULEIRO.posicao_valida(destino):
                return origem, destino
            else:
                print("Posição inválida! Use números entre 0 e 7 para linha e coluna.")
        except ValueError:
            print("Entrada inválida! Use o formato: linha,coluna-linha,coluna (ex: 2,3-3,4)")

def ler_movimento_continuacao(origem):
    """
    Lê o próximo destino para movimentos de captura múltipla.
    Retorna destino ou None para sair.
    """
    while True:
        try:
            movimento = input(f"Você pode capturar novamente com a peça em {origem}. Digite o próximo destino (ex: 1,6) ou 'sair' para terminar: ").strip()
            if movimento.lower() == 'sair':
                return None

            destino = tuple(int(x) for x in movimento.split(','))

            if TABULEIRO.posicao_valida(destino):
                return destino
            else:
                print("Posição inválida! Use números entre 0 e 7 para linha e coluna.")
        except ValueError:
            print("Entrada inválida! Use o formato: linha,coluna (ex: 1,6)")

def validar_posicao(pos):
    """
    Valida se a posição está dentro dos limites do tabuleiro.
    """
    return TABULEIRO.posicao_valida(pos)
