import asyncio
import pygame
from config import *
from pygame import mixer

# Variável global para armazenar o som de game over
GAMEOVER_SOUND = None  

# Função que exibe a tela de "Game Over"
async def tela_game_over(screen):
    global GAMEOVER_SOUND

    # Carrega o som de game over apenas uma vez (lazy loading)
    if not GAMEOVER_SOUND:
        GAMEOVER_SOUND = mixer.Sound("assets/sounds/resultados/gameover.ogg")
        GAMEOVER_SOUND.set_volume(SOUND_VOLUME_MUSIC)

    # Usa o canal 2 para tocar o som em loop infinito
    canal_gameover = pygame.mixer.Channel(2)
    canal_gameover.play(GAMEOVER_SOUND, loops=-1)

    # Carrega e redimensiona a imagem de Game Over para ocupar toda a tela
    gameover_img = pygame.image.load("assets/images/GameOver.png").convert_alpha()
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    # Loop principal da tela de Game Over
    while True:
        for event in pygame.event.get():
            # Encerra o jogo se o jogador clicar em fechar a janela
            if event.type == pygame.QUIT:
                return "quit"
            # Se o jogador pressionar ESC, para a música e retorna ao menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    canal_gameover.stop()
                    return 'menu'

        # Exibe a imagem de Game Over na tela
        screen.blit(gameover_img, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)
