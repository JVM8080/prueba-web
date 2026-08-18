import math
import pygame


class VirtualXboxController:
    """Controle Xbox virtual para mouse/touch, compatível com o joystick físico.

    A configuração usa o mesmo padrão de botões do pygame para facilitar a
    integração com as classes de jogador já existentes:
      0 = A, 1 = B, 2 = X, 3 = Y, 4 = LB, 5 = RB, 7 = START.
    """

    BUTTON_COLORS = {
        "A": (72, 190, 120),
        "B": (220, 75, 75),
        "X": (75, 125, 220),
        "Y": (225, 195, 70),
    }

    def __init__(self, screen, physical_joystick=None):
        self.screen = screen
        self.physical_joystick = physical_joystick
        self.width, self.height = screen.get_size()

        scale = min(self.width / 800, self.height / 600)
        self.scale = max(0.75, min(scale, 1.5))

        self.stick_center = pygame.Vector2(
            int(105 * self.scale), int(self.height - 105 * self.scale)
        )
        self.stick_radius = int(58 * self.scale)
        self.knob_radius = int(25 * self.scale)
        self.stick_vector = pygame.Vector2(0, 0)
        self.stick_active = False
        self.stick_pointer_id = None

        self.buttons = {
            0: self._make_button("A", 675, self.height - 98),
            1: self._make_button("B", 750, self.height - 145),
            2: self._make_button("X", 600, self.height - 145),
            3: self._make_button("Y", 675, self.height - 192),
            4: self._make_button("LB", 82, 72),
            5: self._make_button("RB", self.width - 82, 72),
            7: self._make_button("START", self.width // 2, self.height - 48, 68, 28),
        }

        self._pressed = {button_id: False for button_id in self.buttons}
        self._pointer_buttons = {}
        self.pause_just_pressed = False

        self.left_zone = pygame.Rect(
            18,
            int(self.height - 180 * self.scale),
            int(175 * self.scale),
            int(170 * self.scale),
        )

    def _make_button(self, label, x, y, radius=29, height=None):
        radius = int(radius * self.scale)
        if label in {"LB", "RB"}:
            size = (int(58 * self.scale), int(28 * self.scale))
            rect = pygame.Rect(0, 0, *size)
            rect.center = (int(x), int(y))
            return {"label": label, "rect": rect, "radius": 0}
        if label == "START":
            width = int(radius * self.scale)
            rect = pygame.Rect(0, 0, int(width), int(height * self.scale))
            rect.center = (int(x), int(y))
            return {"label": label, "rect": rect, "radius": 0}

        radius = max(16, radius)
        rect = pygame.Rect(0, 0, radius * 2, radius * 2)
        rect.center = (int(x), int(y))
        return {"label": label, "rect": rect, "radius": radius}

    def set_physical_joystick(self, joystick):
        self.physical_joystick = joystick

    def get_axis(self, axis):
        # O analógico virtual assume prioridade enquanto estiver sendo usado.
        if self.stick_active:
            return self.stick_vector.x if axis == 0 else self.stick_vector.y

        if self.physical_joystick is not None:
            try:
                return self.physical_joystick.get_axis(axis)
            except pygame.error:
                pass

        return 0.0

    def get_button(self, button):
        virtual_pressed = self._pressed.get(button, False)
        physical_pressed = False

        if self.physical_joystick is not None:
            try:
                physical_pressed = bool(self.physical_joystick.get_button(button))
            except pygame.error:
                pass

        return virtual_pressed or physical_pressed

    def _position_from_event(self, event):
        if event.type in (pygame.FINGERDOWN, pygame.FINGERMOTION, pygame.FINGERUP):
            return pygame.Vector2(event.x * self.width, event.y * self.height)
        return pygame.Vector2(event.pos)

    def _pointer_id(self, event):
        if event.type in (pygame.FINGERDOWN, pygame.FINGERMOTION, pygame.FINGERUP):
            return event.finger_id
        return "mouse"

    def _update_stick(self, position):
        offset = pygame.Vector2(position) - self.stick_center
        max_distance = float(self.stick_radius)
        if offset.length() > max_distance:
            offset.scale_to_length(max_distance)
        self.stick_vector.x = offset.x / max_distance
        self.stick_vector.y = offset.y / max_distance

    def _button_at(self, position):
        for button_id, data in self.buttons.items():
            rect = data["rect"]
            radius = data["radius"]
            if radius > 0:
                if pygame.Vector2(position).distance_to(rect.center) <= radius + 8:
                    return button_id
            elif rect.collidepoint(position):
                return button_id
        return None

    def handle_event(self, event):
        """Processa mouse/touch e retorna True quando START foi pressionado."""
        if event.type == pygame.WINDOWFOCUSLOST:
            self.reset()
            return False

        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
            pointer_id = self._pointer_id(event)
            position = self._position_from_event(event)

            if self.left_zone.collidepoint(position) or (
                pygame.Vector2(position).distance_to(self.stick_center) <= self.stick_radius + 18
            ):
                self.stick_active = True
                self.stick_pointer_id = pointer_id
                self._update_stick(position)
                return False

            button_id = self._button_at(position)
            if button_id is not None:
                self._pointer_buttons[pointer_id] = button_id
                self._pressed[button_id] = True
                if button_id == 7:
                    self.pause_just_pressed = True
                    return True

        elif event.type in (pygame.MOUSEMOTION, pygame.FINGERMOTION):
            pointer_id = self._pointer_id(event)
            position = self._position_from_event(event)
            if self.stick_active and pointer_id == self.stick_pointer_id:
                self._update_stick(position)

        elif event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
            pointer_id = self._pointer_id(event)
            if self.stick_active and pointer_id == self.stick_pointer_id:
                self.stick_active = False
                self.stick_pointer_id = None
                self.stick_vector.update(0, 0)

            button_id = self._pointer_buttons.pop(pointer_id, None)
            if button_id is not None:
                self._pressed[button_id] = any(
                    active_button == button_id for active_button in self._pointer_buttons.values()
                )

        return False

    def consume_pause(self):
        pressed = self.pause_just_pressed
        self.pause_just_pressed = False
        return pressed

    def reset(self):
        self.stick_active = False
        self.stick_pointer_id = None
        self.stick_vector.update(0, 0)
        self._pointer_buttons.clear()
        for button_id in self._pressed:
            self._pressed[button_id] = False
        self.pause_just_pressed = False

    def _draw_button(self, data, button_id):
        label = data["label"]
        rect = data["rect"]
        pressed = self._pressed.get(button_id, False)

        if label in self.BUTTON_COLORS:
            center = rect.center
            radius = data["radius"]
            color = self.BUTTON_COLORS[label]
            outer = (35, 35, 45, 145)
            pygame.draw.circle(self.screen, outer[:3], center, radius + 6)
            pygame.draw.circle(self.screen, color, center, radius - (3 if pressed else 0))
            if pressed:
                pygame.draw.circle(self.screen, (255, 255, 255), center, radius - 2, 2)
        else:
            color = (70, 70, 85) if not pressed else (110, 110, 130)
            pygame.draw.rect(self.screen, (25, 25, 35), rect.inflate(8, 8), border_radius=9)
            pygame.draw.rect(self.screen, color, rect, border_radius=7)

        font_size = max(12, int(20 * self.scale))
        font = pygame.font.SysFont("arial", font_size, bold=True)
        text = font.render(label, True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=rect.center))

    def draw(self, enabled=True):
        if not enabled:
            return

        # Analógico esquerdo
        pygame.draw.circle(
            self.screen,
            (25, 25, 35),
            self.stick_center,
            self.stick_radius + 9,
        )
        pygame.draw.circle(
            self.screen,
            (65, 65, 78),
            self.stick_center,
            self.stick_radius,
        )

        knob_offset = self.stick_vector * self.stick_radius
        knob_center = self.stick_center + knob_offset
        pygame.draw.circle(self.screen, (35, 35, 45), knob_center, self.knob_radius + 4)
        pygame.draw.circle(self.screen, (120, 120, 135), knob_center, self.knob_radius)

        # Botões Xbox.
        for button_id, data in self.buttons.items():
            self._draw_button(data, button_id)

        # Legenda discreta para indicar que é possível tocar/clicar.
        font = pygame.font.SysFont("arial", max(10, int(13 * self.scale)))
        text = font.render("CONTROLE", True, (220, 220, 220))
        self.screen.blit(text, (self.width - text.get_width() - 12, self.height - 20))
