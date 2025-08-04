import pygame
import sys

# Cores
FUNDO = (30, 30, 30)
BRANCO = (240, 240, 240)
VERDE = (46, 204, 113)
VERDE_CLARO = (67, 224, 138)
VERMELHO = (231, 76, 60)
VERMELHO_CLARO = (250, 105, 95)

pygame.font.init()
FONTE_TITULO = pygame.font.SysFont("Segoe UI", 48, bold=True)
FONTE_BOTOES = pygame.font.SysFont("Segoe UI", 32)

def desenhar_botao(tela, texto, fonte, cor_base, cor_hover, rect, mouse_pos):
    cor = cor_hover if rect.collidepoint(mouse_pos) else cor_base
    pygame.draw.rect(tela, cor, rect, border_radius=12)
    texto_render = fonte.render(texto, True, BRANCO)
    texto_rect = texto_render.get_rect(center=rect.center)
    tela.blit(texto_render, texto_rect)

def mostrar_menu():
    pygame.init()
    tela = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Menu - Jogo de Damas")
    relogio = pygame.time.Clock()

    botao_iniciar = pygame.Rect(220, 280, 200, 70)
    botao_sair = pygame.Rect(220, 380, 200, 70)

    while True:
        tela.fill(FUNDO)
        mouse_pos = pygame.mouse.get_pos()

        titulo = FONTE_TITULO.render("Jogo de Damas", True, BRANCO)
        texto_rect = titulo.get_rect(center=(640 // 2, 150))
        # sombra para profundidade
        sombra = FONTE_TITULO.render("Jogo de Damas", True, (0, 0, 0))
        sombra_rect = sombra.get_rect(center=(640 // 2 + 2, 150 + 2))
        tela.blit(sombra, sombra_rect)
        tela.blit(titulo, texto_rect)

        desenhar_botao(tela, "Iniciar Jogo", FONTE_BOTOES, VERDE, VERDE_CLARO, botao_iniciar, mouse_pos)
        desenhar_botao(tela, "Sair", FONTE_BOTOES, VERMELHO, VERMELHO_CLARO, botao_sair, mouse_pos)

        pygame.display.flip()
        relogio.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.collidepoint(evento.pos):
                    return True
                elif botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
