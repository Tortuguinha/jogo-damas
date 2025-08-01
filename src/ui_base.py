from abc import ABC, abstractmethod

class UIBase(ABC):
    @abstractmethod
    def ler_movimento(self, turno):
        """
        Lê o movimento completo: origem e destino.
        Deve retornar (origem, destino) ou (None, None) para sair.
        """
        pass

    @abstractmethod
    def ler_movimento_continuacao(self, origem):
        """
        Lê o próximo destino em sequência de captura.
        Deve retornar destino ou None para sair.
        """
        pass

    @abstractmethod
    def mostrar_mensagem(self, mensagem):
        """
        Exibe uma mensagem para o usuário.
        """
        pass