# Importa os módulos necessários
import pygame
from src.utils.asset_loader import load_image  # Função para carregar imagens com redimensionamento

# Classe que representa um inimigo voador simples (como um morcego)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=3):
        super().__init__()  # Inicializa a classe Sprite base do Pygame

        # Carrega a imagem do inimigo e redimensiona para 40x40 pixels
        self.image = load_image("level_3/bat.webp", size=(40, 40))

        # Define a posição inicial do inimigo
        self.rect = self.image.get_rect(topleft=(x, y))

        # Velocidade com que o inimigo se move em direção ao jogador
        self.speed = speed

        # Vida do inimigo (pode ser usada para determinar se ele morre após ser atingido)
        self.health = 2

    # Método que atualiza a posição do inimigo para seguir o jogador
    def update(self, player_rect):
        # Calcula a diferença de posição entre o centro do jogador e o inimigo
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery

        # Calcula a distância entre os dois (evita divisão por zero com dist mínimo 1)
        dist = max((dx**2 + dy**2) ** 0.5, 1)

        # Move o inimigo em direção ao jogador, proporcionalmente à distância
        self.rect.x += int(self.speed * dx / dist)
        self.rect.y += int(self.speed * dy / dist)
