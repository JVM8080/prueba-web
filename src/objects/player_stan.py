import pygame
from config import *
from src.utils.asset_loader import load_image
from pygame import mixer
from src.objects.power import PoderBase

# Sons globais
JUMP_SOUND = None
TIRO_SOUND = None
DANO_SOUND = None

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        global JUMP_SOUND
        global TIRO_SOUND
        global DANO_SOUND

        # Carregamento das imagens de animação
        self.image_idle = load_image("level2/stan/stan parado.png").convert_alpha()
        self.anim_left = load_image('level2/stan/stan indo pra esquerda.png').convert_alpha()
        self.anim_right = load_image('level2/stan/stan indo pra direita.png').convert_alpha()

        # Cálculo das dimensões dos quadros de animação
        frame_width = self.anim_left.get_width() // 3
        frame_height = self.anim_left.get_height()

        # Separação dos quadros de animação
        self.stan_anim_left = [self.anim_left.subsurface(i * frame_width, 0, frame_width, frame_height) for i in range(3)]
        self.stan_anim_right = [self.anim_right.subsurface(i * frame_width, 0, frame_width, frame_height) for i in range(3)]

        # Estado inicial da animação
        self.frame_left = 0
        self.frame_right = 0
        self.image = self.stan_anim_right[self.frame_right]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Física e movimento
        self.vel_y = 0
        self.speed = 5
        self.jump_force = -8
        self.gravity = 0.3
        self.on_ground = False
        self.last_shoot_direction = -1

        # Estado do jogador
        self.vida = 7
        self.dinheiro = 0 
        self.enemy_group = pygame.sprite.Group()
        self.morto_no_fogo = False
        self.momento_morte = 0

        # Poder (tiro com moeda)
        self.poder_group = pygame.sprite.Group()
        self.moeda_spritesheet = load_image("level2/stan/poder moedas.png").convert_alpha()
        self.moeda_frame_width = self.moeda_spritesheet.get_width() // 6
        self.moeda_frame_height = self.moeda_spritesheet.get_height()

        # Carregamento dos sons (apenas uma vez)
        if not JUMP_SOUND:
            JUMP_SOUND = mixer.Sound("assets/sounds/dipper-jump.ogg")
        
        if not TIRO_SOUND:
            TIRO_SOUND = mixer.Sound("assets/sounds/level2_audio/Coin.ogg")
            TIRO_SOUND.set_volume(0.4)

        if not DANO_SOUND:
            DANO_SOUND = mixer.Sound("assets/sounds/level2_audio/enemy_attack.ogg")
            DANO_SOUND.set_volume(0.5)

        # Controle da animação
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 50
        self.shoot_pressed_last_frame = False
        self.jump_pressed_last_frame = False

    def update(self, keys, platforms, joystick=None):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update

        dx = 0
        shoot_button = False
        jump_button = False
        moving_left = False
        moving_right = False

        # Controle por joystick
        if joystick:
            axis_x = joystick.get_axis(0)
            shoot_button = joystick.get_button(2)  
            jump_button = joystick.get_button(0)  

            if axis_x < -0.3:
                dx = -self.speed
                moving_left = True
            elif axis_x > 0.3:
                dx = self.speed
                moving_right = True

        # Controle por teclado
        if keys:
            if keys[pygame.K_LEFT]:
                dx = -self.speed
                moving_left = True
            elif keys[pygame.K_RIGHT]:
                dx = self.speed
                moving_right = True

            if keys[pygame.K_z]:
                shoot_button = True
            if keys[pygame.K_SPACE]:
                jump_button = True

        # Animação para a esquerda
        if moving_left:
            if elapsed_ticks > self.frame_ticks:
                self.last_update = now
                self.frame_left = (self.frame_left + 1) % len(self.stan_anim_left)
            self.image = self.stan_anim_left[self.frame_left]
            self.last_shoot_direction = -1

        # Animação para a direita
        elif moving_right:
            if elapsed_ticks > self.frame_ticks:
                self.last_update = now
                self.frame_right = (self.frame_right + 1) % len(self.stan_anim_right)
            self.image = self.stan_anim_right[self.frame_right]
            self.last_shoot_direction = 1

        # Parado
        else:
            self.image = self.image_idle

        # Disparo do poder (moeda)
        if shoot_button and not self.shoot_pressed_last_frame:
            direction = self.last_shoot_direction
            offset = 30
            moeda = PoderBase(
                self.rect.centerx + direction * offset,
                self.rect.centery,
                direction,
                self.moeda_spritesheet,
                frame_count=6,
                frame_width=self.moeda_frame_width,
                frame_height=self.moeda_frame_height
            )
            self.poder_group.add(moeda)
            TIRO_SOUND.play()

        self.shoot_pressed_last_frame = shoot_button

        # Aplicação da gravidade
        self.vel_y += self.gravity
        dy = self.vel_y

        # Atualização da posição
        self.rect.x += dx
        self.rect.y += dy
        
        # Limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0  
            self.on_ground = True

        # Verificação de colisão com plataformas
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0 and abs(self.rect.bottom - platform.rect.top) < 15:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # Pulo
        if jump_button and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False
            JUMP_SOUND.play()

        self.jump_pressed_last_frame = jump_button

        # Atualiza os projéteis
        self.poder_group.update()

        # Verifica colisão com inimigos
        for enemy in pygame.sprite.spritecollide(self, self.enemy_group, False):
            if enemy.state == "attack":
                if not hasattr(enemy, "last_hit") or pygame.time.get_ticks() - enemy.last_hit > 500:
                    self.vida -= 1
                    DANO_SOUND.play()
                    enemy.last_hit = pygame.time.get_ticks()
                    print(f"Player levou dano! Vida: {self.vida}")
                if self.vida <= 0:
                    self.kill()

    # Reseta posição do jogador
    def reset_position(self):
        self.rect.topleft = (100, HEIGHT - 150)

    # Desenha o jogador e seus poderes na tela
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.poder_group.draw(screen)
