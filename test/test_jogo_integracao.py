import pytest
from src.jogo import Jogo

def test_jogo_fluxo_simples(monkeypatch):
    # Sequência simulada de inputs do jogador
    # Cada string representa o que o usuário digitou para input()
    inputs = iter([
        "5,0-4,1",   # movimento válido das brancas
        "2,1-3,0",   # movimento válido das pretas
        "sair"       # sair do jogo
    ])

    # Função mock para input
    def mock_input(prompt):
        return next(inputs)

    monkeypatch.setattr("builtins.input", mock_input)

    jogo = Jogo()
    jogo.jogar()

    # Aqui você pode adicionar asserts para o estado final do tabuleiro, turno, etc.
