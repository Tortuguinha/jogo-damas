from src.tabuleiro import Tabuleiro, Peao, Dama

def test_tabuleiro_tem_64_posicoes():
    tab = Tabuleiro()
    total_posicoes = sum(1 for linha in tab.tabuleiro for _ in linha)
    assert total_posicoes == 64

def test_tabuleiro_inicial_tem_12_pecas_por_lado():
    tab = Tabuleiro()
    todas = [p for linha in tab.tabuleiro for p in linha if p]
    brancas = sum(1 for p in todas if p.cor == 'B')
    pretas = sum(1 for p in todas if p.cor == 'P')
    assert brancas == 12
    assert pretas == 12

def test_posicao_valida_funciona():
    tab = Tabuleiro()
    assert tab.posicao_valida((0, 0))
    assert not tab.posicao_valida((-1, 0))
    assert not tab.posicao_valida((8, 8))
