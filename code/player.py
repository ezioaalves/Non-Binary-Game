import pygame
from settings import *
from utils import import_folder
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load(
            'graphics/player/baixo/baixo_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, -26)

        # graphics setup
        self.import_player_assets()
        self.status = 'baixo'

        # attacking
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        # atributos
        self.stats = {'vida': 100, 'energia': 60,
                      'ataque': 10, 'velocidade': 6}
        self.health = self.stats['vida']
        self.energy = self.stats['energia']
        self.speed = self.stats['velocidade']

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'cima': [], 'baixo': [], 'esquerda': [], 'direita': [],
                           'direita_parado': [], 'esquerda_parado': [], 'cima_parado': [], 'baixo_parado': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'cima'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'baixo'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'direita'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'esquerda'
            else:
                self.direction.x = 0

            # Tecla de disparo
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

    def get_status(self):

        # parado status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'parado' in self.status:
                self.status = self.status + '_parado'

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.cooldowns()
        self.move(self.speed)
