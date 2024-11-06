import pygame
import random
import sys

## Inicializa o Pygame
pygame.init()
# Inicializa o módulo de sons e música do Pygame
pygame.mixer.init()

# Janela do jogo
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

## Variáveis globais de tela
# Variável que controla a tela de opções
options = False
# Variável que sabe se o jogo acabou
ended = False
# Variáveis que controlam a função de pausar o jogo
pause = False
pvar = False

# Variáveis para facilitar referenciar diferentes cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 109, 255)

## Setup inicial

# Variáveis iniciais de velocidade
PLAYER_SPEED = 5
BG_SPEED = 7
# Variável que sabe se a música está tocando
music = True
# Variável que sabe qual modelo de jogador está escolhido
chosen = 1
# Tempo que o jogador fica invulnerável depois que toma dano
INV_TIME = 2000
# Variável auxiliar para timers
n = 10000000000000

# Configura highscore a partir do arquivo txt
file = open("./resources/highscore.txt", "r")
HIGHSCORE = int(file.read())
file.close()

## Variáveis globais
# Variáveis que controlam em qual nível o jogo está
nivel = 1
nivel_choice = 1
# Variável global que controla pontuação
score = 0
# Variáveis que sabem se tomamos dano ou encontramos um powerup
hit = False
pow = False
# Variável que controla onde a avalanche deve ir
avalanche_target = 1170
# Variáveis que sabem quais modelos de jogador foram desbloqueados
player2unlocked = False
player3unlocked = False
player4unlocked = False
# Variáveis que sabem quais dificuldades foram desbloqueadas
diff2unlock = False
diff3unlock = False
diff4unlock = False

### Timers usados no jogo
# Timer para criar powerups periodicamente
PSPAWN = pygame.USEREVENT+1
# Timer para parar efeito de powerups periodicamente
PSTOP = pygame.USEREVENT + 2
# Timer que rapidamente alterna a frame de animação da avalanche
AVANIM = pygame.USEREVENT + 3
## Inicializar timers, o segundo parâmetro controla quantos millisegundos para cada um
# Os timers executam cada vez que esse valor de millisegundos passa
pygame.time.set_timer(PSPAWN, 6500)
pygame.time.set_timer(PSTOP, 5000)
pygame.time.set_timer(AVANIM, 500)

# O clock do pygame permite controlar o FPS (frames por segundo) do jogo
clock = pygame.time.Clock()

## Carregando imagem de fundo
background = pygame.image.load('./resources/bg.png')
# Variável que sabe onde a imagem de fundo está
background_y = 0

# Carregando imagens de botão
botao = pygame.image.load('./resources/button.png').convert_alpha()
botao2 = pygame.image.load('./resources/button2.png').convert_alpha()
botao3 = pygame.image.load('./resources/button3.png').convert_alpha()
mbotao = pygame.image.load('./resources/mbutton.png').convert_alpha()
mbotao2 = pygame.image.load('./resources/mbutton2.png').convert_alpha()
mbotao3 = pygame.image.load('./resources/mbutton3.png').convert_alpha()
player2botao = pygame.image.load('./resources/p2button.png').convert_alpha()
player2botao2 = pygame.image.load('./resources/p2button2.png').convert_alpha()
player2botao3 = pygame.image.load('./resources/p2button3.png').convert_alpha()
player3botao = pygame.image.load('./resources/p3button.png').convert_alpha()
player3botao2 = pygame.image.load('./resources/p3button2.png').convert_alpha()
player3botao3 = pygame.image.load('./resources/p3button3.png').convert_alpha()
player4botao = pygame.image.load('./resources/p4button.png').convert_alpha()
player4botao2 = pygame.image.load('./resources/p4button2.png').convert_alpha()
player4botao3 = pygame.image.load('./resources/p4button3.png').convert_alpha()

