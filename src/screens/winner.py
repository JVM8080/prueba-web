import asyncio
import pygame
import os
from config import *
from pygame import mixer

# Função que exibe a tela de vitória com animação e música
async def tela_vitoria(screen):
    # Carrega e configura o som de vitória
    VITORIA_SOUND = mixer.Sound("assets/sounds/resultados/victory.ogg")
    VITORIA_SOUND.set_volume(SOUND_VOLUME_MUSIC)
    canal_vitoria = pygame.mixer.Channel(1)  # Usa o canal 1 do mixer
    canal_vitoria.play(VITORIA_SOUND, loops=-1)  # Toca o som em loop

    # Carrega os frames da animação da vitória
    frames = []
    folder = "assets/images/level2/gif.winner"  # Pasta com os frames da animação

    # Percorre todos os arquivos da pasta ordenadamente
    for filename in sorted(os.listdir(folder)):
        # Verifica se o arquivo é uma imagem válida
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            # Carrega a imagem e redimensiona para o tamanho da tela
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            frames.append(img)  # Adiciona à lista de frames

    frame_index = 0             # Índice atual do frame
    frame_speed = 150           # Velocidade da animação (ms por frame)
    last_update = pygame.time.get_ticks()  # Tempo da última atualização

    clock = pygame.time.Clock()  # Relógio para controle de FPS

    # Loop principal da tela de vitória
    while True:
        # Lida com os eventos (teclado, mouse, sair)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    canal_vitoria.stop()  # Para a música
                    return 'menu'         # Volta para o menu

        # Atualiza o frame da animação se já passou tempo suficiente
        now = pygame.time.get_ticks()
        if now - last_update > frame_speed:
            frame_index = (frame_index + 1) % len(frames)  # Vai para o próximo frame
            last_update = now

        # Desenha o frame atual na tela
        screen.blit(frames[frame_index], (0, 0))
        pygame.display.flip()  # Atualiza a tela
        clock.tick(FPS)
        await asyncio.sleep(0)
