import random
from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH
 
class Cloud:
    def __init__(self):
        self.cloud = CLOUD
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = self.cloud
        self.width = self.image.get_width()
 
    def update(self, game_speed):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(1800, 2500)
            self.y = random.randint(50, 250)
            
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))