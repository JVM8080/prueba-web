# Pygame DesSoft – Gravity Falls

### Integrantes do grupo:

* Julián Esteban Vargas Montaño.
* Sophia Montecinos Kalil.
* Felipe Campos Leite Lima.

Este projeto é um jogo digital desenvolvido por estudantes do Insper como parte de uma atividade acadêmica. Foi implementado em Python utilizando a biblioteca Pygame, com o objetivo de explorar conceitos de programação, lógica de jogos e design interativo. Todos os recursos gráficos e sonoros utilizados foram obtidos de fontes livres e abertas disponíveis na internet, respeitando as licenças de uso e promovendo o uso ético de conteúdo digital.

## Como executar o jogo:

1. Ative o ambiente virtual com as bibliotecas necessárias (consulte o passo 1 mais abaixo).
2. Edite o arquivo `config.py` para ajustar suas preferências de áudio e desempenho. As variáveis relevantes são:

   ```
   FPS = 90
   SOUND_VOLUME_SFX = 0.3
   SOUND_VOLUME_MUSIC = 0.5
   ```
3. Estando na pasta raiz do repositório, execute o jogo com o seguinte comando no terminal, ou abra o arquivo `main.py` com o VS Code e execute por lá:

   ```
   python main.py
   ```

**Pd: O jogo foi feito para controle de Xbox One.**

## Video do jogo funcionando:

