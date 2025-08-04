import pygame, time
from .ui_base import UIBase
from .tabuleiro import Tabuleiro, Dama
from .cores import PRETO, BRANCO, VERMELHO, VERDE, AZUL

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

        # ⏱️ Cronômetros iniciam em 5 minutos (300 segundos)
        self.tempo_branco = 300.0
        self.tempo_preto = 300.0

        self.inicio_turno = None
        self.turno_atual = None

    def desenhar_cronometros(self):
        # Exibir minutos e segundos no formato mm:ss
        def formatar_tempo(segundos):
            if segundos < 0:
                segundos = 0
            m = int(segundos) // 60
            s = int(segundos) % 60
            return f"{m:02d}:{s:02d}"

        texto_b = self.fonte.render(f"Brancas: {formatar_tempo(self.tempo_branco)}", True, BRANCO)
        texto_p = self.fonte.render(f"Pretas: {formatar_tempo(self.tempo_preto)}", True, BRANCO)

        self.tela.blit(texto_b, (10, 10))
        self.tela.blit(texto_p, (10, 40))

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
        # Ao iniciar a leitura do movimento, define o turno atual e registra o tempo inicial
        if self.turno_atual != turno:
            # mudou o turno, atualiza o tempo do turno anterior antes de trocar
            self.atualizar_tempo_turno()
            self.turno_atual = turno
            self.inicio_turno = time.time()
        elif self.inicio_turno is None:
            self.inicio_turno = time.time()

        origem = None
        destino = None

        while True:
            # Atualiza o cronômetro a cada loop
            self.atualizar_tempo_turno()

            # Se algum jogador zerar o tempo, encerra o jogo (retornando None, None)
            if self.tempo_branco <= 0:
                self.mostrar_mensagem("Tempo esgotado! Jogador das Brancas perdeu!")
                return None, None
            if self.tempo_preto <= 0:
                self.mostrar_mensagem("Tempo esgotado! Jogador das Pretas perdeu!")
                return None, None

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

                            # Atualiza tempo antes de finalizar o movimento
                            self.atualizar_tempo_turno()
                            self.inicio_turno = None  # Pausa o cronômetro até o próximo turno

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

    def atualizar_tempo_turno(self):
        if self.inicio_turno is None or self.turno_atual is None:
            return

        tempo_agora = time.time()
        tempo_passado = tempo_agora - self.inicio_turno

        if self.turno_atual == 'B':
            self.tempo_branco -= tempo_passado
        else:
            self.tempo_preto -= tempo_passado

        self.inicio_turno = tempo_agora  # reinicia o timer para próxima medição

    # O método ler_movimento_continuacao deve usar o mesmo sistema para o tempo
    def ler_movimento_continuacao(self, origem):
        self.selecionado = origem
        self.movimentos_validos = self.tabuleiro.movimentos_validos_para_peca(origem)

        if self.inicio_turno is None:
            self.inicio_turno = time.time()

        while True:
            # Atualiza o cronômetro a cada loop
            self.atualizar_tempo_turno()

            # Verifica se tempo acabou
            if self.tempo_branco <= 0:
                self.mostrar_mensagem("Tempo esgotado! Jogador das Brancas perdeu!")
                return None
            if self.tempo_preto <= 0:
                self.mostrar_mensagem("Tempo esgotado! Jogador das Pretas perdeu!")
                return None

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
                        self.inicio_turno = None  # Pausa o cronômetro após movimento continuar
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
        print(mensagem)  # Você pode imprimir no console também
