from operator import truediv
import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.text_utils import draw_message_component
from dino_runner.components.powerups.power_up_manager import PowerUpManager

class Game:

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

        self.game_speed = 20

        self.x_pos_bg = 0

        self.y_pos_bg = 380

        self.player = Dinosaur()

        self.obstacle_manager = ObstacleManager()

        self.power_up_manager = PowerUpManager()
    
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
                
        pygame.display.quit()
        pygame.quit()
    
    def run(self):
        self.playing = True
        self.obstacle_manager.reset_obstacle()
        self.power_up_manager.reset_power_up()
        self.score.reset_score()
        self.game_speed.reset_game_speed()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):               
        for event in pygame.event.get():
            if event.type == pygame.quit():
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.score.update()
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed +=5
    
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) 
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()
    