Link: [Pygame Gravity Falls – 100% Complete [All Levels] | Julián Vargas – Sophia Kalil – Felipe Campos](https://youtu.be/4lXOMEJS7yI)

## Estrutura de pastas e arquivos

```
PyGameDesSoft/
│
├── assets/                # Pasta para recursos do jogo (imagens, sons, fontes)
│   ├── images/
│   │   ├── background.png
│   │   ├── player.png
│   │   └── ...
│   ├── sounds/
│   └── fonts/
│
├── src/                   # Código fonte principal do jogo
│   ├── __init__.py        # Arquivo __init__.py para permitir a importação dos módulos da pasta.
│   ├── screens/           # Telas do jogo (cada uma em um arquivo separado)
│   │   ├── __init__.py    # Arquivo __init__.py para permitir a importação dos módulos da pasta.
│   │   ├── main_menu.py   # Tela inicial do jogo com botão de play
│   │   ├── level_select.py # Tela de seleção de nível/mapa
│   │   └── game_screen.py # Tela principal do jogo
│   │
│   ├── objects/           # Classes dos objetos do jogo
│   │   ├── __init__.py    # Arquivo __init__.py para permitir a importação dos módulos da pasta.
│   │   ├── player.py      # Classe do jogador principal
│   │   └── obstacles.py   # Classe dos obstáculos
│   │   └── ...
│   │
│   ├── utils/             # Utilitários do jogo
│   │   ├── __init__.py    # Arquivo __init__.py para permitir a importação dos módulos da pasta.
│   │   ├── collision.py   # Sistema de detecção de colisões
│   │   └── asset_loader.py # Carregador de recursos (imagens, sons)
│   │   └── ...
│   │
│   ├── levels/            # Níveis do jogo
│   │   ├── __init__.py    # Arquivo __init__.py para permitir a importação dos módulos da pasta.
│   │   ├── level_1.py     # Nível 1
│   │   ├── level_2.py     # Nível 2
│   │   └── level_3.py     # Nível 3
│
├── .gitignore             # Arquivos ignorados no repositorio
├── config.py              # Arquivo de configurações globais (resolução, FPS, caminhos etc.)
├── main.py                # Ponto de entrada principal do jogo (inicialização e loop principal)
└── README.md              # Arquivo Readme
└── requirements.txt       # Dependências do projeto (pygame etc.)

```

## 1. Ambiente virtual de Python

* Crie um ambiente virtual, para isso digite dentro da raiz os seguintes comandos em ordem (no Mac ou Linux):

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

* Caso use Windows:

```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

* Lembre-se de ativar o ambiente virtual antes de executar o jogo!

## 2. Fluxo de trabalho com Git – Pull Requests e Issues

### Para contribuir com o projeto:

1. **Crie uma branch a partir da `main`:**

```bash
git checkout main #Volta pra branch main
git pull origin main #Sincroniza o repositorio
git checkout -b sua-feature-aqui # Cria a branch donde vc quer trabalhar
```

2. **Desenvolva e faça commits claros (exemplo):**

```bash
git add . # Adiciona as mudanças do diretorio atual
git commit -m "feat: adiciona tela de contato" #Cria o commit
```

3. **Suba sua branch:**

```bash
git push origin sua-feature-aqui #Envia a branch com os commit para criar o Pull Request (PR) no Github 
```

4. **Abra um Pull Request no GitHub:**

- Base: `main`
- Compare: `sua-feature-aqui`
- Preencha o título e a descrição do PR (ligue a issue com `Closes #número_da_issue` na descrição, quando você digitar `Closes #` já irá listar as issues)

5. **Espere aprovação para merge.**

- O Admin irá testar o PR, e posteriormente aceitar ou recusar. Se tiver algum erro será comunicado pelo grupo de Whats.

## 3. Fontes usadas no trabalho

Exemplo: A função `funcao-do-jogo()` do arquivo   `diretorio/arquivo.py` foi desenvolvida pela IA [www.blackbox.ai](https://www.blackbox.ai/).

* A estrutura de pastas e arquivos foi obtida pela IA [chat.deepseek.com](chat.deepseek.com).
* Os arquivos iniciais do repositorio foram obtidos pela IA [chatgpt.com](https://chatgpt.com/).
* Os recursos gráficos foram obtidos no link a seguir: [Fravity Falls Pinesquest 2d](https://novastarlyght.itch.io/gravity-falls-pinesquest-2d).
* Alguns recursos de audio foram usados do jogo [Cuphead ](https://cupheadgame.com/)desarrollado pela empresa [Studio MDHR](https://www.google.com/search?sca_esv=a983052df2b98a8d&rlz=1C1ONGR_esCO1042CO1042&sxsrf=AE3TifMBRX8On7N2blnc0Xh4W1OVJZTaXg:1748368410965&q=Studio+MDHR&si=AMgyJEs9DArPE9xmb5yVYVjpG4jqWDEKSIpCRSjmm88XZWnGNdOJzdIqw1FvSSFjTPqRvqXkvD8Mz6-uTHgr2UaM157q_jPUncigFsVSpKi8ORSqiwPjQtRjZYUIA3j_N44YFxYHGDnctAu1ltw4j97MeAUW1Fga3T38s-sjsS2SkGFcPORI3urthU6nytiAYmI-hYoXuxVTgJD0f5FnTMEMU69EMC3omg%3D%3D&sa=X&ved=2ahUKEwinysnwm8SNAxVmqZUCHVd2CCAQmxN6BAglEAI).
* Alguns recursos de audio foram usados do jogo [Geometry Dash](https://www.robtopgames.com/) desarrollado pela empresa [RobTop Games](https://www.robtopgames.com/).
* Alguns membros do trabalho usaram [Github Copilot](https://github.com/features/copilot) e [Windsuft AI](https://windsurf.com/editor) como IA de ajuda durante o desarrollo do jogo.

## Executar no navegador com Pygbag

Este projeto foi preparado para ser empacotado como WebAssembly com Pygbag.

### 1. Instalar as dependencias

No ambiente virtual:

```powershell
pip install -r requirements.txt
```

### 2. Executar localmente no navegador

Na raiz do projeto, onde esta o `main.py`:

```powershell
python -m pygbag .
```

Depois, abra no navegador o endereco mostrado pelo Pygbag, normalmente:

```text
http://localhost:8000
```

### 3. Gerar apenas a build web

```powershell
python -m pygbag --build .
```

Os arquivos da versao web ficam em `build/web/`.

### Observacoes

- O projeto usa `pygame-ce`, porque o Pygbag atual suporta pygame-ce para a versao WebAssembly.
- O arquivo `main.py` usa `asyncio` e o loop principal cede o controle ao navegador com `await asyncio.sleep(0)`.
- As telas e niveis que possuem loops proprios tambem foram convertidos para funcoes `async`.
