import pygame
import random
from config import HEIGHT, WIDTH
from src.utils.asset_loader import load_image

# Classe que representa uma bola de fogo animada que sobe na tela
class Fireball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Carrega o spritesheet completo da animação (5 frames lado a lado, cada um 50x50)
        spritesheet = load_image("level_3/chuva.png", size=(50 * 5, 50))

        # Define o tamanho de cada frame da animação
        frame_width = spritesheet.get_width() // 5
        frame_height = spritesheet.get_height()

        # Extrai os 5 frames individuais do spritesheet (organizados horizontalmente)
        self.frames = []
        for i in range(5):
            frame = spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            self.frames.append(frame)

        # Inicializa os parâmetros da animação
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 100  # Velocidade da animação em milissegundos

        # Define a imagem inicial e sua posição aleatória no eixo x
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)  # Posição horizontal aleatória
        self.rect.y = HEIGHT + 20  # Começa fora da tela, embaixo

        # Define a velocidade vertical aleatória para subir
        self.speed = random.randint(3, 6)

        # Tempo da última atualização da animação
        self.last_update = pygame.time.get_ticks()

    def update(self):
        # Verifica se é hora de mudar para o próximo frame da animação
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        # Move a bola de fogo para cima
        self.rect.y -= self.speed

        # Remove o sprite se sair completamente da tela
        if self.rect.bottom < 0:
            self.kill()
