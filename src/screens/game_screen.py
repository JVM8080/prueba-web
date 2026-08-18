# Importa os módulos que contêm os diferentes níveis do jogo
from src.levels import level_1, level_2, level_3

# Função principal da tela de jogo, que recebe a tela e o número do nível selecionado
async def game_screen(screen, level):
    # Se o nível selecionado for 1, executa o nível 1
    if level == 1:
        return await level_1.run(screen)
    # Se o nível selecionado for 2, executa o nível 2
    elif level == 2:
        return await level_2.run(screen)
    # Se o nível selecionado for 3, executa o nível 3
    elif level == 3:
        return await level_3.run(screen)
