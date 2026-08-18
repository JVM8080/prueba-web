import asyncio
import pygame
from src.utils.asset_loader import load_image
from pygame import mixer
from config import *


async def main_menu(screen):
    # Carrega e toca a música de fundo do menu em loop
    mixer.music.load("assets/sounds/menu/introducao.ogg")
    mixer.music.set_volume(SOUND_VOLUME_MUSIC)
    mixer.music.play(-1)  # -1 = loop infinito

    # Cria um objeto Clock para controlar o FPS do menu
    clock = pygame.time.Clock()

    # Carrega a imagem de fundo do menu e redimensiona para caber na tela
    background = load_image("inicio_menu.jpg")
    background = pygame.transform.scale(background, screen.get_size())

    # Tenta carregar a fonte personalizada; se falhar, usa uma fonte padrão do sistema
    try:
        font = pygame.font.Font("src/assets/fonts/GravityFalls.ttf", 36)
    except:
        font = pygame.font.SysFont("comicsansms", 36)

    # Define algumas cores usadas no menu
    white = (255, 255, 255)
    yellow = (255, 255, 0)
    hover_yellow = (255, 255, 102)
    black = (0, 0, 0)

    # Define o texto e o retângulo do botão "Iniciar Jogo"
    button_text = "Iniciar Jogo"
    button_rect = pygame.Rect(0, 0, 240, 80)
    button_rect.center = (screen.get_width() // 2, 420)

    running = True
    while running:
        # Captura a posição atual do mouse
        mouse_pos = pygame.mouse.get_pos()

        # Verifica os eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"  # Sai do jogo
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Verifica se o clique foi dentro do botão
                if button_rect.collidepoint(mouse_pos):
                    mixer.music.stop()  # Para a música
                    return "level_select"  # Vai para a tela de seleção de nível

        # Desenha a imagem de fundo
        screen.blit(background, (0, 0))

        # Altera a cor do botão se o mouse estiver sobre ele
        color = hover_yellow if button_rect.collidepoint(mouse_pos) else yellow
        pygame.draw.rect(screen, color, button_rect, border_radius=12)

        # Desenha uma sombra no texto do botão
        shadow = font.render(button_text, True, (50, 50, 50))
        screen.blit(shadow, shadow.get_rect(center=(button_rect.centerx + 2, button_rect.centery + 2)))

        # Desenha o texto principal do botão
        label = font.render(button_text, True, black)
        screen.blit(label, label.get_rect(center=button_rect.center))

        # Atualiza a tela
        pygame.display.flip()

        # Controla o FPS do menu (60 quadros por segundo)
        clock.tick(FPS)
        await asyncio.sleep(0)
