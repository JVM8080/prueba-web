# Importação das bibliotecas necessárias
import asyncio
import pygame
import random
from src.objects.dipper import Player
from src.objects.enemigo import Enemy
from src.objects.bill import Bill
from src.objects.platform import Platform
from src.objects.fireball import Fireball
from src.utils.asset_loader import load_image
from config import *

from src.screens.pause_screen import PauseScreen
from src.utils.virtual_controller import VirtualXboxController
from src.screens.game_over import tela_game_over
from src.screens.winner import tela_vitoria

# Função principal que roda o nível do jogo
async def run(screen):
    # Inicializa o mixer de som e toca a música do nível
    pygame.mixer.init()
    pygame.mixer.music.load("assets/sounds/level_3.ogg")  
    pygame.mixer.music.set_volume(SOUND_VOLUME_MUSIC)  
    pygame.mixer.music.play(-1)
    
    # Inicializa o relógio do jogo
    clock = pygame.time.Clock()
    dt = clock.tick(FPS)

    # Grupos de sprites
    enemies = pygame.sprite.Group()
    enemy_spawn_timer = 0
    enemy_spawn_delay = 1000  # Delay para spawn de inimigos

    # Vidas do jogador
    lives = 3
    heart_image = load_image("level_3/vida.png", size=(32, 32))

    # Inicializa o joystick, se existir
    joystick = None
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    virtual_controller = VirtualXboxController(screen, joystick)

    # Estados do jogo
    running = True
    game_over = False
    paused = False
    level_complete = False  

    # Tela de pausa
    pause_screen = PauseScreen(screen)
    
    # Criação das plataformas
    platforms = pygame.sprite.Group()
    platforms.add(Platform(150, 400, phase=0))
    platforms.add(Platform(350, 450, phase=45))
    platforms.add(Platform(550, 400, phase=90))
    starting_platform = list(platforms)[1]  # Plataforma inicial
    
    # Posição inicial do jogador
    player_x = starting_platform.rect.x + starting_platform.rect.width // 2
    player_y = starting_platform.rect.y - 90  

    # Cria o jogador
    player = Player(player_x, player_y)
    
    # Cria o chefão (Bill)
    bills = pygame.sprite.Group()
    bill = Bill(WIDTH // 2, 150, phase=0)
    bills.add(bill)
    
    # Grupo de bolas de fogo do chefão
    fireballs = pygame.sprite.Group()
    fireball_timer = 0
    fireball_spawn_delay = 700  # Tempo entre disparos

    # Loop principal do jogo
    while running:
        dt = clock.tick(FPS)
        enemy_spawn_timer += dt
        
        # Bill atira bolas de fogo se estiver danificado
        if bill.is_damaged:
            fireball_timer += dt
            if fireball_timer >= fireball_spawn_delay:
                fireball = Fireball()
                fireballs.add(fireball)
                fireball_timer = 0

        # Trata eventos do sistema
        for event in pygame.event.get():
            virtual_controller.handle_event(event)
            if event.type == pygame.QUIT:
                return 'quit'

            # Caso o jogo tenha terminado
            if game_over:
                pygame.mixer.music.stop()
                result = await tela_game_over(screen)
                if result == 'menu':
                    pygame.mixer.music.stop()
                    return 'menu'

            # Caso o nível tenha sido completado
            elif level_complete:
                pygame.mixer.music.stop()
                result = await tela_vitoria(screen)
                if result == 'menu':
                    pygame.mixer.music.stop()
                    return 'menu'

            # Caso esteja em pausa
            elif paused:
                pause_screen.update(dt)
                result = pause_screen.handle_event(event)
                pygame.mixer.music.pause()
                if result == 'continue':
                    pygame.mixer.music.unpause()
                    # Reinicia posição do jogador
                    player.rect.x = starting_platform.rect.x + starting_platform.rect.width // 2
                    player.rect.y = starting_platform.rect.y - 90
                    paused = False
                    pause_screen.hide()
                elif result == 'level_select':
                    pygame.mixer.music.stop()
                    return 'level_select'
                elif result == 'menu':
                    pygame.mixer.music.stop()
                    return 'menu'

            # Eventos normais do jogo
            else:  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = True
                        pause_screen.show()
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 7:  
                        paused = not paused
                        if paused:
                            pause_screen.show()
                        else:
                            pause_screen.hide()
                elif virtual_controller.consume_pause():
                    paused = not paused
                    if paused:
                        pause_screen.show()
                    else:
                        pause_screen.hide()

        # Captura teclas pressionadas
        keys = pygame.key.get_pressed()

        # Atualizações de jogo, apenas se não estiver pausado, vencido ou com game over
        if not game_over and not paused and not level_complete:
            player.update(keys=keys, joystick=virtual_controller, platforms=platforms)
            fireballs.update()

            # Colisão entre jogador e bolas de fogo
            for fireball in fireballs.copy():
                if player.rect.colliderect(fireball.rect):
                    if not player.invulnerable:
                        lives -= 1
                        player.activate_invulnerability()
                        player.play_damage_animation()
                        if lives <= 0:
                            game_over = True
                            enemies.empty()
                            player.projectiles.clear()
                            player.special_attacks.clear()
                            pygame.mixer.music.stop()
                    fireball.kill()

            # Queda do jogador
            if player.rect.y >= HEIGHT-150: 
                lives -= 1
                if lives <= 0:
                    game_over = True
                    enemies.empty()
                    player.projectiles.clear()
                    player.special_attacks.clear()
                    pygame.mixer.music.stop()
                else:
                    # Reinicializa o jogador
                    player.rect.midbottom = starting_platform.rect.midtop
                    player.vel_y = 0
                    player.on_ground = True
                    player.has_teleported_in_air = False
                    player.teleporting = False
                    player.visible = True
                    player.invulnerable = False
                    player.playing_damage_animation = False
                    player.activate_invulnerability()
                    player.play_damage_animation()
                    player.rect.x = starting_platform.rect.x + starting_platform.rect.width // 2
                    player.rect.y = starting_platform.rect.y - 90

            # Colisão entre jogador e inimigos
            for enemy in enemies.copy():
                enemy.update(player.rect)
                if player.rect.colliderect(enemy.rect):
                    if not player.invulnerable:
                        lives -= 1
                        player.activate_invulnerability()
                        player.play_damage_animation()  
                        enemies.remove(enemy)
                        if lives <= 0:
                            game_over = True
                            enemies.empty()
                            player.projectiles.clear()
                            player.special_attacks.clear()

            # Colisão dos projéteis do jogador
            projectiles_to_remove = []

            for projectile in player.projectiles.copy():
                removed = False

                # Colisão com inimigos
                for enemy in enemies.copy():
                    if projectile.rect.colliderect(enemy.rect):
                        enemy.health -= getattr(projectile, 'damage', 1)
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                        projectiles_to_remove.append(projectile)
                        removed = True
                        break  

                # Colisão com Bill
                if not removed and bill.rect.colliderect(projectile.rect):
                    bill.health -= projectile.damage
                    if bill.health <= 0:
                        bill.kill()
                        level_complete = True
                        pygame.mixer.music.stop()
                        enemies.empty()
                        player.projectiles.clear()
                        player.special_attacks.clear()
                    projectiles_to_remove.append(projectile)

            for projectile in projectiles_to_remove:
                if projectile in player.projectiles:
                    player.projectiles.remove(projectile)

            # Colisão entre jogador e Bill
            for bill in bills.copy():
                if player.rect.colliderect(bill.rect):
                    if not player.invulnerable:
                        lives -= 1
                        player.activate_invulnerability()
                        player.play_damage_animation()
                        if lives <= 0:
                            game_over = True
                            enemies.empty()
                            player.projectiles.clear()
                            player.special_attacks.clear()
                            
            # Ataques especiais
            for attack in player.special_attacks.copy():
                hit = False
                for enemy in enemies.copy():
                    if attack.rect.colliderect(enemy.rect):
                        enemies.remove(enemy)
                        hit = True
                        break

                if bill.rect.colliderect(attack.rect):
                    bill.health -= getattr(attack, 'damage', 6)
                    if bill.health <= 0:
                        bill.kill()
                        level_complete = True
                    hit = True

                if hit:
                    player.special_attacks.remove(attack)

            # Spawn de inimigos
            if enemy_spawn_timer >= enemy_spawn_delay and not level_complete:
                spawn_side = random.choice(['top', 'left', 'right'])
                if spawn_side == 'top':
                    enemy_x = random.randint(0, WIDTH - 40)
                    enemy_y = -40
                elif spawn_side == 'left':
                    enemy_x = -40
                    enemy_y = random.randint(0, HEIGHT - 40)
                else:  
                    enemy_x = WIDTH + 40
                    enemy_y = random.randint(0, HEIGHT - 40)

                enemy = Enemy(enemy_x, enemy_y)
                enemies.add(enemy)
                enemy_spawn_timer = 0

        # Carrega o fundo dependendo do estado do Bill
        background_path = "level_3/background_2.png" if bill.is_damaged else "level_3/background_1.png"
        screen.blit(load_image(background_path, size=("auto", HEIGHT)), (0, 0))

        # Desenha os elementos na tela
        player.draw(screen)
        enemies.draw(screen)
        platforms.update()
        platforms.draw(screen)
        fireballs.draw(screen)
        
        # Atualiza e desenha Bill e sua barra de vida
        if not level_complete:
            bill.update(dt, player.rect)
            bills.draw(screen)

            if bill.alive():
                bar_width = 250
                bar_height = 25
                bar_x = (WIDTH - bar_width) // 2
                bar_y = 20

                bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
                pygame.draw.rect(screen, (50, 50, 50), bg_rect, border_radius=10)

                health_ratio = max(bill.health, 0) / bill.max_health
                current_bar_width = int(bar_width * health_ratio)
                health_rect = pygame.Rect(bar_x, bar_y, current_bar_width, bar_height)
                pygame.draw.rect(screen, (200, 0, 0), health_rect, border_radius=10)

                pygame.draw.rect(screen, (0, 0, 0), bg_rect, width=2, border_radius=10)

        virtual_controller.draw(enabled=not paused)

        # Desenha a tela de pausa
        if paused:
            pause_screen.draw()
        
        # Desenha os corações de vida
        for i in range(lives):
            x = 10 + i * (heart_image.get_width() + 10)
            y = HEIGHT - heart_image.get_height() - 10
            screen.blit(heart_image, (x, y))

        # Atualiza a tela
        pygame.display.flip()
        await asyncio.sleep(0)
