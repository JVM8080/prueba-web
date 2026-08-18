# Importa a biblioteca pygame e a constante WIDTH do arquivo config
import pygame
from config import WIDTH

class PoderBase(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, spritesheet, frame_count, frame_width, frame_height, speed=9):
        """Inicializa o projétil/poder base
        
        Args:
            x (int): Posição x inicial
            y (int): Posição y inicial
            direction (int): Direção do movimento (1 para direita, -1 para esquerda)
            spritesheet (Surface): Folha de sprites com os frames da animação
            frame_count (int): Quantidade de frames na animação
            frame_width (int): Largura de cada frame
            frame_height (int): Altura de cada frame
            speed (int, optional): Velocidade do projétil. Padrão 9.
        """
        super().__init__()  # Chama o construtor da classe pai (Sprite)
        
        # Prepara os frames de animação
        self.frames = []
        for i in range(frame_count):
            # Extrai cada frame da spritesheet
            frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            self.frames.append(frame)

        # Configuração da animação
        self.frame_index = 0  # Frame atual
        self.image = self.frames[self.frame_index]  # Imagem inicial
        self.rect = self.image.get_rect(center=(x, y))  # Retângulo de colisão
        self.spawn_time = pygame.time.get_ticks()  # Momento em que foi criado

        # Controle de animação
        self.last_update = pygame.time.get_ticks()  # Última atualização
        self.frame_delay = 80  # Tempo entre frames em milissegundos

        # Propriedades de movimento
        self.direction = direction  # Direção (1 ou -1)
        self.speed = speed  # Velocidade do projétil

    def update(self):
        """Atualiza o estado do projétil a cada frame"""
        
        # Movimento horizontal
        self.rect.x += self.speed * self.direction

        # Animação dos frames
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            # Avança para o próximo frame (volta ao início se chegar no último)
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]  # Atualiza a imagem

        # Remove o projétil se sair dos limites da tela
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()  # Método do pygame.sprite.Sprite para remover o sprite