import pygame
from config import HEIGHT
from src.utils.safe_asset_loader import load_image_safe as load_image

# Classe do inimigo gnomo que persegue o jogador, pula e pode causar ou receber dano
class GnomoInimigo(pygame.sprite.Sprite):
    def __init__(self, arco_rect, player, plataformas):
        super().__init__()
        self.player = player
        self.plataformas = plataformas

        # Atributos de movimento e combate
        self.speed = 1.6
        self.gravity = 0.4
        self.vel_y = 0
        self.jump_force = -14
        self.dano = 1
        self.cooldown = 1000  # tempo de espera entre ataques
        self.last_hit = 0
        self.hp = 1
        self.on_ground = False

        # Carrega e separa os sprites de animação por direção
        self.frames = {
            "down": self.split_sheet(load_image("gnome_down_up.png")),
            "left": self.split_sheet(load_image("gnome_left.png")),
            "right": self.split_sheet(load_image("gnome_right.png")),
            "up": self.split_sheet(load_image("gnome_down_up.png")),
        }

        self.direction = "down"  # direção inicial
        self.frame_index = 0
        self.image = self.frames[self.direction][self.frame_index]
        self.rect = self.image.get_rect(midbottom=(arco_rect.centerx, arco_rect.bottom))  # posição inicial

        # Controle de animação
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 150

        # Controle de reação para pulo
        self.reaction_timer = pygame.time.get_ticks()
        self.reaction_delay = 400  # tempo mínimo entre pulos

    # Função para dividir uma spritesheet em 3 frames
    def split_sheet(self, sheet):
        frame_width = sheet.get_width() // 3
        frame_height = sheet.get_height()
        return [sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(3)]

    # Função chamada a cada frame para atualizar o estado do gnomo
    def update(self):
        now = pygame.time.get_ticks()
        dx = 0
        dy = self.vel_y

        # Coordenadas do jogador e do gnomo
        px, py = self.player.rect.center
        gx, gy = self.rect.center
        dist_x = px - gx
        dist_y = py - gy

        horizontal_prox = abs(dist_x) < 300  # distância horizontal para começar a seguir

        # Movimento horizontal em direção ao jogador (Mabel)
        if horizontal_prox:
            dx = self.speed if dist_x > 0 else -self.speed
            self.direction = "right" if dx > 0 else "left"

        # Se o jogador estiver acima e próximo, tenta pular
        if (
            py < self.rect.centery - 60 and
            abs(dist_x) < 100 and
            self.on_ground and
            now - self.reaction_timer > self.reaction_delay
        ):
            self.vel_y = self.jump_force
            self.reaction_timer = now

        # Aplica a gravidade
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy = self.vel_y

        # Atualiza a posição com base nas velocidades calculadas
        self.rect.x += dx
        self.rect.y += dy

        # Verifica colisão com plataformas e ajusta a posição do gnomo
        self.on_ground = False
        for plat in self.plataformas:
            if self.vel_y >= 0:
                if (
                    self.rect.bottom <= plat.rect.top + 10 and
                    self.rect.bottom + self.vel_y >= plat.rect.top and
                    self.rect.right > plat.rect.left + 5 and
                    self.rect.left < plat.rect.right - 5
                ):
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    break

        # Impede que o gnomo caia além do chão da tela
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.on_ground = True

        # Animação do sprite de acordo com o tempo
        if now - self.frame_timer >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.direction])
            self.frame_timer = now

        self.image = self.frames[self.direction][self.frame_index]

        # Causa dano ao jogador se estiver colidindo e fora do cooldown
        if self.rect.colliderect(self.player.rect):
            if now - self.last_hit > self.cooldown:
                if hasattr(self.player, 'vida'):
                    self.player.vida -= self.dano
                self.last_hit = now

        # Verifica se foi atingido por um poder do jogador
        for poder in self.player.poder_group:
            if self.rect.colliderect(poder.rect):
                self.hp -= 1
                poder.kill()
                if self.hp <= 0:
                    self.kill()
