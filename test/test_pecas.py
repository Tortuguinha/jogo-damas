from src.jogo import Jogo
from src.tabuleiro import Peao

def test_movimento_simples_valido():
    jogo = Jogo()
    jogo.tabuleiro.tabuleiro = [[None for _ in range(8)] for _ in range(8)]
    jogo.tabuleiro.tabuleiro[5][0] = 'B'
    assert jogo.validar_movimento((5, 0), (4, 1)) is True

def test_movimento_invalido_destino_ocupado():
    jogo = Jogo()
    jogo.tabuleiro.tabuleiro = [[None for _ in range(8)] for _ in range(8)]
    jogo.tabuleiro.tabuleiro[5][0] = Peao('B')
    jogo.tabuleiro.tabuleiro[4][1] = Peao('P')
    assert jogo.validar_movimento((5, 0), (4, 1)) is False