## Sprite de botão
# Parametros em ordem: posição (x e y), se está ativo (boolean), o texto do botão, a fonte do texto, o tipo de botão
# Os três últimos parâmetros são opcionais e tem valores padrões se não incluídos
# Tipo 1 é o botão normal com texto
# Tipo 2 é botão para mudar música
# Tipo 3 é botão com imagem do modelo 2 de jogador
# Tipo 4 é botão com imagem do modelo 3 de jogador
# Tipo 5 é botão com imagem do modelo 4 de jogador
class Button( pygame.sprite.Sprite ):
    # Esse método inicializa a sprite e processa os parâmetros dados
    def __init__(self, x, y, active, text="", font=pygame.font.Font("./resources/upheavtt.ttf", 36), type=1):
        pygame.sprite.Sprite.__init__( self )
        self.type = type
        self.image = botao
        # Cada tipo diferente de botão tem imagens diferentes
        if self.type == 2:
            self.image = mbotao
        if self.type == 3:
            self.image = player2botao
        if self.type == 4:
            self.image = player3botao
        if self.type == 5:
            self.image = player4botao
        self.rect = self.image.get_rect()
        self.rect.center = ( x-30, y )
        self.text = text
        self.active = active
        self.font = font
        
    # Desenhar o botão
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        x,y = self.rect.center

        # Mudar cor se o mouse está em cima/desativado
        if self.active and self.type == 1:
            if self.rect.collidepoint(mouse_pos):
                self.image = botao2
                screen.blit(self.image, (x-80, y-15))
            else:
                self.image = botao
                screen.blit(self.image, (x-80, y-15))
        elif not self.active and self.type == 1:
            self.image = botao3
            screen.blit(self.image, (x-80, y-15))
        elif self.active and self.type == 2:
            if self.rect.collidepoint(mouse_pos):
                self.image = mbotao2
                screen.blit(self.image, (x-80, y-15))
            else:
                self.image = mbotao
                screen.blit(self.image, (x-80, y-15))
        elif not self.active and self.type == 2:
            self.image = mbotao3
            screen.blit(self.image, (x-80, y-15))
        elif self.active and self.type == 3:
            if self.rect.collidepoint(mouse_pos):
                self.image = player2botao2
                screen.blit(self.image, (x-80, y-15))
            else:
                self.image = player2botao
                screen.blit(self.image, (x-80, y-15))
        elif not self.active and self.type == 3:
            self.image = player2botao3
            screen.blit(self.image, (x-80, y-15))
        elif self.active and self.type == 4:
            if self.rect.collidepoint(mouse_pos):
                self.image = player3botao2
                screen.blit(self.image, (x-80, y-15))
            else:
                self.image = player3botao
                screen.blit(self.image, (x-80, y-15))
        elif not self.active and self.type == 4:
            self.image = player3botao3
            screen.blit(self.image, (x-80, y-15))
        elif self.active and self.type == 5:
            if self.rect.collidepoint(mouse_pos):
                self.image = player4botao2
                screen.blit(self.image, (x-80, y-15))
            else:
                self.image = player4botao
                screen.blit(self.image, (x-80, y-15))
        elif not self.active and self.type == 5:
            self.image = player4botao3
            screen.blit(self.image, (x-80, y-15))

        # Desenhar o texto por cima, a partir da variável text (apenas se o botão for de tipo 1)
        if not type == 2 and not type == 3 and not type == 4 and not type == 5:
            font = self.font
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(x+2,y+15))
            screen.blit(text_surface, text_rect)

# Carregar imagem dos obstaculos
load_img = pygame.image.load('./resources/log.png').convert_alpha()
tronco_img = pygame.transform.scale(load_img, (50,50))

# Carregar imagens dos powerups
load_img = pygame.image.load('./resources/powerup.png').convert_alpha()
pup_img = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/powerup2.png').convert_alpha()
pup_img2 = pygame.transform.scale(load_img, (50,50))

# Carregar imagens da avalanche
load_img = pygame.image.load('./resources/avalanche1.png').convert_alpha()
ava_img = pygame.transform.scale(load_img, (600,900))
load_img = pygame.image.load('./resources/avalanche2.png').convert_alpha()
ava_img2 = pygame.transform.scale(load_img, (600,900))

# Carregar imagem das marcas
load_img = pygame.image.load('./resources/track.png').convert()
tra_img = pygame.transform.scale(load_img, (50,50))

# Carregar imagens do personagem (esquiador)
load_img = pygame.image.load('./resources/player1.png').convert_alpha()
player_normal = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player1hurt.png').convert_alpha()
player_hurt = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player1power.png').convert_alpha()
player_power = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player1left.png').convert_alpha()
player_left = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player1right.png').convert_alpha()
player_right = pygame.transform.scale(load_img, (50,50))

# Carregar imagens do modelo 2 de personagem
load_img = pygame.image.load('./resources/player2.png').convert_alpha()
player2_normal = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player2hurt.png').convert_alpha()
player2_hurt = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player2power.png').convert_alpha()
player2_power = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player2left.png').convert_alpha()
player2_left = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player2right.png').convert_alpha()
player2_right = pygame.transform.scale(load_img, (50,50))

# Carregar imagens do modelo 3 de personagem
load_img = pygame.image.load('./resources/player3.png').convert_alpha()
player3_normal = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player3hurt.png').convert_alpha()
player3_hurt = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player3power.png').convert_alpha()
player3_power = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player3left.png').convert_alpha()
player3_left = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player3right.png').convert_alpha()
player3_right = pygame.transform.scale(load_img, (50,50))

# Carregar imagens do modelo 4 de personagem
load_img = pygame.image.load('./resources/player4.png').convert_alpha()
player4_normal = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player4hurt.png').convert_alpha()
player4_hurt = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player4power.png').convert_alpha()
player4_power = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player4left.png').convert_alpha()
player4_left = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/player4right.png').convert_alpha()
player4_right = pygame.transform.scale(load_img, (50,50))

# Configuração inicial do jogador
player_img = player_normal
player_rect = player_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 220))

# Carregar imagem para o pause
pausebg = pygame.image.load('./resources/pausebg.png').convert_alpha()

## Configurar layers
# Esta variável armazena sprites em camadas numeradas, e funciona como um grupo de sprites
# Camadas de números maiores desenham por cima de camadas de números menores
layers = pygame.sprite.LayeredUpdates()

# Carregar sons
hit_sound = pygame.mixer.Sound("./resources/hit.mp3")
pup_sound = pygame.mixer.Sound("./resources/powerup.mp3")
gameover_sound = pygame.mixer.Sound("./resources/gameover.mp3")
diffchange_sound = pygame.mixer.Sound("./resources/diffchange.mp3")
unlock_sound = pygame.mixer.Sound("./resources/unlock.mp3")
fail_sound = pygame.mixer.Sound("./resources/fail.mp3")
select_sound = pygame.mixer.Sound("./resources/select.mp3")

