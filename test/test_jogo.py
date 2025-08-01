import pytest
from src.jogo import Jogo
from src.tabuleiro import Peao, Dama

def test_jogada_basica_e_turnos():
    jogo = Jogo()

    # Turno inicial: Brancas
    assert jogo.turno == 'B'

    # Movimento válido: peça branca na (5,0) para (4,1)
    origem = (5, 0)
    destino = (4, 1)
    assert jogo.validar_movimento(origem, destino)
    assert jogo.mover_peca(origem, destino)

    # Depois do movimento, turno deve alternar
    jogo.alternar_turno()
    assert jogo.turno == 'P'

    # Movimento inválido: peça preta tentando mover peça branca
    origem = (4, 1)  # peça branca recém movida
    destino = (3, 0)
    assert not jogo.validar_movimento(origem, destino)

def test_captura_simples():
    jogo = Jogo()

    # Setup manual para situação de captura:
    # Peça branca em (5, 0)
    # Peça preta em (4, 1)
    # Espaço livre em (3, 2)
    jogo.tabuleiro.tabuleiro[5][0] = Peao('B')
    jogo.tabuleiro.tabuleiro[4][1] = Peao('P')
    jogo.tabuleiro.tabuleiro[3][2] = None

    origem = (5, 0)
    destino = (3, 2)

    assert jogo.validar_movimento(origem, destino)
    assert jogo.mover_peca(origem, destino)

    # Peça preta foi capturada
    assert jogo.tabuleiro.obter_peca((4,1)) is None
    # Peça branca está na nova posição
    peca = jogo.tabuleiro.obter_peca(destino)
    assert peca is not None and peca.cor == 'B'

def test_promocao_a_dama():
    jogo = Jogo()

    # Coloca peça branca quase na promoção
    jogo.tabuleiro.tabuleiro[1][2] = Peao('B')
    jogo.tabuleiro.tabuleiro[0][1] = None

    origem = (1, 2)
    destino = (0, 1)

    assert jogo.validar_movimento(origem, destino)
    assert jogo.mover_peca(origem, destino)

    peca = jogo.tabuleiro.obter_peca(destino)
    assert isinstance(peca, Dama)
    assert peca.cor == 'B'
