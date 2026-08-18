# src/objects/porquinho.py
import pygame
from src.utils.safe_asset_loader import load_image_safe as load_image

class Porquinho(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = load_image("porco1.png")
        self.image = pygame.transform.scale(image, (80, 45))
        self.rect = self.image.get_rect()
