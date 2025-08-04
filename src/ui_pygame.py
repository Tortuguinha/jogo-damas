import pygame, sys
from .ui_base import UIBase
from .tabuleiro import Tabuleiro, Dama
from .cores import PRETO, BRANCO

class UIPygame(UIBase):
    def __init__(self, tabuleiro):
        super().__init__(tabuleiro)
        pygame.init()
        self.tela = pygame.display.set_mode((640, 640))
        pygame.display.set_caption("Jogo de Damas")
        self.fonte = pygame.font.SysFont("arial", 24)

        self.selecionado = None
        self.movimentos_validos = []
        self.mensagem = ""

    def pos_click_para_casa(self, pos):
        x, y = pos
        tamanho_casa = self.tela.get_width() // self.tabuleiro.tamanho
        coluna = x // tamanho_casa
        linha = y // tamanho_casa

        if 0 <= linha < self.tabuleiro.tamanho and 0 <= coluna < self.tabuleiro.tamanho:
            return (linha, coluna)
        else:
            return None

    def ler_movimento(self, turno):
        origem = None
        destino = None

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  # fecha o programa imediatamente
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_casa = self.pos_click_para_casa(evento.pos)
                    if pos_casa is None:
                        continue

                    peca = self.tabuleiro.obter_peca(pos_casa)

                    if origem is None:
                        if peca and peca.cor == turno:
                            movimentos = self.tabuleiro.movimentos_validos_para_peca(pos_casa)
                            if movimentos:
                                origem = pos_casa
                                self.selecionado = origem
                                self.movimentos_validos = movimentos
                                self.mostrar_mensagem(f"Peça selecionada em {origem}. Escolha o destino.")
                            else:
                                self.mostrar_mensagem("Essa peça não possui movimentos válidos.")
                        else:
                            self.mostrar_mensagem("Selecione uma peça sua com movimentos válidos.")
                    else:
                        if pos_casa == origem:
                            origem = None
                            self.selecionado = None
                            self.movimentos_validos = []
                            self.mostrar_mensagem("Seleção cancelada.")
                        elif peca and peca.cor == turno:
                            movimentos = self.tabuleiro.movimentos_validos_para_peca(pos_casa)
                            if movimentos:
                                origem = pos_casa
                                self.selecionado = origem
                                self.movimentos_validos = movimentos
                                self.mostrar_mensagem(f"Peça alterada para {origem}. Escolha o destino.")
                            else:
                                self.mostrar_mensagem("Essa peça não possui movimentos válidos.")
                        elif pos_casa in self.movimentos_validos:
                            destino = pos_casa
                            self.selecionado = None
                            self.movimentos_validos = []
                            self.mostrar_mensagem("")
                            return origem, destino
                        else:
                            self.mostrar_mensagem("Movimento inválido. Escolha um destino válido.")

            self.tela.fill(PRETO)
            self.desenhar_tabuleiro()
            self.desenhar_pecas()
            self.desenhar_selecao()
            self.desenhar_mensagem()
            pygame.display.flip()

    def ler_movimento_continuacao(self, origem):
        self.selecionado = origem
        self.movimentos_validos = self.tabuleiro.movimentos_validos_para_peca(origem)

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  # fecha o programa imediatamente
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_casa = self.pos_click_para_casa(evento.pos)
                    if pos_casa is None:
                        continue

                    if pos_casa in self.movimentos_validos:
                        self.mostrar_mensagem("")
                        self.selecionado = None
                        self.movimentos_validos = []
                        return pos_casa
                    else:
                        self.mostrar_mensagem("Movimento inválido. Escolha um destino válido.")

            self.tela.fill(PRETO)
            self.desenhar_tabuleiro()
            self.desenhar_pecas()
            self.desenhar_selecao()
            self.desenhar_mensagem()
            pygame.display.flip()

    def desenhar_mensagem(self):
        if self.mensagem:
            texto = self.fonte.render(self.mensagem, True, (255, 255, 255))
            rect = texto.get_rect(center=(self.tela.get_width() // 2, self.tela.get_height() - 30))
            self.tela.blit(texto, rect)

    def desenhar_tabuleiro(self):
        tamanho_casa = self.tela.get_width() // self.tabuleiro.tamanho
        cores = [(235, 209, 166), (165, 117, 81)]  # cores claras e escuras das casas

        for linha in range(self.tabuleiro.tamanho):
            for coluna in range(self.tabuleiro.tamanho):
                cor = cores[(linha + coluna) % 2]
                rect = pygame.Rect(coluna * tamanho_casa, linha * tamanho_casa, tamanho_casa, tamanho_casa)
                pygame.draw.rect(self.tela, cor, rect)

    def desenhar_pecas(self):
        tamanho_casa = self.tela.get_width() // self.tabuleiro.tamanho
        for linha in range(self.tabuleiro.tamanho):
            for coluna in range(self.tabuleiro.tamanho):
                peca = self.tabuleiro.obter_peca((linha, coluna))
                if peca:
                    cor_peca = (255, 255, 255) if peca.cor == 'B' else (0, 0, 0)
                    centro = (coluna * tamanho_casa + tamanho_casa // 2, linha * tamanho_casa + tamanho_casa // 2)
                    pygame.draw.circle(self.tela, cor_peca, centro, tamanho_casa // 2 - 10)

                    if isinstance(peca, Dama):
                        pygame.draw.circle(self.tela, (255, 215, 0), centro, tamanho_casa // 4)  # Marcação para dama

    def desenhar_selecao(self):
        if self.selecionado:
            tamanho_casa = self.tela.get_width() // self.tabuleiro.tamanho
            linha, coluna = self.selecionado
            rect = pygame.Rect(coluna * tamanho_casa, linha * tamanho_casa, tamanho_casa, tamanho_casa)
            pygame.draw.rect(self.tela, (255, 255, 0), rect, 3)  # contorno amarelo na seleção

            # Destaca os movimentos válidos
            for mov in self.movimentos_validos:
                linha_m, col_m = mov
                centro = (col_m * tamanho_casa + tamanho_casa // 2, linha_m * tamanho_casa + tamanho_casa // 2)
                pygame.draw.circle(self.tela, (0, 255, 0), centro, 10)

    def mostrar_mensagem(self, mensagem):
        self.mensagem = mensagem
        print(mensagem)  # para debug também
