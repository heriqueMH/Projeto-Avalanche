import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()
pygame.mixer.init()

# Janela do jogo
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Variáveis globais de tela
options = False
ended = False

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 109, 255)

## Setup inicial

# Vars iniciais
PLAYER_SPEED = 5
BG_SPEED = 7

# Tempo que o jogador fica invulnerável depois que toma dano
INV_TIME = 2000

# Configura highscore a partir do arquivo txt
file = open("./resources/highscore.txt", "r")
HIGHSCORE = int(file.read())
file.close()

# Variáveis globais
nivel = 1
nivel_choice = 1
score = 0
hit = False
pow = False
avalanche_target = 1170

# Timers
PSPAWN = pygame.USEREVENT+1
PSTOP = pygame.USEREVENT + 2
AVANIM = pygame.USEREVENT + 3
pygame.time.set_timer(PSPAWN, 6500)
pygame.time.set_timer(PSTOP, 5000)
pygame.time.set_timer(AVANIM, 500)

# FPS
clock = pygame.time.Clock()

# Carregando imagem de fundo
background = pygame.image.load('./resources/bg.png')
background_y = 0

# Carregando imagens de botão
botao = pygame.image.load('./resources/button.png').convert_alpha()
botao2 = pygame.image.load('./resources/button2.png').convert_alpha()
botao3 = pygame.image.load('./resources/button3.png').convert_alpha()

# Sprite de botão
class Button( pygame.sprite.Sprite ):
    def __init__(self, text, x, y,active):
        pygame.sprite.Sprite.__init__( self ) 
        self.image = botao
        self.rect = self.image.get_rect()
        self.rect.center = ( x, y )
        self.text = text
        self.active = active

    # Desenhar o botão
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        x,y = self.rect.center

        # Mudar cor se o mouse está em cima
        if self.active:
            if self.rect.collidepoint(mouse_pos):
                self.image = botao2
                screen.blit(self.image, (x-80, y-15))
            else:
                self.image = botao
                screen.blit(self.image, (x-80, y-15))
        else:
            self.image = botao3
            screen.blit(self.image, (x-80, y-15))

        # Desenhar o texto por cima, a partir da variável text
        font = pygame.font.Font("./resources/upheavtt.ttf", 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x+2,y+15))
        screen.blit(text_surface, text_rect)

# Carregando imagem dos obstaculos
load_img = pygame.image.load('./resources/tile_0047.png').convert()
tronco_img = pygame.transform.scale(load_img, (50,50))

# Carregando imagem dos powerups
load_img = pygame.image.load('./resources/tile_0021.png').convert()
pup_img = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/tile_0021b.png').convert()
pup_img2 = pygame.transform.scale(load_img, (50,50))

# Carregando imagens da avalanche
load_img = pygame.image.load('./resources/tile_0004.png').convert_alpha()
ava_img = pygame.transform.scale(load_img, (600,900))
load_img = pygame.image.load('./resources/tile_0004b.png').convert_alpha()
ava_img2 = pygame.transform.scale(load_img, (600,900))

# Carregando imagem das marcas
load_img = pygame.image.load('./resources/tile_0058.png').convert()
tra_img = pygame.transform.scale(load_img, (50,50))

# Carregando imagens do personagem (esquiador)
load_img = pygame.image.load('./resources/tile_0070.png').convert()
player_normal = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/tile_0071.png').convert()
player_hurt = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/tile_0070p.png').convert()
player_power = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/tile_0070left.png').convert_alpha()
player_left = pygame.transform.scale(load_img, (50,50))
load_img = pygame.image.load('./resources/tile_0070right.png').convert_alpha()
player_right = pygame.transform.scale(load_img, (50,50))

player_img = player_normal
player_rect = player_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 220))

# Configurando layers
# Esta variável armazena sprites em camadas
layers = pygame.sprite.LayeredUpdates()

# Carregar sons
hit_sound = pygame.mixer.Sound("./resources/hit.mp3")
pup_sound = pygame.mixer.Sound("./resources/powerup.mp3")
gameover_sound = pygame.mixer.Sound("./resources/gameover.mp3")
diffchange_sound = pygame.mixer.Sound("./resources/diffchange.mp3")

