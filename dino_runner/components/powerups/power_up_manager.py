import pygame
import random
from dino_runner.components.powerups.heart import Heart
from dino_runner.components.powerups.shield import Shield
from dino_runner.components.powerups.hammer import Hammer

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0

    def generate_power_up(self,score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(200,300)
            self.power_ups.append(Shield())
            self.power_ups.append(Hammer())
            self.power_ups.append(Heart())

    def update(self, score, game_speed, player):
        power_up_type = [
            Hammer(),
            Shield(),
            Heart()
        ]
        if len(self.power_ups) == 0:
            self.power_ups.append(power_up_type[random.randint(0,2)])
            self.generate_power_up(score)
        for power_up in self.power_ups:#detecção da hitbox do dino, se tiver power up não 'ocorre' colisão e objeto é removido
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                player.shield = True
                player.has_power_up = True
                player.type = power_up.type
                player.power_up_time = power_up.start_time + (power_up.duration * 200)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200,300)
        