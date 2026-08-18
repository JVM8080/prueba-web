import pygame
from config import HEIGHT
from src.utils.asset_loader import load_image
from pygame import mixer
from src.objects.power import PoderBase

JUMP_SOUND = None  # Variável global para armazenar o som de pulo

class Player:
    def __init__(self, x, y):
        global JUMP_SOUND

        # Carrega a imagem de Mabel parada
        self.image_idle = load_image("mabel/mabel.png", size=(60, "auto"))

        # Carrega as sprites de animação da Mabel andando para esquerda e direita
        self.anim_left = load_image('mabel/mabel indo pra esquerda.png').convert_alpha()
        self.anim_right = load_image('mabel/mabel pra direita.png').convert_alpha()

        # Divide a imagem da esquerda em 3 frames
        frame_width_left = self.anim_left.get_width() // 3
        frame_height_left = self.anim_left.get_height()
        self.mabel_anim_left = [
            self.anim_left.subsurface(pygame.Rect(i * frame_width_left, 0, frame_width_left, frame_height_left))
            for i in range(3)
        ]

        # Divide a imagem da direita em 3 frames
        frame_width_right = self.anim_right.get_width() // 3
        frame_height_right = self.anim_right.get_height()
        self.mabel_anim_right = [
            self.anim_right.subsurface(pygame.Rect(i * frame_width_right, 0, frame_width_right, frame_height_right))
            for i in range(3)
        ]

        # Índices de animação
        self.frame_left = 0
        self.frame_right = 0

        # Define imagem e posição inicial
        self.image = self.mabel_anim_right[self.frame_right]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Direção do último movimento (1 = direita, -1 = esquerda)
        self.last_direction = 1

        # Atributos de movimento
        self.vel_y = 0
        self.speed = 4
        self.jump_force = -13         
        self.gravity = 0.45            
        self.max_fall_speed = 10      
        self.on_ground = False  # Verifica se está no chão

        # Grupo para armazenar os poderes lançados
        self.poder_group = pygame.sprite.Group()

        # Carrega e ajusta a imagem da estrela usada como poder
        estrela_original = load_image("mabel/estrela_poder_transparente.png").convert_alpha()
        reduzida_w = estrela_original.get_width() // 25
        reduzida_h = estrela_original.get_height() // 25
        self.estrela_direita = pygame.transform.scale(estrela_original, (reduzida_w, reduzida_h))
        self.estrela_esquerda = pygame.transform.flip(self.estrela_direita, True, False)

        self.estrela_frame_width = reduzida_w
        self.estrela_frame_height = reduzida_h

        # Carrega o som de pulo se ainda não estiver carregado
        if not JUMP_SOUND:
            JUMP_SOUND = mixer.Sound("assets/sounds/jump.ogg")

        # Controle de tempo para animações
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 50  # Intervalo entre frames

        # Armazena se o botão Z foi pressionado no frame anterior
        self.z_pressed_last_frame = False

    def update(self, keys, joystick=None):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update
        dx = 0  # Deslocamento horizontal

        # Captura teclas pressionadas
        jump_pressed = keys[pygame.K_SPACE]
        fire_pressed = keys[pygame.K_z]
        move_left = keys[pygame.K_LEFT]
        move_right = keys[pygame.K_RIGHT]

        # Se tiver joystick conectado
        if joystick:
            axis_0 = joystick.get_axis(0)  # Eixo horizontal do direcional
            joystick_dx = axis_0

            if axis_0 < -0.3:
                move_left = True
            elif axis_0 > 0.3:
                move_right = True

            # Botão 0 = pulo, botão 2 = disparo
            jump_pressed = jump_pressed or joystick.get_button(0)
            fire_pressed = fire_pressed or joystick.get_button(2)

        # Dispara poder se Z (ou botão equivalente) for pressionado e não estiver segurando do frame anterior
        if fire_pressed and not self.z_pressed_last_frame:
            direction = self.last_direction
            estrela_sprite = self.estrela_direita if direction == 1 else self.estrela_esquerda

            # Cria o poder e adiciona ao grupo
            estrela = PoderBase(
                self.rect.centerx,
                self.rect.centery,
                direction,
                estrela_sprite,
                frame_count=1,
                frame_width=self.estrela_frame_width,
                frame_height=self.estrela_frame_height
            )
            self.poder_group.add(estrela)

        # Atualiza estado do botão Z
        self.z_pressed_last_frame = fire_pressed

        # Movimento para esquerda
        if move_left:
            dx = -self.speed
            self.last_direction = -1
            if elapsed_ticks > self.frame_ticks:
                self.last_update = now
                self.frame_left = (self.frame_left + 1) % len(self.mabel_anim_left)
                self.image = self.mabel_anim_left[self.frame_left]

        # Movimento para direita
        elif move_right:
            dx = self.speed
            self.last_direction = 1
            if elapsed_ticks > self.frame_ticks:
                self.last_update = now
                self.frame_right = (self.frame_right + 1) % len(self.mabel_anim_right)
                self.image = self.mabel_anim_right[self.frame_right]

        # Se não está se movendo, mostra imagem parada
        else:
            self.image = self.image_idle

        # Pulo
        if jump_pressed and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False
            JUMP_SOUND.play()  # Toca som de pulo

        # Aplica gravidade
        self.vel_y += self.gravity
        if self.vel_y > self.max_fall_speed:
            self.vel_y = self.max_fall_speed

        dy = self.vel_y  # Deslocamento vertical

        # Atualiza posição
        self.rect.x += dx
        self.rect.y += dy

        # Atualiza poderes
        self.poder_group.update()

    def reset_position(self):
        # Reposiciona o jogador na posição inicial
        self.rect.topleft = (100, HEIGHT - 150)

    def draw(self, screen):
        # Desenha o jogador e os poderes na tela
        screen.blit(self.image, self.rect)
        self.poder_group.draw(screen)