# Sprite do jogador
class Player( pygame.sprite.Sprite ):
    def __init__( self, layer=1 ):   
        pygame.sprite.Sprite.__init__( self ) 
        self.image = player_normal
        self.rect  = self.image.get_rect()     
        self.rect.center = ( SCREEN_WIDTH // 2, SCREEN_HEIGHT - 220 )
        self._layer = layer

    # Método update
    # Atualiza imagens e movimento
    def update( self ):
        x, y = self.rect.center
        keys = pygame.key.get_pressed()
        left = False
        right = False
        
        # Movimentação do jogador
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

        # Mudar imagem de acordo com o estado do jogador
        if hit:
            self.image = player_hurt
        elif pow:
            self.image = player_power
        elif left:
            self.image = player_left
        elif right:
            self.image = player_right
        else:
            self.image = player_normal

# Grupo para a sprite do jogador
player = pygame.sprite.GroupSingle()

# Sprite das marcas na neve
class Track( pygame.sprite.Sprite ):
    def __init__( self,  player, layer=0 ):   
        pygame.sprite.Sprite.__init__( self ) 
        self.image = tra_img
        self.rect  = self.image.get_rect()     
        self.rect.center = ( player )
        self._layer = layer

    # Método update
    def update( self ):
        x, y = self.rect.center

        # Movimentar as marcas
        y += 7

        # Apagar marcas que saem da tela
        if y > SCREEN_HEIGHT:
            self.kill()
        self.rect.center = ( x, y )

# Grupo para as sprites de marcas     
tracks = pygame.sprite.Group()

# Sprite dos obstáculos
class Obstacle( pygame.sprite.Sprite ): 
    def __init__( self, layer=2 ):   
        pygame.sprite.Sprite.__init__( self ) 
        self.image = tronco_img
        self.rect  = self.image.get_rect()     
        self.y = random.randint(-1000,-100)
        self.x = random.randint(0, SCREEN_WIDTH - 10)
        self.rect.center = ( self.x, self.y )
        self._layer = layer

    # Método update
    # Atualiza velocidade, movimento e estado
    def update( self ):
        global score, BG_SPEED

        # Deixar obstáculos mais rápidos de acordo com dificuldade
        if nivel == 2:
            if BG_SPEED < 8:   
                BG_SPEED += 2
        if nivel == 3:
            if BG_SPEED < 11:
                BG_SPEED += 3
        if nivel == 4:
            if BG_SPEED < 15:
               BG_SPEED += 4

        x, y = self.rect.center

        # Movimentar obstáculos
        y += BG_SPEED

        # Apagar obstáculos que saem da tela
        if y > SCREEN_HEIGHT:
            now = pygame.time.get_ticks()
            self.kill()
            # Quando apagamos um obstáculo, criamos outro no topo da tela
            obstaculos.add(Obstacle())
            # Aumentar pontuação quando um obstáculo sai da tela
            score += 1
        self.rect.center = ( x, y )

    # Método que apaga obstáculos quando batem no jogador
    # Quando apagamos um obstáculo, criamos outro no topo da tela
    def collide( self ): 
        self.kill()
        obstaculos.add(Obstacle())

# Grupo para as sprites de obstáculo  
obstaculos = pygame.sprite.Group()

# Sprite dos powerups
class Powerup( pygame.sprite.Sprite ): 
    def __init__( self, tipo, layer=2 ):   
        pygame.sprite.Sprite.__init__( self ) 
        self.type = tipo
        if tipo == 1:
            self.image = pup_img
        elif tipo == 2:
            self.image = pup_img2
        self.rect  = self.image.get_rect()
        self.x = random.randint(0, SCREEN_WIDTH - 10)
        self.rect.center = ( self.x, -2000 )
        self._layer = layer

    # Método update
    # Atualiza movimento
    def update( self ):
        global now
        now = pygame.time.get_ticks()
        x, y = self.rect.center

        # Movimenta o powerup
        y += 7

        # Apaga powerups que saem da tela
        if y > SCREEN_HEIGHT:
            self.kill()
        self.rect.center = ( x, y )

    # Método que apaga obstáculos quando batem no jogador
    def collide( self ):
        self.kill()
        
# Grupo para as sprites de powerup 
powerups = pygame.sprite.Group()

# Sprite da avalanche
class Avalanche( pygame.sprite.Sprite ):
    def __init__( self,  layer=3 ):   
        pygame.sprite.Sprite.__init__( self )
        self.image = ava_img
        self.rect  = self.image.get_rect()     
        self.rect.center = ( 300, 1200 )
        self._layer = layer

    # Método update
    # Atualiza movimento
    def update( self ):
        global avalanche_target
        x, y = self.rect.center
        # Movimentar avalanche lentamente
        if y > avalanche_target:
            y -= 3
        if y < avalanche_target:
            y += 3
        self.rect.center = ( x, y )

    # Método de animação da sprite
    def anim( self ):
        self.image = random.choice([ava_img,ava_img2])
        
# Grupo para a sprite de avalanche
avalanche = pygame.sprite.GroupSingle()
        
# Função que reinicia todas as variáveis e sprites
def reset():
    # Avisar o código que não estamos referenciando variáveis locais
    global nivel, PLAYER_SPEED, score, obstaculos, powerups, avalanche_target

    # Reiniciar variáveis para valores iniciais
    nivel = 1
    score = 0
    avalanche_target = 1170
    PLAYER_SPEED = 5

    # Remover todas as sprites da tela
    for obstaculo in obstaculos:
        obstaculo.kill()
    for powerup in powerups:
        powerup.kill()
    for p in player:
        p.kill()
    for a in avalanche:
        a.kill()

# Função principal do jogo
def game_loop():
    # Avisar o código que não estamos referenciando variáveis locais
    global nivel, PLAYER_SPEED, score, INV_TIME, pupend, hitend, hit, pow, avanim, ended, player_img, player_hurt, player_power, player_normal, obstaculos, avalanche_y, avalanche_target, background_y, HIGHSCORE

    # Configurar variáveis iniciais
    running = True
    hitend = pygame.time.get_ticks()*100
    pupend = pygame.time.get_ticks()*100
    
    # Pontuação inicial dependendo do nível
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
    pygame.mixer.music.load("./resources/gamesong.mp3")
    pygame.mixer.music.play(-1)

    # Loop do jogo
    while running:
        layers.add(obstaculos)
        # Definir tempo atual em uma variável
        now = pygame.time.get_ticks()
        # Processar jeitos de fechar o jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Tocar música de menu
                pygame.mixer.music.load("./resources/menusong.mp3")
                pygame.mixer.music.play(-1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                            running = False
                            # Tocar música de menu
                            pygame.mixer.music.load("./resources/menusong.mp3")
                            pygame.mixer.music.play(-1)

            # Checks com timer
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
            for p in player:
                tracks.add(Track(p.rect.center))
                layers.add(tracks)

        # Aumentar dificuldade com pontuação
        if nivel < 4:
            if score == 50:
                diffchange_sound.play()
                INV_TIME = 1500
                nivel = 2
            if score == 100:
                diffchange_sound.play()
                INV_TIME = 1000
                nivel = 3
            if score == 200:
                diffchange_sound.play()
                INV_TIME = 500
                nivel = 4

        # Processar colisão com obstáculos
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
        player.update()
        obstaculos.update()
        powerups.update()
        avalanche.update()
        tracks.update()

        # Processar colisão com a avalanche
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
                        # Mudar para tela de fim de jogo
                        death_screen()
                        ended = True

        # Mover imagem de fundo constantemente
        if not ended:
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
            #text3 = font.render(f"{avalanche_target}", True, BLACK)

            screen.blit(text, (10, 10))
            screen.blit(text2, (10, 35))
            #screen.blit(text3, (10,50) )

            # Atualizar tela
            pygame.display.flip()

        # Frames por segundo do jogo
        clock.tick(60)

# Função do menu principal
def main_menu():
    # Avisar o código que não estamos referenciando variáveis locais
    global nivel, nivel_choice, hscore, menusong

    # Tocar música de menu
    pygame.mixer.music.load("./resources/menusong.mp3")
    pygame.mixer.music.play(-1)

    # Ler highscore do arquivo local
    file = open("./resources/highscore.txt", "r")
    hscore = int(file.read())

    # Criar botões
    start_button = Button("Start", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, True)
    options_button = Button("Options", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80, True)

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

        # Desenhar tela, texto e botões
        screen.fill(WHITE)
        font = pygame.font.Font("./resources/upheavtt.ttf", 128)
        font2 = pygame.font.Font("./resources/upheavtt.ttf", 36)
        text = font.render(f"SKI", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 200))
        text = font2.render(f"High Score: {hscore}", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 200))
        start_button.draw(screen)
        options_button.draw(screen)
        pygame.display.flip()

