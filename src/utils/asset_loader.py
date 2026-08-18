import pygame
from config import IMG_PATH  # Caminho base para as imagens

_cache = {}  # Dicionário para armazenar imagens em cache

def load_image(name, size=None):
    """
    Carrega uma imagem do caminho IMG_PATH + name e opcionalmente redimensiona.
    Usa cache para não recarregar a mesma imagem múltiplas vezes.

    Parâmetros:
        name (str): Nome do arquivo da imagem.
        size (tuple ou None): Tamanho desejado (largura, altura). Use "auto" para manter proporção.

    Retorna:
        pygame.Surface: A imagem carregada (e possivelmente redimensionada).
    """

    key = (name, size)  # Chave única baseada no nome e tamanho para uso no cache

    # Se a imagem ainda não estiver no cache, carrega e armazena
    if key not in _cache:
        image = pygame.image.load(IMG_PATH + name).convert_alpha()  # Carrega com transparência

        if size:
            width, height = size
            original_width, original_height = image.get_size()

            # Redimensiona proporcionalmente se um dos valores for "auto"
            if height == "auto":
                scale_factor = width / original_width
                height = int(original_height * scale_factor)

            elif width == "auto":
                scale_factor = height / original_height
                width = int(original_width * scale_factor)

            # Aplica redimensionamento
            image = pygame.transform.scale(image, (width, height))

        _cache[key] = image  # Armazena a imagem no cache

    return _cache[key]  # Retorna a imagem (do cache ou nova)