## Sprite do jogador
# O parâmetro layer determina em qual camada será desenhado
class Player( pygame.sprite.Sprite ):
    # Esse método inicializa a sprite e processa os parâmetros dados
    def __init__( self, layer=1 ):   
        pygame.sprite.Sprite.__init__( self )
        # Dependendo de qual modelo está escolhido, utilizar a imagem correspondente
        if chosen == 1:
            self.image = player_normal
        elif chosen == 2:
            self.image = player2_normal
        elif chosen == 3:
            self.image = player3_normal
        elif chosen == 4:
            self.image = player4_normal
        # Configurar o retângulo de colisão e posição da imagem
        self.rect  = self.image.get_rect()     
        self.rect.center = ( SCREEN_WIDTH // 2, SCREEN_HEIGHT - 220 )
        # Número da camada
        self._layer = layer

    # Método update
    # Atualiza imagens e movimento
    def update( self ):
        x, y = self.rect.center
        keys = pygame.key.get_pressed()
        left = False
        right = False
        
        # Movimentação do jogador baseado em botões apertados
        # Roda apenas se o jogo não terminou 
        if not ended:  
            if ( keys[pygame.K_LEFT] ):
                left = True
                x -= PLAYER_SPEED
            elif ( keys[pygame.K_RIGHT] ):
                right = True
                x += PLAYER_SPEED
            elif ( keys[pygame.K_UP] ):
                y -= PLAYER_SPEED
            elif ( keys[pygame.K_DOWN] ):
                y += PLAYER_SPEED
            else:
                left = False
                right = False

        # Impedir o jogador de sair da tela
        if x < 0:
            x = 0
        if x > SCREEN_WIDTH-30:
            x = SCREEN_WIDTH-30
        self.rect.center = ( x, y )

        # Mudar imagem de acordo com o estado do jogador (e de acordo com modelo escolhido)
        if hit:
            if chosen == 1:
                self.image = player_hurt
            elif chosen == 2:
                self.image = player2_hurt
            elif chosen == 3:
                self.image = player3_hurt
            elif chosen == 4:
                self.image = player4_hurt
        elif pow:
            if chosen == 1:
                self.image = player_power
            elif chosen == 2:
                self.image = player2_power
            elif chosen == 3:
                self.image = player3_power
            elif chosen == 4:
                self.image = player4_power
        elif left:
            if chosen == 1:
                self.image = player_left
            elif chosen == 2:
                self.image = player2_left
            elif chosen == 3:
                self.image = player3_left
            elif chosen == 4:
                self.image = player4_left
        elif right:
            if chosen == 1:
                self.image = player_right
            elif chosen == 2:
                self.image = player2_right
            elif chosen == 3:
                self.image = player3_right
            elif chosen == 4:
                self.image = player4_right
        else:
            if chosen == 1:
                self.image = player_normal
            elif chosen == 2:
                self.image = player2_normal
            elif chosen == 3:
                self.image = player3_normal
            elif chosen == 4:
                self.image = player4_normal

## Grupo para a sprite do jogador
# Normalmente se armazena sprites em grupos categorizados para separação, organização e controle de vários itens de uma vez
# Como só existe um jogador, utiliza-se GroupSingle, que é um grupo de 1 item
player = pygame.sprite.GroupSingle()

## Sprite das marcas de ski na neve
# O parâmetro player serve para referenciar a sprite do jogador, e layer determina em qual camada será desenhado
class Track( pygame.sprite.Sprite ):
    # Esse método inicializa a sprite e processa os parâmetros dados
    def __init__( self,  player, layer=0 ):   
        pygame.sprite.Sprite.__init__( self ) 
        self.image = tra_img
        # Configurar o retângulo de colisão e posição da imagem
        self.rect  = self.image.get_rect()     
        self.rect.center = ( player )
        # Número da camada
        self._layer = layer

    # Método update
    # Atualiza o movimento
    def update( self ):
        x, y = self.rect.center

        # Movimentar as marcas para baixo
        y += 7

        # Apagar marcas que saem da tela
        if y > SCREEN_HEIGHT:
            self.kill()
        self.rect.center = ( x, y )

# Grupo para as sprites de marcas     
tracks = pygame.sprite.Group()

## Sprite dos obstáculos
# O parâmetro layer determina em qual camada será desenhado
class Obstacle( pygame.sprite.Sprite ): 
    # Esse método inicializa a sprite e processa os parâmetros dados
    def __init__( self, layer=2 ):   
        pygame.sprite.Sprite.__init__( self ) 
        self.image = tronco_img
        # Configurar o retângulo de colisão e posição da imagem
        self.rect  = self.image.get_rect()
        # Para garantir que os obstáculos vão cair de pontos aleatórios do topo da tela,
        # iniciamos a posição com valores aleatórios
        # Utilizar uma altura aleatória fora da tela faz com que cada obstáculo caia em um momento diferente
        self.y = random.randint(-1000,-100)
        self.x = random.randint(0, SCREEN_WIDTH - 10)
        self.rect.center = ( self.x, self.y )
        # Número da camada
        self._layer = layer

    ## Método update
    # Atualiza velocidade, movimento e estado
    def update( self ):
        ## Avisar o código que não estamos referenciando estas variáveis apenas localmente
        # Precisamos fazer isto pois iremos modificar variáveis que foram declaradas no escopo global
        # Obs.: Utilizar chamadas globais não é ideal pois dificulta debugging
        # Foram utilizadas neste código pois debugging complexo não é uma necessidade neste projeto, e para manter o código mais legível
        global score, BG_SPEED

        # Deixar obstáculos mais rápidos de acordo com dificuldade
        # A condição intermediária em cada nível estabelece limites para a velocidade
        if nivel == 2:
            if BG_SPEED < 8:   
                BG_SPEED += 2
        if nivel == 3:
            if BG_SPEED < 11:
                BG_SPEED += 3
        if nivel == 4:
            if BG_SPEED < 15:
               BG_SPEED += 4

        # Obter posição do obstáculo a partir de seu retângulo
        x, y = self.rect.center

        # Movimentar obstáculos para baixo
        y += BG_SPEED

        # Apagar obstáculos que saem da tela
        if y > SCREEN_HEIGHT:
            self.kill()
            # Quando apagamos um obstáculo, criamos outro no topo da tela
            # (para garantir que sempre terá pelo menos um obstáculo no jogo)
            obstaculos.add(Obstacle())
            # Aumentar pontuação quando um obstáculo sai da tela
            score += 1
            # Se quando aumentamos a pontuação passamos para outra dificuldade,
            # Toca o som que indica mudança de dificuldade
            if score == 50:
                diffchange_sound.play()
            elif score == 100:
                diffchange_sound.play()
            elif score == 200:
                diffchange_sound.play()
        # Atualizar o retângulo com as posições que foram modificadas
        self.rect.center = ( x, y )

    # Método que apaga obstáculos quando batem no jogador
    # Quando apagamos um obstáculo, criamos outro no topo da tela
    def collide( self ): 
        self.kill()
        obstaculos.add(Obstacle())

# Grupo para as sprites de obstáculo  
obstaculos = pygame.sprite.Group()

## Sprite dos powerups
# O parâmetro tipo determina o tipo de powerup, e layer determina em qual camada será desenhado
# Tipo 1 é o powerup que deixa o jogador mais veloz por alguns segundos
# Tipo 2 é o powerup que empurra a avalanche para trás, essencialmente curando parte do dano que o jogador tomou
class Powerup( pygame.sprite.Sprite ): 
    # Esse método inicializa a sprite e processa os parâmetros dados
    def __init__( self, tipo, layer=2 ):   
        pygame.sprite.Sprite.__init__( self ) 
        # Dependendo do tipo, utilizar a imagem correspondente
        self.type = tipo
        if tipo == 1:
            self.image = pup_img
        elif tipo == 2:
            self.image = pup_img2
        # Configurar o retângulo de colisão e posição da imagem
        self.rect  = self.image.get_rect()
        # Para garantir que os powerups vão cair de pontos aleatórios do topo da tela,
        # iniciamos a posição horizontal com valores aleatórios
        self.x = random.randint(0, SCREEN_WIDTH - 10)
        self.rect.center = ( self.x, -2000 )
        # Número da camada
        self._layer = layer

    ## Método update
    # Atualiza movimento
    def update( self ):
        # Avisar o código que não estamos referenciando esta variável apenas localmente
        global now
        # Obter um marcador do tempo atual (em ticks)
        # Fazemos isto para garantir que o powerup saberá quando parar
        now = pygame.time.get_ticks()
        # Obter posição do powerup a partir de seu retângulo
        x, y = self.rect.center
        # Movimentar o powerup para baixo
        y += 7
        # Apagar powerups que saem da tela
        if y > SCREEN_HEIGHT:
            self.kill()
        # Atualizar o retângulo com as posições que foram modificadas
        self.rect.center = ( x, y )

    # Método que apaga obstáculos quando batem no jogador
    def collide( self ):
        self.kill()
        
# Grupo para as sprites de powerup
powerups = pygame.sprite.Group()

## Sprite da avalanche
# O parâmetro layer determina em qual camada será desenhado
class Avalanche( pygame.sprite.Sprite ):
    # Esse método inicializa a sprite e processa os parâmetros dados
    def __init__( self,  layer=3 ):   
        pygame.sprite.Sprite.__init__( self )
        self.image = ava_img
        # Configurar o retângulo de colisão e posição da imagem
        self.rect  = self.image.get_rect()
        # A avalanche sempre deve começar em um lugar específico da tela
        # Nesta linha, posicionamos ela neste lugar atualizando a posição de seu retângulo
        self.rect.center = ( 300, 1200 )
        # Número da camada
        self._layer = layer

    ## Método update
    # Atualiza movimento
    def update( self ):
        # Obter posição da avalanche a partir de seu retângulo
        x, y = self.rect.center
        # Movimentar avalanche lentamente até sua posição alvo
        if y > avalanche_target:
            y -= 3
        if y < avalanche_target:
            y += 3
        # Atualizar o retângulo com as posições que foram modificadas
        self.rect.center = ( x, y )

    ## Método que ajuda na animação da sprite
    # Quando for chamado, alterna aleatoriamente a frame de animação da avalanche
    def anim( self ):
        self.image = random.choice([ava_img,ava_img2])
        
# Grupo para a sprite de avalanche
avalanche = pygame.sprite.GroupSingle()

## Função que reinicia todas as variáveis e sprites
# Como as sprites e variáveis do jogo são principalmente globais,
# seus valores normalmente se mantém os mesmos se sairmos do jogo.
# Como queremos que tudo comece novamente quando re-entramos no jogo,
# esta função reinicia todos valores e posições que afetam o jogo.
# Obs.: A função deve ser chamada antes e sempre que o jogo for iniciado
def reset():
    # Avisar o código que não estamos referenciando estas variáveis apenas localmente
    global hit, nivel, PLAYER_SPEED, BG_SPEED, score, obstaculos, powerups, avalanche_target

    # Reiniciar variáveis para valores iniciais
    nivel = 1
    score = 0
    avalanche_target = 1170
    PLAYER_SPEED = 5
    BG_SPEED = 7
    hit = False

    # Remover todas as sprites da tela
    # Podemos fazer isso pois as sprites são sempre desenhadas novamente quando o jogo inicia
    for obstaculo in obstaculos:
        obstaculo.kill()
    for powerup in powerups:
        powerup.kill()
    for p in player:
        p.kill()
    for a in avalanche:
        a.kill()

## Função principal do jogo
def game_loop():
    # Avisar o código que não estamos referenciando estas variáveis apenas localmente
    # Infelizmente temos que fazer isso com basicamente todas as variáveis do resto do código, e a linha fica longa
    global nivel, music, diff2unlock, diff3unlock, diff4unlock, pause, pvar, PLAYER_SPEED, score, INV_TIME, pupend, hitend, hit, pow, avanim, ended, player_img, player_hurt, player_power, player_normal, obstaculos, avalanche_y, avalanche_target, background_y, HIGHSCORE

    ## Configurar variáveis iniciais
    # Variável do loop do jogo: enquanto for True, o jogo roda
    running = True
    # Variáveis que marcam o ponto no tempo em que invulnerabilidade e poder do powerup acabam (em ticks)
    # Inicializamos estas variáveis com um valor ridiculamente alto para garantir que não iram ser ativadas ainda
    # Obs.: Em média, o jogador poderia esperar até esses valores acontecerem sozinhos, 
    # se ele manter o jogo aberto por mais de 5 dias, ou 105 anos, dependendo em quanto demora para iniciar o jogo.
    hitend = pygame.time.get_ticks()*n
    pupend = pygame.time.get_ticks()*n
    
    # Pontuação inicial que é dada para o jogador dependendo do nível
    score = 0
    if nivel == 2:
        score = 50
        INV_TIME = 1500
    if nivel == 3:
        score = 100
        INV_TIME = 1000
    if nivel == 4:
        score = 200
        INV_TIME = 500
    
    # Criar 4 obstáculos no início do jogo
    for i in range( 4 ):
        obstaculos.add( Obstacle())
    # Colocar na camada de fundo
    layers.add(obstaculos)

    # Criar jogador no início do jogo
    player.add(Player())
    # Colocar na camada do meio
    layers.add(player)

    # Criar avalanche no início do jogo
    avalanche.add(Avalanche())
    # Colocar na camada de cima
    layers.add(avalanche)

    # Tocar música de jogo
    if music:
        pygame.mixer.music.load("./resources/gamesong.mp3")
        pygame.mixer.music.play(-1)

    # Loop do jogo
    while running:
        if pause:
            screen.blit(pausebg,(0,0))
            # Criar botões
            return_button = Button(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT - 100, True, "Voltar")
            resume_button = Button(SCREEN_WIDTH // 2 + 10, 50, True, "Resumir")

            # Processar input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Pausar o jogo
                    if event.key == pygame.K_ESCAPE and pause and not pvar:
                        pause = False
                        pvar = False
                        hit = False
                        PLAYER_SPEED = 5
                        pupend = now*100
                        pow = False
                        hitend = now*100
                # Isso evita que o botão repita o input continuamente
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                            pvar = False
                # Processar cliques em cada botão
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Botão de voltar sai do jogo
                    if return_button.rect.collidepoint(event.pos):
                        pause = False
                        hit = False
                        hitend = now*100
                        PLAYER_SPEED = 5
                        pupend = now*100
                        pow = False
                        reset()
                        # Chama função que renderiza o menu
                        main_menu()
                    # Botão de resumir desfaz o pause
                    if resume_button.rect.collidepoint(event.pos):
                        pause = False
                        pvar = False
                        hit = False
                        PLAYER_SPEED = 5
                        pupend = now*100
                        pow = False
                        hitend = now*100
              
            # Desenhar botões
            return_button.draw(screen)
            resume_button.draw(screen)

            # Renderizar imagens na tela
            pygame.display.flip()

        if not pause:
            layers.add(obstaculos)
            # Definir tempo atual em uma variável
            now = pygame.time.get_ticks()
        # Processar jeitos de fechar o jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Pausar o jogo com ESC
                if event.key == pygame.K_ESCAPE and not pause:
                            pause = True
                            pvar = True

            # Checks com timer
            if not pause:
                # Este check cria powerups periodicamente
                if event.type == PSPAWN:
                    spawn = random.choice([True,False])
                    if spawn == True:
                        if avalanche_target != 850:
                            # Aleatoriamente criar de tipo 1 ou 2
                            ptype = random.choice([1,2])
                        else:
                            ptype = 1
                        powerups.add(Powerup(tipo=ptype))
                        layers.add(powerups)
                # Este check muda animação da avalanche periodicamente
                if event.type == AVANIM:
                    for a in avalanche:
                        a.anim()

        # Cria marcas na neve embaixo do jogador
        if not ended:
            if not pause:
                for p in player:
                    tracks.add(Track(p.rect.center))
                    layers.add(tracks)

        # Aumentar dificuldade com pontuação
        if not pause:
            if nivel < 4:
                if score == 50:
                    INV_TIME = 1500
                    nivel = 2
                if score == 100:
                    INV_TIME = 1000
                    nivel = 3
                if score == 200:
                    INV_TIME = 500
                    nivel = 4

        # Processar colisão com obstáculos
        if not pause:
            for obstaculo in obstaculos:
                for p in player:
                    for a in avalanche:
                        if pygame.sprite.collide_rect(obstaculo,p) and not hit:
                            # Tocar som
                            hit_sound.play()
                            # Jogador fica temporariamente invulnerável logo após a colisão
                            obstaculo.collide()
                            hit = True
                            # Levantar avalanche com a colisão
                            x, y = a.rect.center
                            avalanche_target = y - 30
                            # Timer para acabar a invulnerabilidade
                            hitend = now + INV_TIME
            
            # Remover invulnerabilidade depois do fim do timer
            if now >= hitend:
                hit = False
                hitend = now*100

        # Processar colisão com powerups
        if not pause:
            for powerup in powerups:
                for p in player:
                    # Se o powerup for de tipo 1, aumentar velocidade do jogador
                    if pygame.sprite.collide_rect(powerup,p) and powerup.type == 1:
                        # Tocar som
                        pup_sound.play()
                        powerup.collide()
                        PLAYER_SPEED += 2
                        # Variável para mudar a imagem do jogador
                        pow = True
                        # Timer para fim do efeito do powerup
                        pupend = now + 5000
                    # Se o powerup for de tipo 2, abaixar a avalanche
                    if pygame.sprite.collide_rect(powerup,p) and powerup.type == 2:
                        # Tocar som
                        pup_sound.play()
                        powerup.collide()
                        x, y = a.rect.center
                        if avalanche_target < 1170:
                            avalanche_target = y + 30
            # Remover efeito do powerup depois do fim do timer
            if now >= pupend:
                PLAYER_SPEED = 5
                pupend = now*100
                pow = False

        # Estas linhas garantem que o método update das sprites vai ser ativado em cada loop
        if not pause:
            player.update()
            obstaculos.update()
            powerups.update()
            avalanche.update()
            tracks.update()

        # Processar colisão com a avalanche
        if not pause:
            for a in avalanche:
                for p in player:
                    x, y = a.rect.center
                    px, py = p.rect.center
                    if y < py + 450:
                            # Atualizar o highscore se a pontuação for maior
                            if score > HIGHSCORE:
                                file = open("./resources/highscore.txt", "w")
                                file.write(str(score))
                                file.close()
                                HIGHSCORE = score
                            # Desbloquear dificuldades com pontuação
                            if score >= 50 and not diff2unlock:
                                diff2unlock = True
                            if score >= 100 and not diff3unlock:
                                diff3unlock = True
                            if score >= 200 and not diff4unlock:
                                diff4unlock = True
                            # Mudar para tela de fim de jogo
                            death_screen()
                            ended = True

        # Mover imagem de fundo constantemente
        if not ended:
            if not pause:
                background_y += BG_SPEED
                if background_y >= SCREEN_HEIGHT:
                    background_y = 0

            # Desenhar imagem de fundo
            screen.blit(background, (0, background_y))
            screen.blit(background, (0, background_y - SCREEN_HEIGHT))

            # Desenhar sprites
            layers.draw(screen)

            # Mostra pontuação
            font = pygame.font.Font("./resources/upheavtt.ttf", 36)
            text = font.render(f"Score: {score}", True, BLACK)
            text2 = font.render(f"Nivel: {nivel}", True, BLACK)

            screen.blit(text, (10, 10))
            screen.blit(text2, (10, 35))

            # Atualizar tela
            if not pause:
                pygame.display.flip()

        # Frames por segundo do jogo
        clock.tick(60)

# Função do menu principal
def main_menu():
    # Avisar o código que não estamos referenciando variáveis locais
    global nivel, nivel_choice, hscore, music

    # Tocar música de menu
    if music:
        pygame.mixer.music.load("./resources/menusong.mp3")
        pygame.mixer.music.play(-1)

    # Ler highscore do arquivo local
    file = open("./resources/highscore.txt", "r")
    hscore = int(file.read())

    # Criar botões
    start_button = Button(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - 40, True, "Start")
    options_button = Button(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 80, True, "Options")
    unlocks_button = Button(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 300, True, "Recompensas", pygame.font.Font("./resources/upheavtt.ttf", 22))

    # Loop do menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Processar cliques em cada botão
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    reset()
                    nivel = nivel_choice
                    game_loop()
                if options_button.rect.collidepoint(event.pos):
                    options_menu()
                if unlocks_button.rect.collidepoint(event.pos):
                    unlocks_menu()

        # Desenhar tela, texto e botões
        screen.fill(WHITE)
        font = pygame.font.Font("./resources/upheavtt.ttf", 70)
        font2 = pygame.font.Font("./resources/upheavtt.ttf", 36)
        text = font.render(f"AVALANCHE", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2 - 200))
        text = font2.render(f"High Score: {hscore}", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 200))
        start_button.draw(screen)
        options_button.draw(screen)
        unlocks_button.draw(screen)
        pygame.display.flip()

