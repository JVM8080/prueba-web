import pygame

# Classe que representa a tela de pausa
class PauseScreen:
    def __init__(self, screen, width=450, height=300):
        self.screen = screen
        self.width = width
        self.height = height
        self.active = False  # Estado da tela de pausa (ativa ou não)

        # Tenta carregar fontes personalizadas, se não conseguir usa fontes do sistema
        try:
            self.font = pygame.font.Font("assets/fonts/roboto-bold.ttf", 48)
            self.button_font = pygame.font.Font("assets/fonts/roboto-regular.ttf", 24)
        except:
            self.font = pygame.font.SysFont("Arial", 48, bold=True)
            self.button_font = pygame.font.SysFont("Arial", 24)

        # Define a posição da caixa central da tela de pausa
        self.rect = self._centered_rect(self.width, self.height)

        # Define os botões da tela de pausa com seus respectivos rótulos e posições
        self.buttons = {
            'continue': self._create_button("Continuar", 80),
            'level_select': self._create_button("Selecionar Nivel", 140),
            'menu': self._create_button("Menu", 200)
        }

        # Cores usadas na interface
        self.bg_color = (30, 30, 40, 180)  # Fundo semi-transparente
        self.button_color = (70, 130, 230)  # Cor dos botões
        self.hover_color = (100, 160, 255)  # Cor dos botões ao passar o mouse
        self.text_color = (255, 255, 255)   # Cor do texto
        self.title_color = (255, 215, 0)    # Cor do título "PAUSA"

    # Cria um retângulo centralizado com as dimensões informadas
    def _centered_rect(self, width, height):
        screen_w, screen_h = self.screen.get_size()
        return pygame.Rect(
            (screen_w - width) // 2,
            (screen_h - height) // 2,
            width,
            height
        )

    # Cria um botão com texto e deslocamento vertical
    def _create_button(self, label, offset_y):
        rect = pygame.Rect(
            self.rect.left + (self.width - 220) // 2,
            self.rect.top + offset_y,
            220,
            45
        )
        return {'rect': rect, 'label': label}

    # Ativa a tela de pausa
    def show(self):
        self.active = True

    # Desativa a tela de pausa
    def hide(self):
        self.active = False

    # Atualização da tela de pausa (sem uso no momento)
    def update(self, dt):
        pass  # Sem animações implementadas

    # Desenha a tela de pausa e seus componentes
    def draw(self):
        if not self.active:
            return  # Não desenha nada se a tela não estiver ativa

        # Cria uma superfície semi-transparente para o fundo da caixa de pausa
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(overlay, self.bg_color, (0, 0, self.width, self.height), border_radius=15)
        
        # Posiciona o fundo da caixa na tela
        self.screen.blit(overlay, self.rect.topleft)

        # Desenha o título "PAUSA"
        self._draw_title("PAUSA", self.rect.centerx, self.rect.top + 10)

        # Desenha os botões
        for btn in self.buttons.values():
            self._draw_button(btn['rect'], btn['label'])

    # Desenha o título centralizado no topo da caixa
    def _draw_title(self, text, center_x, y):
        main_text = self.font.render(text, True, self.title_color)
        self.screen.blit(main_text, (center_x - main_text.get_width() // 2, y))

    # Desenha um botão com rótulo e efeito de hover
    def _draw_button(self, rect, label):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hovered else self.button_color

        pygame.draw.rect(self.screen, color, rect, border_radius=8)

        text_surface = self.button_font.render(label, True, self.text_color)
        self.screen.blit(text_surface, (
            rect.centerx - text_surface.get_width() // 2,
            rect.centery - text_surface.get_height() // 2
        ))

    # Trata eventos de clique do mouse sobre os botões
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for action, btn in self.buttons.items():
                if btn['rect'].collidepoint(mouse_pos):
                    return action  # Retorna a ação associada ao botão clicado
        return None  # Nenhuma ação foi clicada
