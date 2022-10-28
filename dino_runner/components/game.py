from operator import truediv
from turtle import screensize
import pygame

from dino_runner.utils.constants import BG, TUTORIAL, BIRD_DECO, CACTUS_DECO, DINOD, GAMEOVER, ICON, RESTART_ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.dinossaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.obstacles.cloud import Cloud
from dino_runner.utils.text_utils import draw_message_component
from dino_runner.components.powerups.power_up_manager import PowerUpManager

class Game: #definição das classes e elementos do player\background

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.score = 0
        self.death_count = 0
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.cloud = Cloud()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
    
    def execute(self): # Essa parte cuida da execução do jogo, se ele estiver rodando(self.running = true) ele não vai puxar o menu, caso não esteja rodando(self.running = False) ele puxa a função do menu
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
                
        pygame.display.quit()
        pygame.quit()
    
    def run(self):#quando o jogo iniciar, esse def serve pra resetar tudo
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.score = 0
        self.game_speed = 10
        while self.playing:#enquanto o jogo tiver rodando, ele vai ficar nesse ciclo de event => update => draw
            self.events()
            self.update()
            self.draw()

    def events(self):#isso serve pra quando a gente apertar o botão vermelho que nunca responde, ele fechar o processo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.update_speed()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_speed(self):
        self.score += 1
        if self.score % 200 == 0:
            self.game_speed += 2

    def draw(self):#chamando as funções e renderizando-as
            self.clock.tick(FPS)
            self.screen.fill((255, 255, 255))
            self.draw_background()
            self.player.draw(self.screen)
            self.obstacle_manager.draw(self.screen)
            self.draw_score()
            self.draw_power_up_time()
            self.power_up_manager.draw(self.screen)
            self.cloud.update(self.game_speed)
            self.cloud.draw(self.screen)
            self.show_fps() 
            pygame.display.update()
            pygame.display.flip()
        
    def draw_background(self):#renderizando o background
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= - image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):#função pra mostrar o score no canto superior direito da tela
       draw_message_component(
        f"Score: {self.score}",
        self.screen,
        pos_x_center=1000,
        pos_y_center=50
        )
    
    def show_fps(self):#função pra mostrar o fps no canto da tela kkkkkk (pc master race)
        draw_message_component(
        f'FPS: {self.clock.get_fps():.0f}',
        self.screen,
        pos_x_center=1000,
        pos_y_center=30
        )

    def draw_power_up_time(self):#contador do tempo do power up
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message_component(
                    f'{self.player.type.capitalize()} enabled for {time_to_show:.0f} seconds',
                    self.screen,
                    font_size = 18,
                    pos_x_center=500,
                    pos_y_center=40
                    )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
    
    def handle_events_on_menu(self):#Parte que vai cuidar dos inputs do jogador, se ele pressionou o botão vermelho que nunca responde, ou alguma tecla pra reiniciar o jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.run()

    def show_menu(self): # Parte do código que vai cuidar do menu do jogo, sendo ele o menu de inicio ou menu de 'restart'
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            draw_message_component("Welcome to the game!", self.screen, pos_y_center= half_screen_height -100)
            draw_message_component("Press any key to start", self.screen, pos_y_center= half_screen_height -40) #esse draw message component() que cuida do que exibir na tela, sendo str ou uma varíavel pré-estabelecida
            self.screen.blit(ICON, (half_screen_width -40, half_screen_height + 10))
            self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg)) 
            self.screen.blit(BIRD_DECO, (half_screen_width -350, half_screen_height - 160))
            self.screen.blit(CACTUS_DECO, (half_screen_width +300, half_screen_height - 5 ))

        else:
            draw_message_component("Press any key if you wish to restart", self.screen, pos_y_center= half_screen_height + 140)
            draw_message_component(
                f'Your score: {self.score}',
                self.screen,
                pos_y_center= half_screen_height - 150
            )
            draw_message_component(
                f'Death Count: {self.death_count}',
                self.screen,
                pos_y_center= half_screen_height - 100
            )
            self.screen.blit(GAMEOVER, (half_screen_width -180, half_screen_height - 220))
            self.screen.blit(RESTART_ICON, (half_screen_width -40, half_screen_height + 170))
            self.screen.blit(DINOD, (half_screen_width - 40, half_screen_height))
            self.screen.blit(BG, (half_screen_width - 550, half_screen_height + 80))
            self.screen.blit(CACTUS_DECO, (half_screen_width + 60, half_screen_height - 5 ))
        
        pygame.display.flip()
        self.handle_events_on_menu()