import pygame
from utils import import_folder
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, portal_sprites, create_attack, destroy_attack):
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
        self.attack_cooldown = 300
        self.attack_time = None
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        # teleporting
        self.teleporting = False
        self.teleport_cooldown = 300
        self.teleport_time = None

        # atributos
        self.stats = {'vida': 100, 'energia': 60,
                      'ataque': 30, 'velocidade': 6}
        self.health = self.stats['vida']
        self.energy = self.stats['energia']
        self.attack = self.stats['ataque']
        self.speed = self.stats['velocidade']

        self.obstacle_sprites = obstacle_sprites
        self.portal_sprites = portal_sprites

        # temporizador dano
        self.vulnerable = True
        self.hurt_time = None
        self.invicible_duration = 500

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'cima': [], 'baixo': [], 'esquerda': [], 'direita': [],
                           'direita_parado': [], 'esquerda_parado': [], 'cima_parado': [], 'baixo_parado': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking and not self.teleporting:
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

    def move(self, speed):
        if self.attacking or self.teleporting:
            self.direction.x = 0
            self.direction.y = 0

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        self.telepot()

    def get_status(self):

        # parado status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'parado' in self.status:
                self.status = self.status + '_parado'

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invicible_duration:
                self.vulnerable = True

        if self.teleporting:
            if current_time - self.teleport_time >= self.teleport_cooldown:
                self.teleporting = False

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # piscar
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def recover(self):
        if self.energy <= self.stats['energia']:
            self.energy += 0.05
        else:
            self.energy = self.stats['energia']
        if self.health <= self.stats['vida']:
            self.health += 0.01
        else:
            self.health = self.stats['vida']

    def telepot(self):
        for sprite in self.portal_sprites:
            centralize = pygame.math.Vector2(24, 24)
            if sprite.hitbox.colliderect(self.hitbox):
                self.teleport_time = pygame.time.get_ticks()

                self.teleporting = True

                if 3400 < sprite.rect.topleft[0] < 3500:
                    self.hitbox.center = (1776, 624)
                elif 1700 < sprite.rect.topleft[0] < 1800:
                    self.hitbox.center = (3456, 624)
                elif 2200 < sprite.rect.topleft[0] < 2300:
                    self.hitbox.center = (3936, 3888)
                else:
                    self.teleporting = False
                    break
                self.hitbox.center += centralize
                self.status = 'baixo_parado'

    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.cooldowns()
        self.move(self.speed)
        self.recover()