# Função do menu de opções
def options_menu():
    # Avisar o código que não estamos referenciando variáveis locais
    global nivel, music, nivel_choice, hscore

    # Variável de loop para o menu
    options = True
    # Criar botões
    return_button = Button(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT - 100, True, "Voltar")
    diff_less = Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT //2 - 100, True, "-")
    diff_more = Button(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT //2 - 100, True, "+")
    reset_button = Button(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT - 300, True, "Reset")
    if music == True:
        mute_button = Button(SCREEN_WIDTH - 70, SCREEN_HEIGHT - 100, True, type=2)
    elif music == False:
        mute_button = Button(SCREEN_WIDTH - 70, SCREEN_HEIGHT - 100, False, type=2)

    # Loop do menu
    while options:
        nivel = nivel_choice
        # Desativar botões que não devem ser clicados
        if nivel < 2:
            diff_less = Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT //2 - 100, False, "-")
            if not diff2unlock:
                diff_more = Button(SCREEN_WIDTH // 2+ 100, SCREEN_HEIGHT //2 - 100, False, "+")
            elif diff2unlock:
                diff_more = Button(SCREEN_WIDTH // 2+ 100, SCREEN_HEIGHT //2 - 100, True, "+")
        if nivel >= 2:
            diff_less = Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT //2 - 100, True, "-")
        if nivel == 2 and not diff3unlock:
            diff_more = Button(SCREEN_WIDTH // 2+ 100, SCREEN_HEIGHT //2 - 100, False, "+")
        elif nivel == 2 and diff3unlock:
            diff_more = Button(SCREEN_WIDTH // 2+ 100, SCREEN_HEIGHT //2 - 100, True, "+")
        if nivel == 3 and not diff4unlock:
            diff_more = Button(SCREEN_WIDTH // 2+ 100, SCREEN_HEIGHT //2 - 100, False, "+")
        elif nivel == 3 and diff4unlock:
            diff_more = Button(SCREEN_WIDTH // 2+ 100, SCREEN_HEIGHT //2 - 100, True, "+")
        if nivel > 3:
            diff_more = Button(SCREEN_WIDTH // 2+ 100, SCREEN_HEIGHT //2 - 100, False, "+")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Processar cliques em cada botão
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.rect.collidepoint(event.pos):
                    options = False
                if diff_less.rect.collidepoint(event.pos) and diff_less.active:
                    if (nivel >= 2):
                        nivel -= 1
                        nivel_choice = nivel
                if diff_more.rect.collidepoint(event.pos) and diff_more.active:
                    if (nivel <= 3):
                        nivel += 1
                        nivel_choice = nivel
                if reset_button.rect.collidepoint(event.pos):
                    file = open("./resources/highscore.txt", "w")
                    file.write(str(0))
                    file.close()
                    hscore = 0
                if mute_button.rect.collidepoint(event.pos):
                    if mute_button.active:
                        music = False
                        pygame.mixer.music.stop()
                        mute_button = Button(SCREEN_WIDTH - 70, SCREEN_HEIGHT - 100, False, type=2)
                    else:
                        music = True
                        pygame.mixer.music.play()
                        mute_button = Button(SCREEN_WIDTH - 70, SCREEN_HEIGHT - 100, True, type=2)
                        
        # Desenhar tela, texto e botões
        font = pygame.font.Font("./resources/upheavtt.ttf", 40)
        diff = font.render(f"Dificuldade: {nivel}", True, BLACK)
        text = font.render(f"Reset High Score", True, BLACK)
        screen.fill(WHITE)
        screen.blit(diff, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT //2 - 200))
        screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 400))
        return_button.draw(screen)
        reset_button.draw(screen)
        diff_less.draw(screen)
        diff_more.draw(screen)
        mute_button.draw(screen)
        pygame.display.flip()

# Função do menu de opções
def unlocks_menu():
    # Avisar o código que não estamos referenciando variáveis locais
    global nivel, music, chosen, nivel_choice, hscore, player2unlocked, player3unlocked, player4unlocked

    # Variável de loop para o menu
    unlock = True
    now = pygame.time.get_ticks()
    resett = now*100

    # Criar botões
    player2unlock = Button(SCREEN_WIDTH // 2 + 50, 200, True, type=3)
    if chosen == 2:
        player2unlock = Button(SCREEN_WIDTH // 2 + 50, 200, False, type=3)
    player3unlock = Button(SCREEN_WIDTH // 2 + 50, 400, True, type=4)
    if chosen == 3:
        player3unlock = Button(SCREEN_WIDTH // 2 + 50, 400, False, type=4)
    player4unlock = Button(SCREEN_WIDTH // 2 + 50, 600, True, type=5)
    if chosen == 4:
        player4unlock = Button(SCREEN_WIDTH // 2 + 50, 600, False, type=5)
    return_button = Button(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT - 100, True, "Voltar")
    
    # Loop do menu
    while unlock:
        now = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Processar cliques em cada botão
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player2unlock.rect.collidepoint(event.pos):
                    if hscore >= 50 and not player2unlocked:
                        player2unlock = Button(SCREEN_WIDTH // 2 + 50, 200, False, type=3)
                        unlock_sound.play()
                        player2unlocked = True
                        resett = now + 1000
                    elif player2unlocked and chosen != 2:
                        chosen = 2
                        player2unlock = Button(SCREEN_WIDTH // 2 + 50, 200, False, type=3)
                        player4unlock = Button(SCREEN_WIDTH // 2 + 50, 600, True, type=5)
                        player3unlock = Button(SCREEN_WIDTH // 2 + 50, 400, True, type=4)
                        select_sound.play()
                    else:
                        fail_sound.play()
                if player3unlock.rect.collidepoint(event.pos):
                    if hscore >= 100 and not player3unlocked:
                        player3unlocked = True
                        player3unlock = Button(SCREEN_WIDTH // 2 + 50, 400, False, type=4)
                        unlock_sound.play()
                        resett = now + 1000
                    elif player3unlocked and chosen != 3:
                        chosen = 3
                        player3unlock = Button(SCREEN_WIDTH // 2 + 50, 400, False, type=4)
                        player2unlock = Button(SCREEN_WIDTH // 2 + 50, 200, True, type=3)
                        player4unlock = Button(SCREEN_WIDTH // 2 + 50, 600, True, type=5)
                        select_sound.play()
                    else:
                        fail_sound.play()
                if player4unlock.rect.collidepoint(event.pos):
                    if hscore >= 200 and not player4unlocked:
                        player4unlocked = True
                        player4unlock = Button(SCREEN_WIDTH // 2 + 50, 600, False, type=5)
                        unlock_sound.play()
                        resett = now + 1000
                    elif player4unlocked and chosen != 4:
                        chosen = 4
                        player4unlock = Button(SCREEN_WIDTH // 2 + 50, 600, False, type=5)
                        player3unlock = Button(SCREEN_WIDTH // 2 + 50, 400, True, type=4)
                        player2unlock = Button(SCREEN_WIDTH // 2 + 50, 200, True, type=3)
                        select_sound.play()
                    else:
                        fail_sound.play()
                if return_button.rect.collidepoint(event.pos):
                    unlock = False
        if now >= resett:
            if chosen == 1:
                player4unlock = Button(SCREEN_WIDTH // 2 + 50, 600, True, type=5)
                player3unlock = Button(SCREEN_WIDTH // 2 + 50, 400, True, type=4)
                player2unlock = Button(SCREEN_WIDTH // 2 + 50, 200, True, type=3)
            if chosen == 2:
                player4unlock = Button(SCREEN_WIDTH // 2 + 50, 600, True, type=5)
                player3unlock = Button(SCREEN_WIDTH // 2 + 50, 400, True, type=4)
            if chosen == 3:
                player4unlock = Button(SCREEN_WIDTH // 2 + 50, 600, True, type=5)
                player2unlock = Button(SCREEN_WIDTH // 2 + 50, 200, True, type=3)
            if chosen == 4:
                player3unlock = Button(SCREEN_WIDTH // 2 + 50, 400, True, type=4)
                player2unlock = Button(SCREEN_WIDTH // 2 + 50, 200, True, type=3)
            resett = now*100
                        
        # Desenhar tela, texto e botões
        font = pygame.font.Font("./resources/upheavtt.ttf", 40)
        title = font.render(f"Recompensas", True, BLACK)
        if player2unlocked:
            p1 = font.render(f"50", True, BLACK)
        if not player2unlocked:
            p1 = font.render(f"50", True, BLUE)
        if player3unlocked:
            p2 = font.render(f"100", True, BLACK)
        if not player3unlocked:
            p2 = font.render(f"100", True, BLUE)
        if player4unlocked:
            p3= font.render(f"200", True, BLACK)
        if not player4unlocked:
            p3 = font.render(f"200", True, BLUE)
        screen.fill(WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - 150, 100))
        screen.blit(p1, (SCREEN_WIDTH // 2 + 50, 200))
        screen.blit(p2, (SCREEN_WIDTH // 2 + 50, 400))
        screen.blit(p3, (SCREEN_WIDTH // 2 + 50, 600))
        player2unlock.draw(screen)
        player3unlock.draw(screen)
        player4unlock.draw(screen)
        return_button.draw(screen)
        pygame.display.flip()

# Função da tela final
def death_screen():
    # Avisar o código que não estamos referenciando variáveis locais
    global score

    # Parar música e sons e tocar som de gameover
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    gameover_sound.play()

    # Variável de loop para o menu
    dscreen = True
    # Criar botões
    return_button = Button(SCREEN_WIDTH // 2 , SCREEN_HEIGHT - 100, True, "Voltar")

    # Loop do menu
    while dscreen:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Processar cliques em cada botão
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if return_button.rect.collidepoint(event.pos):
                        dscreen = False
                        main_menu()

        # Desenhar tela, texto e botões
        screen.fill(WHITE)
        font = pygame.font.Font("./resources/upheavtt.ttf", 40)
        font2 = pygame.font.Font("./resources/upheavtt.ttf", 54)
        text = font2.render(f"Game Over", True, RED)
        text2 = font.render(f"Sua pontuação: {score}", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 200))
        screen.blit(text2, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))
        return_button.draw(screen)
        pygame.display.flip()

# Inicializar o jogo
if __name__ == "__main__":
    main_menu()
