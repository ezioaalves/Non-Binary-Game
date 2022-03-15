import pygame
from weapon import Weapon
from utils import import_folder
from entity import Entity
from read_json import settings
from animation_player import AnimationPlayer


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, portal_sprites, point_sprites, attackable_sprites):
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
        self.current_attack = None
        self.visible_sprites = groups[0]

        # sons
        self.hit_sound = pygame.mixer.Sound('audio/attack/acerto.wav')
        self.hit_sound.set_volume(0.2)
        self.shot_sound = pygame.mixer.Sound('audio/attack/disparo.wav')
        self.shot_sound.set_volume(0.2)

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

        # grupos de sprites
        self.point_sprites = point_sprites
        self.attackable_sprites = attackable_sprites
        self.obstacle_sprites = obstacle_sprites
        self.portal_sprites = portal_sprites

        # temporizador dano
        self.vulnerable = True
        self.hurt_time = None
        self.invicible_duration = 500

        # particulas
        self.animation_player = AnimationPlayer()

    'carrega todos os sprites de todos os estados do jogador'
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

    'verifica se o jogador'
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

    'animação do sprite do jogador'
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

    'recarrega a saúde e energia do jogador'
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

    def create_attack(self):
        if self.energy >= 10:
            self.shot_sound.play()
            self.current_attack = Weapon(self, [self.visible_sprites])
            self.energy -= 10
            # direção em que o tiro vai se mover
            facing = self.status.split('_')[0]
            if facing == 'direita':
                direction = pygame.math.Vector2(1, 0)
            elif facing == 'esquerda':
                direction = pygame.math.Vector2(-1, 0)
            elif facing == 'cima':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(1, 10):
                #horizontal
                if direction.x:
                    offset_x = (direction.x * i) * settings['general_settings']['tilesize']
                    shot_x = self.rect.centerx + offset_x
                    shot_y = self.rect.centery
                    self.animation_player.create_particles('apontar', (shot_x, shot_y), [self.visible_sprites, self.point_sprites])
                else:
                    offset_y = (direction.y * i) * settings['general_settings']['tilesize']
                    shot_x = self.rect.centerx
                    shot_y = self.rect.centery + offset_y
                    self.animation_player.create_particles(
                        'apontar', (shot_x, shot_y), [self.visible_sprites, self.point_sprites])
                for point_sprite in self.point_sprites:
                    hit = pygame.sprite.spritecollide(
                        point_sprite, self.obstacle_sprites, False)
                    hit_damage = pygame.sprite.spritecollide(
                        point_sprite, self.attackable_sprites, False)
                    if hit:
                        for target_sprite in hit:
                            position = target_sprite.rect.center
                            self.animation_player.create_particles('arma', position, [self.visible_sprites])
                    if hit_damage:
                        for target_sprite in hit_damage:
                            target_sprite.get_damage(self)
                            position = target_sprite.rect.center
                            self.animation_player.create_particles(
                                'arma', position, [self.visible_sprites])
                if hit or hit_damage:
                    self.hit_sound.play()
                    break
    
    'destrói o sprite de disparo'
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.cooldowns()
        self.move(self.speed)
        self.recover()
