# Importa as bibliotecas necessárias
import asyncio
import pygame
from config import *
from src.objects.player_mable import Player
from src.utils.asset_loader import load_image
from src.objects.platforma_level1 import Platform
from src.objects.gnomo_inimigo import GnomoInimigo
from src.objects.porquinho import Porquinho
from src.utils.virtual_controller import VirtualXboxController

from src.screens.pause_screen import PauseScreen
from src.screens.game_over import tela_game_over
from src.screens.winner import tela_vitoria

# Função principal que executa o nível do jogo
async def run(screen):
    # Inicializa o mixer de som e carrega a música de fundo
    pygame.mixer.init()
    pygame.mixer.music.load("assets/sounds/som-level1.ogg")
    pygame.mixer.music.set_volume(SOUND_VOLUME_MUSIC)
    pygame.mixer.music.play(-1)  # -1 = toca em loop infinito

    clock = pygame.time.Clock()
    pygame.font.init()
    font_porcos = pygame.font.SysFont("arial", 24)

    # Cria o jogador e define que ele não está no chão
    player = Player(100, HEIGHT - 350)
    player.on_ground = False

    # Inicializa o joystick (caso exista)
    joystick = None
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    virtual_controller = VirtualXboxController(screen, joystick)

    # Variáveis de vida e imagens da interface
    lives = 8
    heart_image = load_image("level_3/vida.png", size=(32, 32))
    porco_icon = load_image("porco1.png", size=("auto", 35))

    # Carrega e redimensiona o plano de fundo
    background = load_image("mabel/imagem level 1.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Carrega o arco-íris e define sua posição
    rainbow_image = load_image("rainbow_large_from_original.png")
    rainbow_image = pygame.transform.scale(rainbow_image, (300, 200))
    rainbow_rect = rainbow_image.get_rect(midtop=(screen_width // 2, 0))
    arco_rect = rainbow_rect

    # Cria o grupo de plataformas
    platforms = pygame.sprite.Group()

    platform_surface = load_image("mabel/plataforma3_limpa.png")
    small_w, small_h = 50, 30
    large_w, large_h = 180, 60

    # Cria e adiciona plataformas ao grupo
    platform2 = Platform(pygame.transform.scale(platform_surface, (large_w, large_h)), screen_width - large_w - 60, HEIGHT - 180)
    platform3 = Platform(pygame.transform.scale(platform_surface, (large_w, large_h)), screen_width // 2 - large_w // 2, HEIGHT - 260)
    platform4 = Platform(pygame.transform.scale(platform_surface, (large_w, large_h)), 60, HEIGHT - 180)

    platforms.add(platform2, platform3, platform4)

    # Verifica colisão inicial com plataformas
    for plat in platforms:
        if player.rect.colliderect(plat.rect):
            player.rect.bottom = plat.rect.top
            player.vel_y = 0
            player.on_ground = True
            break

    # Grupo de inimigos gnomo
    gnomo_group = pygame.sprite.Group()
    last_gnomo_spawn = pygame.time.get_ticks()
    intervalo_gnomo = 1400  # tempo entre cada gnomo (ms)

    # Grupo de porquinhos coletáveis
    porcos_group = pygame.sprite.Group()
    coletados = 0
    last_spawn_time = pygame.time.get_ticks()
    intervalo_spawn = 4000  # tempo entre spawns de porquinho (ms)

    # Tela de pausa
    pause_screen = PauseScreen(screen)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Delta time (segundos)

        # Eventos do jogo
        for event in pygame.event.get():
            virtual_controller.handle_event(event)
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return 'quit'
            if pause_screen.active:
                action = pause_screen.handle_event(event)
                pygame.mixer.music.pause()
                if action == 'continue':
                    pygame.mixer.music.unpause()
                    pause_screen.hide()
                elif action == 'menu':
                    pygame.mixer.music.stop()
                    return 'menu'
                elif action == 'level_select':
                    pygame.mixer.music.stop()
                    return 'level_select'
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause_screen.show()
                elif event.type == pygame.JOYBUTTONDOWN and event.button == 7:
                    pause_screen.show()
                elif virtual_controller.consume_pause():
                    pause_screen.show()

        # Atualiza a tela de pausa se ativa
        if pause_screen.active:
            pause_screen.update(dt)
            screen.blit(background, (0, 0))
            platforms.update()
            for p in platforms:
                p.draw(screen)
            player.draw(screen)
            pause_screen.draw()
            pygame.display.flip()
            await asyncio.sleep(0)
            continue

        # Atualiza jogador com teclado e joystick
        keys = pygame.key.get_pressed()
        player.update(keys, virtual_controller)

        now = pygame.time.get_ticks()

        # Spawn de porquinho após intervalo
        if now - last_spawn_time > intervalo_spawn:
            import random
            spawnou = False
            plataformas_lista = list(platforms)
            random.shuffle(plataformas_lista)
            for plat in plataformas_lista:
                porco = Porquinho()
                porco.rect.midbottom = (random.randint(plat.rect.left + 10, plat.rect.right - 10), plat.rect.top)
                porcos_group.add(porco)
                spawnou = True
                break
            if not spawnou:
                porco = Porquinho()
                porco.rect.midbottom = (random.randint(50, screen_width - 50), HEIGHT)
                porcos_group.add(porco)
            last_spawn_time = now

        # Spawn de gnomo após intervalo
        if now - last_gnomo_spawn > intervalo_gnomo:
            novo_gnomo = GnomoInimigo(arco_rect, player, platforms)
            gnomo_group.add(novo_gnomo)
            last_gnomo_spawn = now

        # Verifica colisão com porquinhos
        colididos = pygame.sprite.spritecollide(player, porcos_group, True)
        coletados += len(colididos)
        if coletados >= 20:
            pygame.mixer.music.stop()
            result = await tela_vitoria(screen)
            if result == 'menu':
                return 'menu'

        # Verifica colisão com gnomos
        for gnomo in gnomo_group.copy():
            if player.rect.colliderect(gnomo.rect):
                gnomo_group.remove(gnomo)
                lives -= 1
                if lives <= 0:
                    pygame.mixer.music.stop()
                    result = await tela_game_over(screen)
                    if result == 'menu':
                        return 'menu'
                    elif result == 'level_select':
                        return 'level_select' 

        # Mantém jogador dentro da tela
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > screen_width:
            player.rect.right = screen_width
        if player.rect.top < 0:
            player.rect.top = 0
        if player.rect.bottom > screen_height:
            player.rect.bottom = screen_height
            player.vel_y = 0
            player.on_ground = True

        # Se jogador estiver no chão (sem colidir com plataforma)
        if player.rect.bottom == screen_height and not any(player.rect.colliderect(p.rect) for p in platforms):
            player.on_ground = True

        # Verifica colisão com plataformas (pouso)
        collided = False
        for plat in platforms:
            if player.vel_y > 0:
                tolerance = 10
                if (
                    player.rect.bottom <= plat.rect.top + tolerance and
                    player.rect.bottom + player.vel_y >= plat.rect.top and
                    player.rect.right > plat.rect.left + 5 and
                    player.rect.left < plat.rect.right - 5
                ):
                    player.rect.bottom = plat.rect.top
                    player.vel_y = 0
                    player.on_ground = True
                    collided = True
                    break

        if not collided and player.rect.bottom < screen_height:
            player.on_ground = False

        # Atualiza gnomos e porquinhos
        gnomo_group.update()
        porcos_group.update()

        # Renderiza elementos na tela
        screen.blit(background, (0, 0))
        screen.blit(rainbow_image, rainbow_rect)
        for p in platforms:
            p.draw(screen)
        player.draw(screen)
        gnomo_group.draw(screen)
        porcos_group.draw(screen)

        virtual_controller.draw()

        # Desenha corações de vida
        for i in range(lives):
            screen.blit(heart_image, (WIDTH - (i + 1) * 40, 20))

        # Exibe ícone e contagem de porquinhos
        screen.blit(porco_icon, (20, 20))
        texto_porcos = font_porcos.render(f"[{coletados}]", True, (255, 255, 0))
        screen.blit(texto_porcos, (80, 30))

        pygame.display.flip()
        await asyncio.sleep(0)
