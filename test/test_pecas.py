from src.tabuleiro import Peao, Dama, Tabuleiro

def test_movimentos_validos_peao_branco():
    tab = Tabuleiro()
    peao = Peao('B')
    tab.tabuleiro[5][2] = peao
    tab.tabuleiro[4][3] = None
    movimentos = peao.movimentos_validos((5, 2), tab)
    assert (4, 3) in movimentos

def test_peao_pode_capturar():
    tab = Tabuleiro()
    peao = Peao('B')
    inimigo = Peao('P')
    tab.tabuleiro[5][2] = peao
    tab.tabuleiro[4][3] = inimigo
    tab.tabuleiro[3][4] = None
    movimentos = peao.movimentos_validos((5, 2), tab)
    assert (3, 4) in movimentos

def test_dama_movimenta_em_diagonal():
    tab = Tabuleiro()
    dama = Dama('P')
    tab.tabuleiro[4][4] = dama
    movimentos = dama.movimentos_validos((4, 4), tab)
    assert (3, 3) in movimentos
    assert (2, 2) in movimentos
    assert (5, 5) in movimentos