# Função do menu de opções
def options_menu():
    # Avisar o código que não estamos referenciando variáveis locais
    global nivel, nivel_choice, hscore

    # Variável de loop para o menu
    options = True
    # Criar botões
    return_button = Button("Voltar", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, True)
    diff_less = Button("-", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT //2 - 100, True)
    diff_more = Button("+", SCREEN_WIDTH // 2 + 70, SCREEN_HEIGHT //2 - 100, True)
    reset_button = Button("Reset", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 300, True)

    # Loop do menu
    while options:
        # Desativar botões que não devem ser clicados
        if nivel < 2:
            diff_less = Button("-", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT //2 - 100, False)
        if nivel >= 2:
            diff_less = Button("-", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT //2 - 100, True)
        if nivel > 3:
            diff_more = Button("+", SCREEN_WIDTH // 2+ 70, SCREEN_HEIGHT //2 - 100, False)
        if nivel <= 3:
            diff_more = Button("+", SCREEN_WIDTH // 2+ 70, SCREEN_HEIGHT //2 - 100, True)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Processar cliques em cada botão
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.rect.collidepoint(event.pos):
                    options = False
                if diff_less.rect.collidepoint(event.pos):
                    if (nivel >= 2):
                        nivel -= 1
                        nivel_choice = nivel
                if diff_more.rect.collidepoint(event.pos):
                    if (nivel <= 3):
                        nivel += 1
                        nivel_choice = nivel
                if reset_button.rect.collidepoint(event.pos):
                    file = open("./resources/highscore.txt", "w")
                    file.write(str(0))
                    file.close()
                    hscore = 0
        
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
    return_button = Button("Voltar", SCREEN_WIDTH // 2 , SCREEN_HEIGHT - 100, True)

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

