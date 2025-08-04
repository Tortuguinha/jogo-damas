import pygame, time
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
SELECAO_COR = (0, 255, 0, 100)

TAMANHO_CASA = 80
TAMANHO_JANELA = TAMANHO_CASA * 8

class UIPygame(UIBase):
    def __init__(self, tabuleiro):
        super().__init__(tabuleiro)
        pygame.init()
        self.tela = pygame.display.set_mode((640, 640))
        pygame.display.set_caption("Jogo de Damas")
        self.fonte = pygame.font.SysFont("arial", 24)

        self.selecionado = None
        self.movimentos_validos = []
        self.rodando = True
        self.mensagem = ""

        # ⏱️ Cronômetros
        self.tempo_branco = 0
        self.tempo_preto = 0
        self.inicio_turno = None
        self.turno_atual = None

    def desenhar_cronometros(self):
        tempo_b = int(self.tempo_branco)
        tempo_p = int(self.tempo_preto)

        texto_b = self.fonte.render(f"Brancas: {tempo_b}s", True, BRANCO)
        texto_p = self.fonte.render(f"Pretas: {tempo_p}s", True, BRANCO)

        self.tela.blit(texto_b, (10, 10))
        self.tela.blit(texto_p, (10, 40))

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

            for mov in self.movimentos_validos:
                linha_m, col_m = mov
                centro = (col_m * TAMANHO_CASA + TAMANHO_CASA//2, linha_m * TAMANHO_CASA + TAMANHO_CASA//2)
                pygame.draw.circle(self.tela, AZUL, centro, 15, 3)

    def mostrar_mensagem(self, mensagem):
        self.mensagem = mensagem
        print(mensagem)

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
        self.inicio_turno = time.time()
        self.turno_atual = turno
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

                            # ⏱️ Finaliza tempo do turno
                            if self.inicio_turno:
                                tempo_passado = time.time() - self.inicio_turno
                                if self.turno_atual == 'B':
                                    self.tempo_branco += tempo_passado
                                else:
                                    self.tempo_preto += tempo_passado
                                self.inicio_turno = None

                            return origem, destino
                        else:
                            self.mostrar_mensagem("Movimento inválido. Escolha um destino válido.")

            self.tela.fill(PRETO)
            self.desenhar_tabuleiro()
            self.desenhar_pecas()
            self.desenhar_selecao()
            self.desenhar_mensagem()
            self.desenhar_cronometros()
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
            self.desenhar_cronometros()
            pygame.display.flip()
