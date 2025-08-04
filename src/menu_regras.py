import pygame
import sys

BRANCO = (255, 255, 255)
CINZA = (50, 50, 50)
AZUL = (0, 120, 255)
AZUL_CLARO = (100, 180, 255)
VERDE = (0, 200, 0)
VERDE_CLARO = (0, 255, 0)

def desenhar_toggle(tela, fonte, texto, estado, rect, mouse_pos):
    cor = AZUL_CLARO if rect.collidepoint(mouse_pos) else AZUL
    pygame.draw.rect(tela, cor, rect)
    label = f"{texto}: {'Sim' if estado else 'Não'}"
    texto_render = fonte.render(label, True, BRANCO)
    texto_rect = texto_render.get_rect(center=rect.center)
    tela.blit(texto_render, texto_rect)

def mostrar_menu_regras():
    pygame.init()
    tela = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Regras - Jogo de Damas")
    fonte = pygame.font.SysFont("arial", 28)

    # Estados das regras
    captura_obrigatoria = True
    dama_multi_captura = True
    multiplas_capturas = True

    # Botões
    # Botões com largura maior e centralizados
    botao_largura = 400
    botao_altura = 60
    botao_x = (640 - botao_largura) // 2  # centralizado

    botao_captura = pygame.Rect(botao_x, 200, botao_largura, botao_altura)
    botao_dama = pygame.Rect(botao_x, 280, botao_largura, botao_altura)
    botao_multi = pygame.Rect(botao_x, 360, botao_largura, botao_altura)
    botao_comecar = pygame.Rect(botao_x + 50, 460, 300, 60)


    while True:
        tela.fill(CINZA)
        mouse_pos = pygame.mouse.get_pos()

        titulo = fonte.render("Escolha as Regras", True, BRANCO)
        tela.blit(titulo, (200, 120))

        desenhar_toggle(tela, fonte, "Captura obrigatória", captura_obrigatoria, botao_captura, mouse_pos)
        desenhar_toggle(tela, fonte, "Dama c/ múltiplas capturas", dama_multi_captura, botao_dama, mouse_pos)
        desenhar_toggle(tela, fonte, "Permitir múltiplas capturas", multiplas_capturas, botao_multi, mouse_pos)

        pygame.draw.rect(tela, VERDE_CLARO if botao_comecar.collidepoint(mouse_pos) else VERDE, botao_comecar)
        texto_comecar = fonte.render("Começar Partida", True, BRANCO)
        tela.blit(texto_comecar, texto_comecar.get_rect(center=botao_comecar.center))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_captura.collidepoint(evento.pos):
                    captura_obrigatoria = not captura_obrigatoria
                elif botao_dama.collidepoint(evento.pos):
                    dama_multi_captura = not dama_multi_captura
                elif botao_multi.collidepoint(evento.pos):
                    multiplas_capturas = not multiplas_capturas
                elif botao_comecar.collidepoint(evento.pos):
                    return {
                        "captura_obrigatoria": captura_obrigatoria,
                        "dama_multi_captura": dama_multi_captura,
                        "multiplas_capturas": multiplas_capturas
                    }
