import pygame
import sys

BRANCO = (240, 240, 240)
FUNDO = (25, 25, 25)
AZUL = (52, 152, 219)
AZUL_CLARO = (116, 185, 255)
VERDE = (46, 204, 113)
VERDE_CLARO = (67, 224, 138)
VERMELHO = (200, 60, 60)

pygame.font.init()
FONTE_TITULO = pygame.font.SysFont("Segoe UI", 36, bold=True)
FONTE_BOTOES = pygame.font.SysFont("Segoe UI", 28)

def desenhar_toggle(tela, fonte, texto, estado, rect, mouse_pos):
    cor_base = AZUL_CLARO if rect.collidepoint(mouse_pos) else AZUL
    pygame.draw.rect(tela, cor_base, rect, border_radius=10)

    # Texto alinhado mais para esquerda para abrir espaço para o círculo
    padding_esquerdo = 20
    texto_render = fonte.render(f"{texto}: {'Sim' if estado else 'Não'}", True, BRANCO)
    texto_rect = texto_render.get_rect(midleft=(rect.left + padding_esquerdo, rect.centery))
    tela.blit(texto_render, texto_rect)

    # Indicador do estado (círculo verde/vermelho no lado direito)
    cor_estado = VERDE if estado else VERMELHO
    raio = 14
    pos_circulo = (rect.right - 30, rect.centery)
    pygame.draw.circle(tela, cor_estado, pos_circulo, raio)

def mostrar_menu_regras():
    pygame.init()
    tela = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Regras - Jogo de Damas")
    relogio = pygame.time.Clock()

    captura_obrigatoria = True
    dama_multi_captura = True
    multiplas_capturas = True

    # Botões maiores para evitar sobreposição das bolinhas
    botao_largura = 460
    botao_altura = 70
    botao_x = (640 - botao_largura) // 2

    botao_captura = pygame.Rect(botao_x, 210, botao_largura, botao_altura)
    botao_dama = pygame.Rect(botao_x, 300, botao_largura, botao_altura)
    botao_multi = pygame.Rect(botao_x, 390, botao_largura, botao_altura)
    botao_comecar = pygame.Rect(botao_x + 70, 520, 300, 70)

    while True:
        tela.fill(FUNDO)
        mouse_pos = pygame.mouse.get_pos()

        titulo = FONTE_TITULO.render("Escolha as Regras", True, BRANCO)
        texto_rect = titulo.get_rect(center=(640 // 2, 120))
        sombra = FONTE_TITULO.render("Escolha as Regras", True, (0, 0, 0))
        sombra_rect = sombra.get_rect(center=(640 // 2 + 2, 120 + 2))
        tela.blit(sombra, sombra_rect)
        tela.blit(titulo, texto_rect)

        desenhar_toggle(tela, FONTE_BOTOES, "Captura obrigatória", captura_obrigatoria, botao_captura, mouse_pos)
        desenhar_toggle(tela, FONTE_BOTOES, "Dama múltiplas capturas", dama_multi_captura, botao_dama, mouse_pos)
        desenhar_toggle(tela, FONTE_BOTOES, "Permitir múltiplas capturas", multiplas_capturas, botao_multi, mouse_pos)

        cor_botao = VERDE_CLARO if botao_comecar.collidepoint(mouse_pos) else VERDE
        pygame.draw.rect(tela, cor_botao, botao_comecar, border_radius=12)
        texto_comecar = FONTE_BOTOES.render("Começar Partida", True, BRANCO)
        texto_comecar_rect = texto_comecar.get_rect(center=botao_comecar.center)
        tela.blit(texto_comecar, texto_comecar_rect)

        pygame.display.flip()
        relogio.tick(60)

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
