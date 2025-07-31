from src.tabuleiro import Tabuleiro

def test_tabuleiro_inicial_tem_64_posicoes():
    tab = Tabuleiro()
    total_posicoes = sum(len(linha) for linha in tab.tabuleiro)
    assert total_posicoes == 64

def test_tabuleiro_tem_12_pecas_brancas_e_12_pretas():
    tab = Tabuleiro()
    pecas = sum(tab.tabuleiro, [])  # achata a lista
    brancas = pecas.count('B')
    pretas = pecas.count('P')
    assert brancas == 12
    assert pretas == 12
