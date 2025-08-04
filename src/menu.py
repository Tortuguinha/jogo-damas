import pygame
import sys

# Cores
CINZA_ESCURO = (40, 40, 40)
BRANCO = (255, 255, 255)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)
VERDE_CLARO = (0, 255, 0)
VERMELHO_CLARO = (255, 50, 50)

def desenhar_botao(tela, texto, fonte, cor_base, cor_hover, rect, mouse_pos):
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(tela, cor_hover, rect)
    else:
        pygame.draw.rect(tela, cor_base, rect)

    texto_render = fonte.render(texto, True, BRANCO)
    texto_rect = texto_render.get_rect(center=rect.center)
    tela.blit(texto_render, texto_rect)

def mostrar_menu():
    pygame.init()
    tela = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Menu - Jogo de Damas")
    fonte = pygame.font.SysFont("arial", 36)

    # Botões
    botao_iniciar = pygame.Rect(220, 250, 200, 60)
    botao_sair = pygame.Rect(220, 350, 200, 60)

    while True:
        tela.fill(CINZA_ESCURO)
        mouse_pos = pygame.mouse.get_pos()

        # Título
        titulo = fonte.render("Jogo de Damas", True, BRANCO)
        tela.blit(titulo, (200, 150))

        # Botões
        desenhar_botao(tela, "Iniciar Jogo", fonte, VERDE, VERDE_CLARO, botao_iniciar, mouse_pos)
        desenhar_botao(tela, "Sair", fonte, VERMELHO, VERMELHO_CLARO, botao_sair, mouse_pos)

        pygame.display.flip()

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
