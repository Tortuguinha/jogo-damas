import json, os,pygame, sys
from datetime import datetime

ARQUIVO_HISTORICO = "historico_placar.json"
BRANCO = (240, 240, 240)
FUNDO = (25, 25, 25)
AZUL = (52, 152, 219)

def carregar_historico():
    if not os.path.exists(ARQUIVO_HISTORICO):
        return []
    with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_historico(historico):
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)

def adicionar_partida(vencedor, tempo, movimentos):
    historico = carregar_historico()
    partida = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "vencedor": vencedor,
        "tempo": tempo,
        "movimentos": movimentos
    }
    historico.append(partida)
    salvar_historico(historico)

def mostrar_historico_pygame(tela, fonte, historico):
    """
    Mostra o histórico das partidas em uma tela com botão 'Voltar'.
    
    Args:
        tela: a surface do pygame para desenhar.
        fonte: fonte pygame para texto.
        historico: lista de strings com as partidas já jogadas.
    """

    botao_voltar = pygame.Rect(10, 10, 100, 40)
    branco = (255, 255, 255)
    azul = (52, 152, 219)
    preto = (0, 0, 0)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(evento.pos):
                    rodando = False  # sai do histórico e volta ao menu

        tela.fill(preto)

        # Desenha o botão Voltar
        pygame.draw.rect(tela, azul, botao_voltar)
        texto_voltar = fonte.render("Voltar", True, branco)
        texto_rect = texto_voltar.get_rect(center=botao_voltar.center)
        tela.blit(texto_voltar, texto_rect)

        # Desenha o título
        titulo = fonte.render("Histórico de Partidas", True, branco)
        tela.blit(titulo, (150, 20))

        # Desenha o histórico (lista de partidas)
        y_inicio = 80
        espacamento = 30
        for i, partida in enumerate(historico[-15:]):  # mostra só as últimas 15
            texto_partida = fonte.render(partida, True, branco)
            tela.blit(texto_partida, (20, y_inicio + i * espacamento))

        pygame.display.flip()