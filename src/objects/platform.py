import pygame
import math
from src.utils.asset_loader import load_image

# Classe para representar uma plataforma que se move verticalmente em forma de onda senoidal
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width=100, height=20, amplitude=20, speed=2, phase=0):
        super().__init__()

        # Cria uma superfície para a imagem da plataforma e carrega a imagem com o tamanho especificado
        self.image = pygame.Surface((width, height))
        self.image = load_image("level_3/platform.png", size=(width, height))
        self.rect = self.image.get_rect(topleft=(x, y))  # Define a posição inicial

        # Guarda a posição vertical inicial
        self.initial_y = y

        # Define os parâmetros do movimento senoidal
        self.amplitude = amplitude  # amplitude do movimento (altura do deslocamento)
        self.speed = speed          # velocidade com que a plataforma oscila
        self.phase = phase          # fase inicial da oscilação
        self.timer = 0              # contador de tempo (em graus para o seno)

    def update(self):
        # Atualiza o timer com a velocidade definida
        self.timer += self.speed

        # Calcula o deslocamento vertical com base na função seno
        offset = math.sin(math.radians(self.timer + self.phase)) * self.amplitude

        # Aplica o deslocamento à posição vertical da plataforma
        self.rect.y = self.initial_y + offset
