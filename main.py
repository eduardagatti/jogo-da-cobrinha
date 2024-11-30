import pygame
import random

# Inicialização do Pygame e configuração da janela do jogo
pygame.init()
pygame.display.set_caption("Jogo da Cobrinha")
largura, altura = 1000, 600  # Definição do tamanho da tela de jogo
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()  # Controle de FPS do jogo

# Definição de paleta de cores utilizadas no jogo (formato RGB)
preto = (0, 0, 0)  # Cor de fundo
branco = (255, 255, 255)  # Cor da cobra
verde = (0, 255, 0)  # Cor do texto e elementos de destaque
vermelho = (255, 0, 0)  # Cor de game over
amarelo = (255, 255, 0)  # Cor de seleção e destaque

# Configurações de jogo
tamanho_quadrado = 20  # Tamanho de cada segmento da cobra
velocidade_cobrinha = 10  # Velocidade de movimento da cobra

# Armazenamento de recordes dos jogadores
historico_pontuacoes = {}  # Dicionário para salvar pontuações máximas

# Funções auxiliares de renderização e geração de elementos


def desenhar_texto(texto, fonte, cor, x, y, centralizado=False):
    """
    Renderiza texto na tela com opção de centralização.

    Args:
        texto (str): Texto a ser renderizado
        fonte (pygame.font.Font): Fonte utilizada
        cor (tuple): Cor do texto em RGB
        x (int): Posição x inicial
        y (int): Posição y inicial
        centralizado (bool): Centraliza o texto se True
    """
    tela_texto = fonte.render(
        texto, False, cor)  # Renderização sem antialiasing
    if centralizado:
        x -= tela_texto.get_width() // 2
    tela.blit(tela_texto, (x, y))


