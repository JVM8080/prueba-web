# Importa os módulos necessários
import pygame
from src.objects.animation import Portal  # Classe responsável por animações de sprite (como portais, fogo, etc.)
from config import *  # Importa configurações globais, como WIDTH e HEIGHT
import os

# Função para carregar o totem animado como um objeto do tipo Portal
def carregar_imagem_totem():
    totem_sheet = pygame.image.load("assets/images/level2/totem.png").convert_alpha()  # Carrega a spritesheet do totem com transparência
    totem = Portal(
        x=400,
        y=HEIGHT - 250,
        spritesheet=totem_sheet,
        frame_width=totem_sheet.get_width() // 7,  # Divide a largura da imagem em 7 frames
        frame_height=totem_sheet.get_height(),
        frame_count=7,  # Número total de frames da animação
        frame_speed=100,  # Velocidade da animação (em milissegundos por frame)
        scale_size=(120, 140)  # Redimensiona cada frame para esse tamanho
    )
    return totem  # Retorna o objeto animado do tipo Portal

# Função para carregar o fogo animado como um objeto do tipo Portal
def carregar_imagem_fogo():
    fogo_sheet = pygame.image.load("assets/images/level2/fogo.png").convert_alpha()  # Carrega a spritesheet do fogo
    fire = Portal(
        x=WIDTH / 2 - 115,
        y=HEIGHT - 215,
        spritesheet=fogo_sheet,
        frame_width=fogo_sheet.get_width() // 8,  # Divide a imagem em 8 frames
        frame_height=fogo_sheet.get_height(),
        frame_count=8,
        frame_speed=100,
        scale_size=(230, 230)
    )
    # Define a área de colisão (hitbox) do fogo manualmente
    fire.hitbox = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 90, 50, 40)
    return fire  # Retorna o objeto animado do tipo Portal com hitbox

# Variável global que armazena a imagem da barra de vida
vida_img = None
POS_VIDAS = (20, 20)  # Posição onde a barra de vida será desenhada na tela

# Função para desenhar a barra de vidas na tela
def desenhar_vidas(surface, vidas):
    global vida_img
    if vida_img is None:
        # Carrega e redimensiona a imagem da barra de vidas apenas uma vez
        vida_img = pygame.image.load("assets/images/level2/vidas.png").convert_alpha()
        vida_img = pygame.transform.scale(vida_img, (260, 30))

    total_coracoes = 7  # A imagem da barra de vidas tem 7 corações
    coracao_largura = vida_img.get_width() // total_coracoes  # Largura de cada coração
    coracao_altura = vida_img.get_height()

    largura_mostrar = max(0, vidas) * coracao_largura  # Calcula a parte da imagem que será exibida
    rect = pygame.Rect(0, 0, largura_mostrar, coracao_altura)  # Define a área da imagem a ser desenhada
    surface.blit(vida_img, POS_VIDAS, rect)  # Desenha a barra de vida parcial conforme o número de vidas

# Função para desenhar o contador de sacos coletados na tela
def desenhar_contador_sacos(surface, fonte, quantidade):
    texto = fonte.render(f"[{quantidade}]", True, (255, 255, 0))  # Renderiza o texto da quantidade em amarelo
    surface.blit(texto, (WIDTH - 150, 30))  # Desenha o texto na parte superior direita da tela
