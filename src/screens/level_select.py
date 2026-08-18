import asyncio
import pygame
from pygame import mixer
from config import *

async def level_select(screen):
    # Carrega e toca a música de fundo da tela de seleção de nível em loop
    mixer.music.load("assets/sounds/menu/select level.ogg")
    mixer.music.set_volume(SOUND_VOLUME_MUSIC)
    mixer.music.play(-1)

    # Define a fonte padrão com tamanho 50 (não está sendo usada neste trecho)
    font = pygame.font.SysFont(None, 50)

    # Carrega e redimensiona a imagem de fundo da tela de seleção de nível
    background = pygame.image.load("assets/images/menu/level select.png").convert()
    background = pygame.transform.scale(background, screen.get_size())

    # Carrega as imagens dos botões de seleção de nível
    button_images = [
        pygame.image.load("assets/images/menu/level 1.png").convert_alpha(),
        pygame.image.load("assets/images/menu/level 2.png").convert_alpha(),
        pygame.image.load("assets/images/menu/level 3.png").convert_alpha()
    ]

    # Redimensiona as imagens dos botões para 180x60 pixels
    button_images = [pygame.transform.scale(img, (180, 60)) for img in button_images]

    # Define as posições (x, y) onde cada botão será exibido na tela
    positions = [(80, 430), (300, 400), (520, 370)]  # x, y de cada botão

    # Cria uma lista com os retângulos (áreas clicáveis) de cada botão
    level_buttons = []
    for i, img in enumerate(button_images):
        rect = img.get_rect(topleft=positions[i])
        level_buttons.append(rect)

    # Loop principal da tela de seleção de nível
    while True:
        # Desenha o fundo
        screen.blit(background, (0, 0))

        # Desenha os botões dos níveis nas suas respectivas posições
        for i, rect in enumerate(level_buttons):
            screen.blit(button_images[i], rect.topleft)

        # Processa os eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit', 1  # Sai do jogo
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se algum botão de nível foi clicado
                for i, rect in enumerate(level_buttons):
                    if rect.collidepoint(event.pos):
                        mixer.music.stop()  # Para a música
                        return 'game', i + 1  # Vai para o nível selecionado

        # Atualiza a tela
        pygame.display.flip()
        await asyncio.sleep(0)
