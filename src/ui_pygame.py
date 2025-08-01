import pygame
from .ui_base import UIBase
from .tabuleiro import Tabuleiro, Peao, Dama

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)
CINZA = (100, 100, 100)
BEGE = (240, 217, 181)
MARROM = (181, 136, 99)
AZUL = (0, 0, 255)
SELECAO_COR = (0, 255, 0, 100)  # Verde translúcido para seleção

TAMANHO_CASA = 80
TAMANHO_JANELA = TAMANHO_CASA * 8

class UIPygame(UIBase):
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((TAMANHO_JANELA, TAMANHO_JANELA))
        pygame.display.set_caption("Jogo de Damas")
        self.fonte = pygame.font.SysFont("arial", 24)
        self.tabuleiro = Tabuleiro()

        self.selecionado = None
        self.movimentos_validos = []

        self.rodando = True
        self.mensagem = ""

    def desenhar_tabuleiro(self):
        for linha in range(8):
            for col in range(8):
                cor = BEGE if (linha + col) % 2 == 0 else MARROM
                pygame.draw.rect(self.tela, cor, (col*TAMANHO_CASA, linha*TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA))

    def desenhar_pecas(self):
        for linha in range(8):
            for col in range(8):
                peca = self.tabuleiro.tabuleiro[linha][col]
                if peca:
                    cor = BRANCO if peca.cor == 'B' else PRETO
                    centro = (col * TAMANHO_CASA + TAMANHO_CASA//2, linha * TAMANHO_CASA + TAMANHO_CASA//2)
                    pygame.draw.circle(self.tela, cor, centro, 30)

                    if isinstance(peca, Dama):
                        pygame.draw.circle(self.tela, VERMELHO, centro, 34, 3)

    def desenhar_selecao(self):
        if self.selecionado:
            linha, col = self.selecionado
            rect = pygame.Rect(col*TAMANHO_CASA, linha*TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA)
            pygame.draw.rect(self.tela, AZUL, rect, 4)

            # Destacar movimentos válidos
            for mov in self.movimentos_validos:
                linha_m, col_m = mov
                centro = (col_m * TAMANHO_CASA + TAMANHO_CASA//2, linha_m * TAMANHO_CASA + TAMANHO_CASA//2)
                pygame.draw.circle(self.tela, AZUL, centro, 15, 3)

    def mostrar_mensagem(self, mensagem):
        self.mensagem = mensagem
        print(mensagem)  # também imprime no console para debug

    def desenhar_mensagem(self):
        if self.mensagem:
            texto = self.fonte.render(self.mensagem, True, VERMELHO)
            self.tela.blit(texto, (10, TAMANHO_JANELA - 30))

    def pos_click_para_casa(self, pos):
        x, y = pos
        linha = y // TAMANHO_CASA
        col = x // TAMANHO_CASA
        if 0 <= linha < 8 and 0 <= col < 8:
            return (linha, col)
        return None

    def ler_movimento(self, turno):
        self.selecionado = None
        self.movimentos_validos = []
        origem = None
        destino = None

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None, None
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_casa = self.pos_click_para_casa(evento.pos)
                    if pos_casa is None:
                        continue

                    if origem is None:
                        peca = self.tabuleiro.obter_peca(pos_casa)
                        movimentos_validos = self.tabuleiro.movimentos_validos_para_peca(pos_casa)
                        if peca and peca.cor == turno and movimentos_validos:
                            origem = pos_casa
                            self.selecionado = origem
                            self.movimentos_validos = movimentos_validos
                            self.mostrar_mensagem(f"Peça selecionada em {origem}. Escolha destino.")
                        else:
                            self.mostrar_mensagem("Selecione uma peça sua que tenha movimentos válidos.")

                    else:
                        if pos_casa in self.movimentos_validos:
                            destino = pos_casa
                            self.selecionado = None
                            self.movimentos_validos = []
                            self.mostrar_mensagem("")
                            return origem, destino
                        else:
                            self.mostrar_mensagem("Destino inválido. Escolha um movimento válido.")

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
                    return None
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