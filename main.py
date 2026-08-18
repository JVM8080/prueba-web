import asyncio
import pygame
from config import *
from src.screens.main_menu import main_menu
from src.screens.level_select import level_select
from src.screens.game_screen import game_screen

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGameDesSoft")
clock = pygame.time.Clock()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Joystick conectado:", joystick.get_name())
else:
    joystick = None

async def main():
    state = 'menu'
    selected_level = 1

    while True:
        if state == 'menu':
            state = await main_menu(screen)
        elif state == 'level_select':
            state, selected_level = await level_select(screen)
        elif state == 'game':
            state = await game_screen(screen, selected_level)
        elif state == 'quit':
            return

        # Entrega o controle ao navegador/WebAssembly a cada ciclo.
        await asyncio.sleep(0)

asyncio.run(main())