def gerar_comida():
    """
    Gera coordenadas aleatórias para a comida dentro da tela.

    Returns:
        tuple: Coordenadas x e y da comida
    """
    comida_x = round(random.randrange(
        0, largura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado
    comida_y = round(random.randrange(
        0, altura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado
    return comida_x, comida_y


def desenhar_cobrinha(tamanho, pixels):
    """
    Desenha a cobra na tela baseado em seus pixels/segmentos.

    Args:
        tamanho (int): Tamanho de cada segmento
        pixels (list): Lista de coordenadas dos segmentos da cobra
    """
    for pixel in pixels:
        pygame.draw.rect(tela, branco, [pixel[0], pixel[1], tamanho, tamanho])


def selecionar_velocidade(tecla, direcao_atual):
    """
    Determina a nova direção da cobra baseado na tecla pressionada.

    Args:
        tecla (int): Tecla pressionada
        direcao_atual (str): Direção atual da cobra

    Returns:
        tuple: Velocidade x, velocidade y e nova direção
    """
    if tecla in (pygame.K_DOWN, pygame.K_s) and direcao_atual != "CIMA":
        return 0, tamanho_quadrado, "BAIXO"
    elif tecla in (pygame.K_UP, pygame.K_w) and direcao_atual != "BAIXO":
        return 0, -tamanho_quadrado, "CIMA"
    elif tecla in (pygame.K_RIGHT, pygame.K_d) and direcao_atual != "ESQUERDA":
        return tamanho_quadrado, 0, "DIREITA"
    elif tecla in (pygame.K_LEFT, pygame.K_a) and direcao_atual != "DIREITA":
        return -tamanho_quadrado, 0, "ESQUERDA"
    return None

# Estados do jogo


def menu():
    fonte_titulo = pygame.font.SysFont("Pxlvetica", 70)
    fonte_menu = pygame.font.SysFont("Pxlvetica", 30)
    opcoes = ["JOGAR", "VER RECORDES", "SAIR"]
    opcao_selecionada = 0
    rodando = True
    nickname = ""
    contador_pisca = 0  # Para alternar a barrinha piscante

    while rodando:
        tela.fill(preto)

        # Desenhar o título
        desenhar_texto("SNAKE GAME", fonte_titulo, verde,
                       largura // 2, 80, centralizado=True)

        # Desenhar as opções do menu
        for i, opcao in enumerate(opcoes):
            cor = amarelo if i == opcao_selecionada else branco
            desenhar_texto(opcao, fonte_menu, cor, largura //
                           2, 200 + i * 50, centralizado=True)

        # Mostrar campo de nickname se "JOGAR" for selecionado
        if opcao_selecionada == 0:
            desenhar_texto("DIGITE SEU NICKNAME:", fonte_menu, branco,
                           largura // 2, 200 + len(opcoes) * 50, centralizado=True)

            # Nickname digitado
            desenhar_texto(nickname, fonte_menu, amarelo, largura //
                           2, 200 + len(opcoes) * 50 + 40, centralizado=True)

            # Barrinha piscante
            if contador_pisca < 50:  # Pisca a cada meio segundo (60 FPS)
                largura_barra = 3
                altura_texto = fonte_menu.size(nickname)[1]
                pygame.draw.rect(
                    tela,
                    amarelo,
                    [
                        largura // 2 +
                        fonte_menu.size(nickname)[0] // 2 + 5,  # Posição x
                        200 + len(opcoes) * 50 + 40 + \
                        (altura_texto // 4),  # Posição y ajustada
                        largura_barra,
                        altura_texto // 1.7,  # Altura reduzida para se alinhar melhor
                    ],
                )

            contador_pisca = (contador_pisca + 1) % 60

        # Desenhar a seta retrô à esquerda da opção selecionada
        pygame.draw.polygon(
            tela,
            amarelo,
            [
                (largura // 2 - 120, 215 + opcao_selecionada * 50),  # Ponta da seta
                (largura // 2 - 130, 210 + opcao_selecionada * 50),  # Canto superior
                (largura // 2 - 130, 220 + opcao_selecionada * 50),  # Canto inferior
            ],
        )

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                elif evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                elif evento.key == pygame.K_RETURN:
                    if opcao_selecionada == 0:  # Jogar
                        if nickname.strip():  # Só começa se o nickname for válido
                            return nickname
                    elif opcao_selecionada == 1:  # Ver Recordes
                        mostrar_recordes()
                    elif opcao_selecionada == 2:  # Sair
                        pygame.quit()
                        quit()
                elif opcao_selecionada == 0 and evento.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                elif opcao_selecionada == 0:
                    nickname += evento.unicode

        pygame.display.update()


def mostrar_recordes():
    fonte = pygame.font.SysFont("Pxlvetica", 30)
    rodando = True

    while rodando:
        tela.fill(preto)
        desenhar_texto("RECORDES", pygame.font.SysFont(
            "Pxlvetica", 40), verde, largura // 2, 50, centralizado=True)

        # Organizar os recordes em ordem decrescente
        recordes_ordenados = sorted(
            historico_pontuacoes.items(), key=lambda x: x[1], reverse=True)
        y_offset = 120

        if recordes_ordenados:
            # Limita a 10 jogadores
            for i, (jogador, pontuacao) in enumerate(recordes_ordenados[:10], start=1):
                texto = f"{i}º - {jogador}: {pontuacao} pontos"
                desenhar_texto(texto, fonte, branco, largura //
                               2, y_offset, centralizado=True)
                y_offset += 40
        else:
            desenhar_texto("Nenhum recorde registrado ainda.", fonte,
                           amarelo, largura // 2, y_offset, centralizado=True)

        desenhar_texto("Pressione M para voltar ao menu", fonte,
                       vermelho, largura // 2, altura - 50, centralizado=True)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_m:
                rodando = False

        pygame.display.update()


def game_over(nickname, pontos):
    fonte = pygame.font.SysFont("Pxlvetica", 40)
    rodando = True

    # Atualiza o recorde
    record = historico_pontuacoes.get(nickname, 0)
    if pontos > record:
        historico_pontuacoes[nickname] = pontos

    while rodando:
        tela.fill(preto)
        desenhar_texto("GAME OVER", fonte, vermelho,
                       largura // 2, 100, centralizado=True)
        desenhar_texto(f"Sua Pontuação: {
                       pontos}", fonte, branco, largura // 2, 200, centralizado=True)
        desenhar_texto(f"Seu Recorde: {
                       historico_pontuacoes[nickname]}", fonte, amarelo, largura // 2, 250, centralizado=True)
        desenhar_texto("Pressione R para jogar novamente", fonte,
                       verde, largura // 2, 350, centralizado=True)
        desenhar_texto("Pressione M para voltar ao menu", fonte,
                       verde, largura // 2, 400, centralizado=True)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return "RESTART"
                elif evento.key == pygame.K_m:
                    return "MENU"

        pygame.display.update()


def rodar_jogo(nickname):
    fim_jogo = False

    x = largura / 2
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0
    direcao_atual = None

    tamanho_cobrinha = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill(preto)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                nova_velocidade = selecionar_velocidade(
                    evento.key, direcao_atual)
                if nova_velocidade:
                    velocidade_x, velocidade_y, direcao_atual = nova_velocidade

        if x < 0 or x >= largura or y < 0 or y >= altura:
            break

        x += velocidade_x
        y += velocidade_y

        pixels.append([x, y])
        if len(pixels) > tamanho_cobrinha:
            del pixels[0]

        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fim_jogo = True  # Marca que o jogo terminou
                break

        if fim_jogo:
            break

        desenhar_cobrinha(tamanho_quadrado, pixels)

        if x == comida_x and y == comida_y:
            tamanho_cobrinha += 1
            comida_x, comida_y = gerar_comida()

        pygame.draw.rect(
            tela, verde, [comida_x, comida_y, tamanho_quadrado, tamanho_quadrado])
        desenhar_texto(f"Pontos: {tamanho_cobrinha - 1}",
                       pygame.font.SysFont("Pxlvetica", 30), amarelo, 10, 10)

        pygame.display.update()
        relogio.tick(velocidade_cobrinha)

    return tamanho_cobrinha - 1


def main():
    while True:
        nickname = menu()
        while True:
            pontos = rodar_jogo(nickname)
            acao = game_over(nickname, pontos)
            if acao == "MENU":
                break


main()
