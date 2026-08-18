import pygame
from config import SOUND_VOLUME_SFX
from pygame import mixer
from src.utils.asset_loader import load_image
from config import HEIGHT, WIDTH
from src.objects.fireball import Fireball

# Variáveis globais para armazenar os sons
PROJECTILE_SOUND = None
ENERGYBALL_SOUND = None

class Projectile:
    def __init__(self, x, y, direction, play_sound=True):
        global PROJECTILE_SOUND

        # Carrega o som do projétil se ainda não estiver carregado
        if PROJECTILE_SOUND is None:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            PROJECTILE_SOUND = pygame.mixer.Sound("assets/sounds/dipper-attack1.ogg")

        # Toca o som se play_sound for True
        if play_sound:
            PROJECTILE_SOUND.set_volume(SOUND_VOLUME_SFX)
            PROJECTILE_SOUND.play()
        
        # Carrega spritesheet com animações do projétil
        self.sprite_sheet = load_image("dipper/dipper_attack1.png", size=(80*5, 80))
        self.frames = []
        self.frame_count = 5
        self.frame_width = self.sprite_sheet.get_width() // self.frame_count
        self.frame_height = self.sprite_sheet.get_height()

        # Divide a spritesheet em frames individuais
        for i in range(self.frame_count):
            frame = self.sprite_sheet.subsurface(
                (i * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            self.frames.append(frame)

        # Inicializa variáveis de animação
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_interval = 5  # tempo entre troca de frames

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        # Propriedades físicas do projétil
        self.speed = 8
        self.damage = 2
        self.direction = direction
        self.lifetime = 60  # tempo de vida do projétil (em frames)

    def update(self):
        # Move o projétil na direção especificada
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Atualiza a animação
        self.frame_timer += 1
        if self.frame_timer >= self.frame_interval:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        # Retorna True se o projétil sair da tela
        return (self.rect.right < 0 or self.rect.left > 800 or
                self.rect.bottom < 0 or self.rect.top > 600)

    def draw(self, screen):
        # Desenha o projétil na tela
        screen.blit(self.image, self.rect)

class EnergyBall(Projectile):
    def __init__(self, x, y, direction):
        # Chama o construtor da classe pai sem tocar o som
        super().__init__(x, y, direction, play_sound=False)

        global ENERGYBALL_SOUND

        # Carrega o som da bola de energia se ainda não estiver carregado
        if ENERGYBALL_SOUND is None:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            ENERGYBALL_SOUND = pygame.mixer.Sound("assets/sounds/dipper-attack2.wav")

        # Configura volume e toca o som
        ENERGYBALL_SOUND.set_volume(SOUND_VOLUME_SFX)
        ENERGYBALL_SOUND.play()

        # Carrega spritesheet com animação da bola de energia
        self.sprite_sheet = load_image("dipper/dipper_attack2.png", size=(50*5, 50))
        self.frames = []
        frame_width = self.sprite_sheet.get_width() // 5
        frame_height = self.sprite_sheet.get_height()

        # Divide a spritesheet em frames individuais
        for i in range(5):
            frame = self.sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            self.frames.append(frame)

        # Inicializa variáveis de animação
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_interval = 5

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        # Propriedades específicas da bola de energia
        self.speed = 4
        self.lifetime = 90
        self.damage = 6

    def update(self):
        # Move a bola de energia
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Atualiza a animação
        self.frame_timer += 1
        if self.frame_timer >= self.frame_interval:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        # Retorna True se a bola sair da tela
        return (self.rect.right < 0 or self.rect.left > 800 or
                self.rect.bottom < 0 or self.rect.top > 600)
