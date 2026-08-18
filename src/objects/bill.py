# Importa os módulos necessários
import pygame
import math
from src.utils.asset_loader import load_image  # Função para carregar imagens com redimensionamento

# Classe que representa o inimigo "Bill"
class Bill(pygame.sprite.Sprite):
    def __init__(self, x, y, phase=0):
        super().__init__()

        # Carrega a spritesheet com a aparência normal e separa os frames
        full_image_normal = load_image("level_3/bill_1.png", size=(75 * 3, 75))
        self.frames_normal = []
        for i in range(3):
            # Cria uma superfície com transparência para cada frame
            frame = pygame.Surface((75, 75), pygame.SRCALPHA)
            frame.blit(full_image_normal, (0, 0), (i * 75, 0, 75, 75))  # Recorta o frame da imagem
            frame = pygame.transform.scale(frame, (200, 200))  # Redimensiona o frame
            self.frames_normal.append(frame)  # Adiciona à lista de frames normais

        # Carrega a spritesheet com aparência danificada e separa os frames
        full_image_damaged = load_image("level_3/bill_2.png", size=(75 * 3, 75))
        self.frames_damaged = []
        for i in range(3):
            frame = pygame.Surface((75, 75), pygame.SRCALPHA)
            frame.blit(full_image_damaged, (0, 0), (i * 75, 0, 75, 75))
            frame = pygame.transform.scale(frame, (200, 200))
            self.frames_damaged.append(frame)  # Adiciona à lista de frames danificados

        self.frames = self.frames_normal  # Começa com os frames normais

        self.current_frame = 0  # Índice do frame atual da animação
        self.animation_timer = 0  # Temporizador para trocar de frame
        self.animation_speed = 150  # Tempo entre frames (em milissegundos)

        # Posição base (fixa no eixo X e Y)
        self.base_x = x
        self.base_y = y
        self.image = self.frames[self.current_frame]  # Define a imagem inicial
        self.rect = self.image.get_rect(center=(self.base_x, self.base_y))  # Define o retângulo com base na imagem

        # Parâmetros da oscilação vertical
        self.oscillation_amplitude = 20  # Amplitude da oscilação (altura máxima)
        self.oscillation_speed = 0.005  # Velocidade da oscilação
        self.phase = math.radians(phase)  # Fase inicial da oscilação

        self.health = 200  # Vida atual
        self.max_health = 200  # Vida máxima
        self.total_time = 0  # Tempo total acumulado (para animar a oscilação)

        self.is_damaged = False  # Estado indicando se o inimigo está danificado

    # Atualiza o comportamento do inimigo a cada frame
    def update(self, dt, player_rect=None):
        self.total_time += dt  # Acumula o tempo desde o início

        # Verifica se a vida chegou a 0 e remove o sprite do jogo
        if self.health <= 0:
            self.kill()
            return

        # Troca para aparência danificada se a vida estiver abaixo de 120
        if self.health < 120 and not self.is_damaged:
            self.frames = self.frames_damaged
            self.is_damaged = True
        # Volta para aparência normal se a vida voltar a subir
        elif self.health >= 120 and self.is_damaged:
            self.frames = self.frames_normal
            self.is_damaged = False

        # Calcula o deslocamento vertical baseado na oscilação senoidal
        offset = self.oscillation_amplitude * math.sin(self.total_time * self.oscillation_speed + self.phase)
        self.rect.centery = self.base_y + offset  # Aplica o deslocamento vertical

        # Atualiza a animação de frames
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0
