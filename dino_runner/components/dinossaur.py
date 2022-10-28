import pygame

from pygame.sprite import Sprite



from dino_runner.utils.constants import BIRD, HAMMER, LARGE_CACTUS, RUNNING, JUMPING, DUCKING, DEFAULT_TYPE, SHIELD, SHIELD_TYPE, DUCKING_SHIELD, JUMPING_SHIELD, RUNNING_SHIELD, SMALL_CACTUS
DUCK_IMG = { DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}

JUMP_IMG = { DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD}

RUN_IMG = { DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}

X_POS = 80

Y_POS = 310

Y_POS_DUCK = 340

JUMP_VEL = 8.5

class Dinosaur(Sprite): #Definição dos elementos do dinossauro e dos diferentes tipos de mecânica. Como: power ups, pular e agachar

    def __init__(self):

        self.type = DEFAULT_TYPE

        self.image = RUN_IMG[self.type][0]

        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = X_POS

        self.dino_rect.y = Y_POS

        self.step_index = 0

        self.dino_run = True

        self.dino_jump = False

        self.dino_duck = False

        self.jump_vel = JUMP_VEL

        self.setup_state()

    def setup_state(self): #definição do estado inicial do dinossauro, quando o jogo acaba de começar
        self.has_power_up = False
        self.shield = False
        self.hammer = False
        self.show_text = False
        self.shield_time_up = 0
    
    def update(self, user_input): #definição das 3 mecânicas do jogo. 1 controlada pelo computador(run) e as outras 2 dependentes de inputs do jogador(jump e duck)
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()

        if user_input[pygame.K_UP] and not self.dino_jump:#função de pular
            self.dino_run = False
            self.dino_jump = True
            self.dino_duck = False
        elif user_input[pygame.K_DOWN] and not self.dino_jump:#função de agachar
            self.dino_run = False
            self.dino_jump = False
            self.dino_duck = True
        elif not self.dino_jump and not self.dino_duck:#função controlada pelo computador, o dinossauro nunca para de correr
            self.dino_run = True
            self.dino_jump = False
            self.dino_duck = False
        
        if self.step_index >= 10:#contagem de passos
            self.step_index = 0
    
    def run(self):#'ensinando' o computador a como lidar com a corrida do dino
        self.image = RUN_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index += 1

    def jump(self):#'ensinando' o computador a como lidar com o jump
        self.image = JUMP_IMG[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4 #varíaveis que cuidam da velocidade do pulo (1\2)
            self.jump_vel -= 0.8#(2/2)

        if self.jump_vel < - JUMP_VEL:
            self.dino_rect_y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL
    
    def duck(self):#'ensinando' o dino a agachar
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS#referente a hitbox do dino, se ele passou em um obstáculo ou não
        self.dino_rect.y = Y_POS_DUCK
        self.step_index += 1
        self.dino_duck = False

    def draw(self, screen):#.blit vai pedir pro pygame renderizar o que vier depois
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))