import pygame
import os

IMG_PATH = "assets/images/"

def load_image_safe(name, size=None):
    path = os.path.join(IMG_PATH, name)
    image = pygame.image.load(path)

    # Só converte se o display já estiver inicializado
    if pygame.display.get_init():
        image = image.convert_alpha()
    
    if size:
        image = pygame.transform.scale(image, size)

    return image
