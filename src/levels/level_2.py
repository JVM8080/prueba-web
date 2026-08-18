# Importa os módulos e classes necessárias
import asyncio
import pygame
import os
from src.objects.player_stan import Player
from src.objects.platforms import Platform
from config import *
from src.utils.asset_loader import load_image
from src.objects.animation import *
from src.objects.decoration import *
import random
from src.screens.game_over import tela_game_over
from src.screens.pause_screen import PauseScreen
from src.utils.virtual_controller import VirtualXboxController

# Função principal que executa o segundo nível do jogo
async def run(screen):
    # Inicia o mixer para sons
    pygame.mixer.init()
    pygame.mixer.music.load("assets/sounds/level2_audio/level2.ogg")
    pygame.mixer.music.set_volume(SOUND_VOLUME_MUSIC)  # Define o volume da música
    pygame.mixer.music.play(-1)  # Toca a música em loop infinito
    som_morte = pygame.mixer.Sound("assets/sounds/level2_audio/stan_death.ogg")
    som_morte.set_volume(SOUND_VOLUME_SFX)  

    clock = pygame.time.Clock()  # Relógio para controlar FPS
    player = Player(100, HEIGHT - 150)  # Cria o jogador na posição inicial

    pygame.font.init()
    fonte_sacos = pygame.font.SysFont('arial', 40, bold=True)
    icone_dinheiro = pygame.image.load("assets/images/level2/money_bag.png").convert_alpha()
    icone_dinheiro = pygame.transform.scale(icone_dinheiro, (90, 90))  # Ícone do contador de sacos

    # Inicializa o joystick, se disponível
    joystick = None
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    
    virtual_controller = VirtualXboxController(screen, joystick)

    # Tela de pausa e variáveis de controle
    pause_screen = PauseScreen(screen)
    is_paused = False
    jogador_morreu = False
    momento_morte = 0

    # Grupos e variáveis auxiliares
    diagramas_pendentes = []
    diagrama_animado_group = pygame.sprite.Group()
    diagrama_disparado = False
    bill_image = pygame.image.load("assets/images/level2/angrybill.png").convert_alpha()
    bill_group = pygame.sprite.Group()

    player_group = pygame.sprite.Group(player)
    totem = carregar_imagem_totem()
    fire = carregar_imagem_fogo()
    fire_group = pygame.sprite.Group(fire)

    # Cria as plataformas do nível
    platforms = pygame.sprite.Group(
        Platform("assets/images/level2/base.png", 0, HEIGHT-60, 800, 100),
        Platform("assets/images/level2/plataforma central.png", 215, HEIGHT/2+50, 375, 50),
        Platform("assets/images/level2/plataformas laterais.png", -40, HEIGHT-150, 200, 50),
        Platform("assets/images/level2/plataformas laterais.png", WIDTH-160, HEIGHT-150, 200, 50),
        Platform("assets/images/level2/plataforma superior.png", 0, HEIGHT/2-70, 130, 100),
        Platform("assets/images/level2/plataforma superior.png", WIDTH-130, HEIGHT/2-70, 130, 100)
    )

    # Carrega imagem da sacola de dinheiro e cria grupo
    money_sheet = pygame.image.load("assets/images/level2/money.png").convert_alpha()
    money_group = pygame.sprite.Group(MoneyBag(money_sheet, platforms, player))

    # Carrega spritesheets de inimigos e portais
    flight_sheet = pygame.image.load(os.path.join("assets", "images", "level2", "Flight.png")).convert_alpha()
    attack_sheet = pygame.image.load(os.path.join("assets", "images", "level2", "Attack1.png")).convert_alpha()
    zombie_walk_sheet = pygame.image.load("assets/images/level2/Zombie correndo.png").convert_alpha()
    zombie_attack_sheet = pygame.image.load("assets/images/level2/Zombie atacando.png").convert_alpha()
    portal_sheet = pygame.image.load("assets/images/level2/portal opening.png").convert_alpha()

    enemies = pygame.sprite.Group()
    portal_group = pygame.sprite.Group()

    # Cria spawns de zumbis
    zombie_spawns = pygame.sprite.Group(
        ZombieSpawn(300, HEIGHT/2 - 20, enemies, player, fire, platforms, zombie_walk_sheet, zombie_attack_sheet)
    )
    for x, y in [(250, HEIGHT/2 - 20), (350, HEIGHT/2 - 20), (400, HEIGHT/2 - 20)]:
        zombie_spawns.add(ZombieSpawn(x, y, enemies, player, fire, platforms, zombie_walk_sheet, zombie_attack_sheet))

    # Spawns aleatórios de portais
    spawn_points = [(70, 200), (WIDTH - 60, 150), (70, 150), (WIDTH - 60, 200)]
    for ponto in random.sample(spawn_points, random.randint(1, min(3, len(spawn_points)))):
        portal_group.add(PortalSpawn(*ponto, portal_sheet, enemies, player, flight_sheet, attack_sheet))

    spawn_timer = pygame.time.get_ticks()
    spawn_interval = 10000  # Intervalo inicial para novos spawns

    running = True
    while running:
        # Loop principal de eventos
        for event in pygame.event.get():
            virtual_controller.handle_event(event)
            if event.type == pygame.QUIT:
                return "quit"

            # Alterna pausa com ESC ou botão do joystick
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.JOYBUTTONDOWN and event.button == 7 or virtual_controller.consume_pause():
                is_paused = not is_paused
                if is_paused:
                    pygame.mixer.music.pause()
                    pause_screen.show()
                else:
                    pygame.mixer.music.unpause()
                    pause_screen.hide()

            # Trata eventos na tela de pausa
            if is_paused:
                action = pause_screen.handle_event(event)
                if action == 'continue':
                    is_paused = False
                    pause_screen.hide()
                elif action == 'menu':
                    return 'menu'
                elif action == 'level_select':
                    return 'level_select'

        # Se pausado, desenha a tela de pausa e continua o loop
        if is_paused:
            pause_screen.draw()
            pygame.display.flip()
            clock.tick(FPS)
            await asyncio.sleep(0)
            continue

        # Carrega e desenha o cenário
        background = pygame.image.load("assets/images/level2/cenario level 2.jpeg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        graves1 = load_image('level2/tumulos.png', size=(370, 70))
        graves2 = load_image('level2/graves.png', size=(370, 70))

        screen.blit(background, (0, -10))
        platforms.draw(screen)
        fire_group.update()
        fire_group.draw(screen)
        screen.blit(graves1, (235, HEIGHT/2 - 15))
        screen.blit(graves2, (220, HEIGHT/2 - 10))
        totem.update()
        screen.blit(totem.image, (10, 130))
        screen.blit(totem.image, (WIDTH - 120, 130))

        # Verifica morte do jogador
        if jogador_morreu:
            pygame.mixer.music.stop()
            som_morte.play()
            tempo_morrido = pygame.time.get_ticks() - momento_morte
            desenhar_vidas(screen, player.vida)
            player_group.draw(screen)
            money_group.draw(screen)
            virtual_controller.draw()
            pygame.display.flip()
            if tempo_morrido > 3000:
                return await tela_game_over(screen)
            clock.tick(FPS)
            await asyncio.sleep(0)
            continue
        
        # Atualiza jogador com teclado ou joystick
        keys = pygame.key.get_pressed()
        player_group.update(keys, platforms, virtual_controller)
        
        # Verifica se o jogador morreu por perder toda a vida
        if not jogador_morreu and player.vida <= 0:
            jogador_morreu = True
            momento_morte = pygame.time.get_ticks()
            print("💀 O jogador morreu, vida zerada")

        # Verifica se o jogador morreu encostando no fogo
        if not jogador_morreu and player.rect.colliderect(fire.hitbox):
            jogador_morreu = True
            momento_morte = pygame.time.get_ticks()
            print("🔥 O jogador morreu no fogo")

        # Desenha jogador, itens e HUD
        player_group.draw(screen)
        money_group.draw(screen)
        desenhar_vidas(screen, player.vida)
        desenhar_contador_sacos(screen, fonte_sacos, player.dinheiro)
        screen.blit(icone_dinheiro, (WIDTH - 230, 15))
        desenhar_contador_sacos(screen, fonte_sacos, player.dinheiro)

        # Verifica se o jogador ganhou
        for money in money_group:
            resultado = money.update()
            if resultado == 'win':
                pygame.mixer.music.stop()
                pygame.display.flip()
                await asyncio.sleep(2)
                return await tela_vitoria(screen)

        # Atualiza inimigos
        enemies.update()
        for enemy in enemies:
            # Zumbi morre se encostar no fogo e ativa o diagrama
            if isinstance(enemy, ZombieEnemy) and fire.hitbox.colliderect(enemy.rect) and not enemy.ativou_diagrama:
                enemy.ativou_diagrama = True
                enemy.dead = True
                enemy.state = "dead"
                enemy.frame_index = 0
                enemy.last_update = pygame.time.get_ticks()
                enemy.frame_speed = 150
                diagrama = DiagramaAnimado("assets/images/level2/diagrama", pos=(WIDTH // 2, 180), frame_speed=50, scale=0.5)
                diagrama_animado_group.add(diagrama)
                diagramas_pendentes.append(diagrama)
                print("⚠️ Zumbi ativou o diagrama e morreu no fogo!")

        enemies.draw(screen)
        zombie_spawns.update()
        zombie_spawns.draw(screen)

        # Atualiza e desenha portais
        portal_group.update()
        for portal in portal_group:
            scaled = pygame.transform.scale(portal.image, (40, 40))
            screen.blit(scaled, scaled.get_rect(center=portal.rect.center).topleft)

        # Desenha poderes do jogador
        player.poder_group.draw(screen)

        # Gera novos inimigos por portais após intervalo
        now = pygame.time.get_ticks()
        if now - spawn_timer > spawn_interval:
            spawn_timer = now
            for ponto in random.sample(spawn_points, random.randint(1, 3)):
                portal_group.add(PortalSpawn(*ponto, portal_sheet, enemies, player, flight_sheet, attack_sheet))
            spawn_interval = random.randint(10000, 15000)

        # Atualiza e desenha animações de diagramas
        diagrama_animado_group.update()
        for diagrama in diagramas_pendentes[:]:
            if diagrama.terminou:
                bill_group.add(BillCipherChaser(WIDTH // 2, HEIGHT // 2, bill_image, player))
                diagramas_pendentes.remove(diagrama)

        diagrama_animado_group.draw(screen)
        bill_group.update()
        bill_group.draw(screen)

        virtual_controller.draw()
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(FPS)
