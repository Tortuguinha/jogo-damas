# ui_base.py

from abc import ABC, abstractmethod

class UIBase(ABC):
    def __init__(self, tabuleiro):
        self.tabuleiro = tabuleiro

    @abstractmethod
    def ler_movimento(self, turno):
        pass

    @abstractmethod
    def ler_movimento_continuacao(self, origem):
        pass

    @abstractmethod
    def mostrar_mensagem(self, mensagem):
        pass
