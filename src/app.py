import sys
import pygame
from src.menu import mostrar_menu
from src.menu_regras import mostrar_menu_regras
from src.jogo import Jogo
from src.ui_pygame import UIPygame
from src.tabuleiro import Tabuleiro

def escolher_modo_jogo():
    tela = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Escolha o modo")
    fonte = pygame.font.SysFont(None, 36)
    botao_humano = pygame.Rect(50, 100, 140, 60)
    botao_ia = pygame.Rect(210, 100, 140, 60)

    while True:
        tela.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_humano.collidepoint(evento.pos):
                    return 'humano'
                elif botao_ia.collidepoint(evento.pos):
                    return 'ia'

        # Botão humano
        cor_humano = (70, 130, 180) if botao_humano.collidepoint(mouse_pos) else (50, 110, 160)
        pygame.draw.rect(tela, cor_humano, botao_humano, border_radius=8)

        # Botão IA
        cor_ia = (180, 130, 70) if botao_ia.collidepoint(mouse_pos) else (160, 110, 50)
        pygame.draw.rect(tela, cor_ia, botao_ia, border_radius=8)

        texto_humano = fonte.render("Humano", True, (255, 255, 255))
        texto_ia = fonte.render("IA", True, (255, 255, 255))

        tela.blit(texto_humano, (botao_humano.x + 30, botao_humano.y + 15))
        tela.blit(texto_ia, (botao_ia.x + 60, botao_ia.y + 15))

        pygame.display.flip()


def iniciar_app():
    pygame.init()
    
    if mostrar_menu():
        modo_jogo = escolher_modo_jogo()
        if modo_jogo is None:
            print("Nenhum modo selecionado, encerrando.")
            pygame.quit()
            sys.exit()

        regras = mostrar_menu_regras()
        tabuleiro = Tabuleiro()
        ui = UIPygame(tabuleiro)

        if modo_jogo == "ia":
            jogo = Jogo(ui, tabuleiro, regras, vs_ia=True, cor_ia='P')
        else:
            jogo = Jogo(ui, tabuleiro, regras, vs_ia=False)

        jogo.jogar()
    else:
        print("Menu principal cancelado.")
    
    pygame.quit()
