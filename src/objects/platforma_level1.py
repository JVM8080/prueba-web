import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, surface, x, y, width=None, height=None, animated=False, frames=None, frame_delay=5):
        super().__init__()

        self.animated = animated
        self.frame_delay = frame_delay
        self.current_frame = 0
        self.frame_count = 0

        if self.animated and frames:
            self.frames = frames
            if width and height:
                self.frames = [pygame.transform.scale(f, (width, height)) for f in self.frames]
            self.image = self.frames[0]
        else:
            self.image = surface
            if width and height:
                self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        if self.animated:
            self.frame_count += 1
            if self.frame_count >= self.frame_delay:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                self.frame_count = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
