import pygame
import random
from config import *
from src.screens.winner import tela_vitoria
import os
from pygame import mixer

COLETAR_DINHEIRO_SOUND = None
VITORIA_SOUND = None

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet, frame_width=24, frame_height=32, frame_count=8, frame_speed=100, scale_size=None):
        super().__init__()
        self.frames = []
        self.frame_speed = frame_speed
        self.scale_size = scale_size if scale_size else (200, 200)
        self.fixed_x = x
        self.fixed_y = y

        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()

        for i in range(frame_count):
            frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, self.scale_size)
            self.frames.append(frame)

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.fixed_x, self.fixed_y))

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        self.image = self.frames[self.frame_index]
        self.rect.topleft = (self.fixed_x, self.fixed_y)


class FlyingEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, flight_sheet, attack_sheet, target, scale_size=(300, 300), speed=1):
        super().__init__()

        self.hit_frames = self.load_frames(pygame.image.load("assets/images/level2/Take Hit.png").convert_alpha(), 4, scale_size)
        self.death_frames = self.load_frames(pygame.image.load("assets/images/level2/Death.png").convert_alpha(), 6, scale_size)
        self.dead = False
        self.hit = False
        self.death_timer = 0
        self.flight_frames = self.load_frames(flight_sheet, 8, scale_size)
        self.attack_frames = self.load_frames(attack_sheet, 8, scale_size)
        self.image = self.flight_frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vida = 2

        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_speed = 100

        self.state = "fly"
        self.target = target
        self.speed = speed

    def load_frames(self, sheet, count, scale_size):
        frames = []
        width = sheet.get_width() // count
        height = sheet.get_height()
        for i in range(count):
            frame = sheet.subsurface(pygame.Rect(i * width, 0, width, height))
            frame = pygame.transform.scale(frame, scale_size)
            frames.append(frame)
        return frames

    def update(self):
        now = pygame.time.get_ticks()

        # Se está morto, roda animação de morte
        if self.dead:
            if now - self.last_update > self.frame_speed:
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.death_frames):
                    self.kill()
                else:
                    self.image = self.death_frames[self.frame_index]
            return

        # Se está tomando dano, roda animação de hit
        if self.hit:
            if now - self.last_update > self.frame_speed:
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.hit_frames):
                    self.hit = False
                    self.state = "fly"
                    self.frame_index = 0
                else:
                    self.image = self.hit_frames[self.frame_index]
            return

        # Movimento em direção ao player
        enemy_center = self.rect.center
        target_center = self.target.rect.center
        dx = dy = 0
        if enemy_center[0] < target_center[0]:
            dx = self.speed
        elif enemy_center[0] > target_center[0]:
            dx = -self.speed

        if enemy_center[1] < target_center[1]:
            dy = self.speed
        elif enemy_center[1] > target_center[1]:
            dy = -self.speed

        self.rect.x += dx
        self.rect.y += dy

        # Define estado de ataque se perto o bastante
        distance_x = abs(self.rect.centerx - self.target.rect.centerx)
        distance_y = abs(self.rect.centery - self.target.rect.centery)
        if distance_x < 20 and distance_y < 20:
            self.state = "attack"
        else:
            self.state = "fly"

        # Animação normal (voando ou atacando)
        if now - self.last_update > self.frame_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % 8
            if self.state == "fly":
                self.image = self.flight_frames[self.frame_index]
            elif self.state == "attack":
                self.image = self.attack_frames[self.frame_index]

        # Colisão com poderes (e checagem de direção)
        for poder in self.target.poder_group:
            if now - poder.spawn_time < 50:
                continue

            if self.rect.colliderect(poder.rect):
                # Verifica se o tiro está realmente vindo na direção certa
                if poder.direction == 1 and poder.rect.centerx < self.rect.centerx:
                    continue
                if poder.direction == -1 and poder.rect.centerx > self.rect.centerx:
                    continue

                # Verifica distância real entre o centro do poder e do inimigo
                distancia_x = abs(self.rect.centerx - poder.rect.centerx)
                distancia_y = abs(self.rect.centery - poder.rect.centery)

                # Evita que o inimigo seja atingido de muito longe
                if distancia_x > 50 or distancia_y > 50:
                    continue

                # Toma dano
                self.vida -= 1
                self.hit = True
                self.state = "hit"
                self.frame_index = 0
                self.last_update = now
                poder.kill()

        # Verifica morte após aplicar dano
        if self.vida <= 0 and not self.dead:
            self.dead = True
            self.state = "dead"
            self.frame_index = 0
            self.last_update = now
            self.frame_speed = 150

def extract_frames(spritesheet, total_frames, cols, rows, scale=2):
    frames = []
    sheet_width = spritesheet.get_width()
    sheet_height = spritesheet.get_height()

    frame_width = sheet_width // cols
    frame_height = sheet_height // rows

    for index in range(total_frames):
        row = index // cols
        col = index % cols
        rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
        frame = spritesheet.subsurface(rect)
        frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
        frames.append(frame)

    return frames


