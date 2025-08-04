import pygame, sys
from src.menu_historico import mostrar_historico_pygame

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
    tela = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Menu Principal")
    fonte = pygame.font.SysFont("Segoe UI", 36)
    relogio = pygame.time.Clock()

    # Exemplo de histórico (substitua pelo seu real)
    historico = [
    ]

    botao_jogar = pygame.Rect(220, 150, 200, 50)
    botao_historico = pygame.Rect(220, 230, 200, 50)
    botao_sair = pygame.Rect(220, 310, 200, 50)

    rodando = True
    while rodando:
        tela.fill(FUNDO)
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    return True
                elif botao_historico.collidepoint(evento.pos):
                    # Passa tela, fonte e histórico para mostrar a tela de histórico
                    mostrar_historico_pygame(tela, fonte, historico)
                elif botao_sair.collidepoint(evento.pos):
                    rodando = False

        # Desenhar botões com efeito hover
        desenhar_botao(tela, "Jogar", fonte, (52, 152, 219), (72, 172, 239), botao_jogar, mouse_pos)
        desenhar_botao(tela, "Histórico", fonte, (52, 152, 219), (72, 172, 239), botao_historico, mouse_pos)
        desenhar_botao(tela, "Sair", fonte, (200, 60, 60), (220, 80, 80), botao_sair, mouse_pos)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    return False
