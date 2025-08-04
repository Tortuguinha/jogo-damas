import random
from .tabuleiro import Tabuleiro, Peao, Dama
from .ui_base import UIBase
from src.menu_historico import adicionar_partida

class Jogo:
    def __init__(self, ui: UIBase, tabuleiro=None, regras=None, vs_ia=False, cor_ia='P'):
        self.tabuleiro = tabuleiro if tabuleiro else Tabuleiro()
        self.turno = 'B'
        self.ui = ui
        self.ui.tabuleiro = self.tabuleiro  # UI pode validar posições

        regras = regras or {}
        self.captura_obrigatoria = regras.get("captura_obrigatoria", True)
        self.dama_multi_captura = regras.get("dama_multi_captura", True)
        self.multiplas_capturas = regras.get("multiplas_capturas", True)

        # Controle do modo IA
        self.vs_ia = vs_ia
        self.cor_ia = cor_ia  # cor que a IA joga ('B' ou 'P')

    def alternar_turno(self):
        self.turno = 'P' if self.turno == 'B' else 'B'

    def validar_movimento(self, origem, destino):
        peca = self.tabuleiro.obter_peca(origem)
        if not peca:
            self.ui.mostrar_mensagem("Não há peça na posição de origem.")
            return False
        if peca.cor != self.turno:
            self.ui.mostrar_mensagem("Você só pode mover suas próprias peças.")
            return False

        # Captura obrigatória: se há captura para o turno, movimento deve ser captura
        if self.captura_obrigatoria and self.tabuleiro.existe_captura(self.turno):
            linha_o, col_o = origem
            linha_d, col_d = destino
            if abs(linha_d - linha_o) <= 1:  # movimento simples, não captura
                self.ui.mostrar_mensagem("Captura obrigatória! Você deve capturar uma peça.")
                return False

        if not self.tabuleiro.movimento_valido(origem, destino):
            self.ui.mostrar_mensagem("Movimento inválido para essa peça.")
            return False
        return True

    def verificar_captura_disponivel(self, pos):
        peca = self.tabuleiro.obter_peca(pos)
        if not peca:
            return False

        for mov in peca.movimentos_validos(pos, self.tabuleiro):
            if abs(mov[0] - pos[0]) > 1:
                return True
        return False

    def fim_de_jogo(self, cor):
        for linha in range(self.tabuleiro.tamanho):
            for coluna in range(self.tabuleiro.tamanho):
                peca = self.tabuleiro.obter_peca((linha, coluna))
                if peca and peca.cor == cor:
                    if peca.movimentos_validos((linha, coluna), self.tabuleiro):
                        return False
        return True

    def ia_escolher_movimento(self):
        movimentos_possiveis = []

        for linha in range(self.tabuleiro.tamanho):
            for coluna in range(self.tabuleiro.tamanho):
                peca = self.tabuleiro.obter_peca((linha, coluna))
                if peca and peca.cor == self.cor_ia:
                    movimentos = self.tabuleiro.movimentos_validos_para_peca((linha, coluna))
                    for destino in movimentos:
                        movimentos_possiveis.append(((linha, coluna), destino))

        if not movimentos_possiveis:
            return None, None

        return random.choice(movimentos_possiveis)

    def jogar(self):
        while True:
            self.tabuleiro.mostrar()

            if self.vs_ia and self.turno == self.cor_ia:
                origem, destino = self.ia_escolher_movimento()
                if origem is None or destino is None:
                    self.ui.mostrar_mensagem("IA não tem movimentos válidos. Você venceu!")
                    break
                self.ui.mostrar_mensagem(f"IA move de {origem} para {destino}.")
                # Se quiser, pode adicionar delay aqui para ver o movimento

            else:
                origem, destino = self.ui.ler_movimento(self.turno)
                if origem is None or destino is None:
                    self.ui.mostrar_mensagem("Jogo encerrado pelo usuário.")
                    break

            if not self.validar_movimento(origem, destino):
                continue

            linha_o, col_o = origem
            linha_d, col_d = destino

            promovido = self.tabuleiro.mover_peca(origem, destino)
            if promovido:
                self.ui.mostrar_mensagem(f"Peça {self.turno} promovida a Dama!")

            # Verifica se houve captura (2 ou mais casas de distância)
            if abs(linha_d - linha_o) > 1:
                nova_origem = destino
                peca = self.tabuleiro.obter_peca(nova_origem)

                if self.multiplas_capturas:
                    if isinstance(peca, Peao) or (self.dama_multi_captura and isinstance(peca, Dama)):
                        while not promovido and self.verificar_captura_disponivel(nova_origem):
                            self.tabuleiro.mostrar()
                            self.ui.mostrar_mensagem("Você pode capturar outra peça!")
                            if self.vs_ia and self.turno == self.cor_ia:
                                novo_destino = None
                                # IA continua capturando, escolher próximo movimento válido
                                movimentos = [mov for mov in peca.movimentos_validos(nova_origem, self.tabuleiro)
                                             if abs(mov[0] - nova_origem[0]) > 1]
                                if movimentos:
                                    novo_destino = random.choice(movimentos)
                                    self.ui.mostrar_mensagem(f"IA captura novamente de {nova_origem} para {novo_destino}.")
                                else:
                                    break
                            else:
                                novo_destino = self.ui.ler_movimento_continuacao(nova_origem)
                                if novo_destino is None:
                                    self.ui.mostrar_mensagem("Jogo encerrado pelo usuário.")
                                    return

                            if novo_destino and self.validar_movimento(nova_origem, novo_destino):
                                promovido = self.tabuleiro.mover_peca(nova_origem, novo_destino)
                                nova_origem = novo_destino
                                if promovido:
                                    self.ui.mostrar_mensagem(f"Peça {self.turno} promovida a Dama!")
                                    break
                            else:
                                self.ui.mostrar_mensagem("Movimento inválido na sequência de capturas.")
                                break
                else:
                    pass  # múltiplas capturas desativadas

            self.alternar_turno()

            if self.fim_de_jogo(self.turno):
                self.ui.mostrar_mensagem(f"\nJogador {'Brancas' if self.turno == 'B' else 'Pretas'} não tem mais movimentos.")
                self.ui.mostrar_mensagem(f"Jogador {'Pretas' if self.turno == 'B' else 'Brancas'} venceu!")
                break