class PortalSpawn(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet, enemy_group, player, flight_sheet, attack_sheet, frame_size=(64, 64), scale=2):
        super().__init__()

        self.frames = extract_frames(spritesheet, total_frames=22, cols=5, rows=5, scale=scale)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_speed = 50  # milissegundos entre frames

        # salvando os dados necessários pro spawn
        self.spawn_x = x
        self.spawn_y = y
        self.enemy_group = enemy_group
        self.player = player
        self.flight_sheet = flight_sheet
        self.attack_sheet = attack_sheet

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_speed:
            self.last_update = now
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                # cria o inimigo ao final da animação
                enemy_image = pygame.transform.scale(self.flight_sheet.subsurface((0, 0, self.flight_sheet.get_width() // 8, self.flight_sheet.get_height())), (300, 300))
                enemy_rect = enemy_image.get_rect(center=(self.spawn_x, self.spawn_y))

                enemy = FlyingEnemy(
                    enemy_rect.x, enemy_rect.y,
                    self.flight_sheet,
                    self.attack_sheet,
                    self.player
                )
                self.enemy_group.add(enemy)
                self.player.enemy_group.add(enemy)
                self.kill()
            else:
                self.image = self.frames[self.frame_index]

class ZombieEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, walk_sheet, attack_sheet, player, platforms, scale_size=(80, 80), speed=1):
        super().__init__()

        # Carregar animações com flip
        self.walk_frames_right, self.walk_frames_left = self.load_frames(walk_sheet, 8, scale_size)
        self.attack_frames_right, self.attack_frames_left = self.load_frames(attack_sheet, 7, scale_size)
        self.hit_frames_right, self.hit_frames_left = self.load_frames(pygame.image.load("assets/images/level2/Zombie hit.png").convert_alpha(), 3, scale_size)
        self.death_frames_right, self.death_frames_left = self.load_frames(pygame.image.load("assets/images/level2/Zombie morrendo.png").convert_alpha(), 5, scale_size)

        # Direção inicial aleatória
        self.facing_right = random.choice([True, False])
        self.direction = 1 if self.facing_right else -1

        # Imagem inicial
        self.image = self.walk_frames_right[0] if self.facing_right else self.walk_frames_left[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Movimento
        self.speed = speed
        self.vel_y = 0
        self.gravity = 0.5
        self.on_ground = False

        # Estado
        self.state = "walk"
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_speed = 100

        # Vida e controle
        self.health = 3
        self.hit = False
        self.dead = False
        self.ativou_diagrama = False

        # Referências
        self.platforms = platforms
        self.player = player


    def load_frames(self, sheet, count, scale_size):
        frames_right = []
        frames_left = []

        width = sheet.get_width() // count
        height = sheet.get_height()

        for i in range(count):
            frame = sheet.subsurface(pygame.Rect(i * width, 0, width, height))
            frame = pygame.transform.scale(frame, (int(scale_size[0]), int(scale_size[1])))
            frames_right.append(frame)
            frames_left.append(pygame.transform.flip(frame, True, False))

        return frames_right, frames_left


    def update(self):
        now = pygame.time.get_ticks()

        # =====================
        # Morte
        # =====================
        if self.dead:
            if now - self.last_update > self.frame_speed:
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.death_frames_right):
                    self.kill()
                else:
                    frames = self.death_frames_right if self.facing_right else self.death_frames_left
                    self.image = frames[self.frame_index]
            return

        # =====================
        # Hit
        # =====================
        if self.hit:
            if now - self.last_update > self.frame_speed:
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.hit_frames_right):
                    self.hit = False
                    self.state = "walk"
                    self.frame_index = 0
                else:
                    frames = self.hit_frames_right if self.facing_right else self.hit_frames_left
                    self.image = frames[self.frame_index]
            return

        # =====================
        # Movimento horizontal
        # =====================
        self.rect.x += self.direction * self.speed

        # Inverter direção no limite da janela
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1
            self.facing_right = self.direction > 0
            self.rect.x += self.direction * self.speed

        # =====================
        # Gravidade e colisão
        # =====================
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        self.on_ground = False

        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # =====================
        # Checar estado de ataque
        # =====================
        perto = (
            abs(self.rect.centerx - self.player.rect.centerx) < 40 and
            abs(self.rect.centery - self.player.rect.centery) < 40
        )

        if perto and self.state != "attack":
            self.state = "attack"
            self.frame_index = 0
            self.last_update = now
        elif not perto and self.state != "walk":
            self.state = "walk"
            self.frame_index = 0
            self.last_update = now

        # =====================
        # Animações (walk e attack)
        # =====================
        if now - self.last_update > self.frame_speed:
            self.last_update = now
            self.frame_index += 1

            if self.state == "walk":
                frames = self.walk_frames_right if self.facing_right else self.walk_frames_left
                if self.frame_index >= len(frames):
                    self.frame_index = 0
                self.image = frames[self.frame_index]

            elif self.state == "attack":
                frames = self.attack_frames_right if self.facing_right else self.attack_frames_left
                if self.frame_index >= len(frames):
                    self.frame_index = 0
                self.image = frames[self.frame_index]

        # =====================
        # Colisão com poderes (moedas)
        # =====================
        for poder in self.player.poder_group:
            if now - poder.spawn_time < 50:
                continue
            if self.rect.colliderect(poder.rect):
                if poder.direction == 1 and poder.rect.centerx < self.rect.centerx:
                    continue
                if poder.direction == -1 and poder.rect.centerx > self.rect.centerx:
                    continue
                self.health -= 1
                self.hit = True
                self.state = "hit"
                self.frame_index = 0
                self.last_update = now
                poder.kill()

        if self.health <= 0 and not self.dead:
            self.dead = True
            self.state = "dead"
            self.frame_index = 0
            self.last_update = now
            self.frame_speed = 150

    def apply_flip(self):
        if self.direction > 0 and not self.facing_right:
            self.facing_right = True
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.direction < 0 and self.facing_right:
            self.facing_right = False
            self.image = pygame.transform.flip(self.image, True, False)


class ZombieSpawn(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_group, player, fire, platforms, walk_sheet, attack_sheet):
        super().__init__()
        self.x = x
        self.y = y
        self.enemy_group = enemy_group
        self.player = player
        self.fire = fire
        self.platforms = platforms
        self.walk_sheet = walk_sheet
        self.attack_sheet = attack_sheet

        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_interval = random.randint(14000, 16000)

        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))  # invisível

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_timer > self.spawn_interval:
            self.spawn_timer = now
            self.spawn_interval = random.randint(14000, 16000)

            zombie = ZombieEnemy(
                self.x, self.y,
                self.walk_sheet,
                self.attack_sheet,
                player=self.player,           
                platforms=self.platforms,
                scale_size=(80, 80),
                speed=1
            )


            self.enemy_group.add(zombie)
            self.player.enemy_group.add(zombie)

class MoneyBag(pygame.sprite.Sprite):
    def __init__(self, image_sheet, platforms, player, frame_count=8, frame_width=32, frame_height=32, scale=2):
        super().__init__()

        global COLETAR_DINHEIRO_SOUND
        if not COLETAR_DINHEIRO_SOUND:
            COLETAR_DINHEIRO_SOUND = mixer.Sound("assets/sounds/level2_audio/Money.ogg")
            COLETAR_DINHEIRO_SOUND.set_volume(0.5)

        self.frames = []
        for i in range(frame_count):
            frame = image_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
            self.frames.append(frame)

        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_speed = 100

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.platforms = platforms
        self.player = player

        self.reposition()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        # Colisão com o jogador
        if self.rect.colliderect(self.player.rect):
            COLETAR_DINHEIRO_SOUND.play()
            self.player.dinheiro += 1
            if self.player.dinheiro >= 25:
                print("🎉 Você venceu!")
                return 'win'
  # chama a tela de vitória
            

            print(f"Sacos coletados: {self.player.dinheiro}")
            self.reposition()

    def reposition(self):
        plataforma = random.choice(self.platforms.sprites())
        x = random.randint(plataforma.rect.left, plataforma.rect.right - self.image.get_width())
        y = plataforma.rect.top - self.image.get_height()  # em cima da plataforma
        self.rect.topleft = (x, y)

class DiagramaAnimado(pygame.sprite.Sprite):
    def __init__(self, folder_path, pos, frame_speed=50, scale=1.0):
        super().__init__()
        self.frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                if scale != 1.0:
                    image = pygame.transform.scale(
                        image,
                        (int(image.get_width() * scale), int(image.get_height() * scale))
                    )
                self.frames.append(image)

        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_speed = frame_speed
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

        self.terminou = False

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_speed:
            self.last_update = now
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame_index]

        if self.frame_index >= len(self.frames):
            self.terminou = True
            self.kill()

class BillCipherChaser(pygame.sprite.Sprite):
    def __init__(self, x, y, image, player, speed=2):
        super().__init__()
        self.image = pygame.transform.scale(image, (100, 100))  # ajuste o tamanho conforme necessário
        self.rect = self.image.get_rect(center=(x, y))
        self.player = player
        self.speed = speed

    def update(self):
        # Movimento em direção ao player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distancia = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        self.rect.x += int(self.speed * dx / distancia)
        self.rect.y += int(self.speed * dy / distancia)

        # Colisão com player
        if self.rect.colliderect(self.player.rect):
            self.player.vida -= 2
            self.player.dinheiro = max(0, self.player.dinheiro - 5)
            print("⚠️ Bill atingiu o jogador! -2 vida, -5 dinheiro")
            self.kill()  # remove o Bill depois de acertar
