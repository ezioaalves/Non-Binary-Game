from ast import Pass
import pygame
from entity import Entity
from utils import *
from read_json import settings


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, function):

        # configuração geral
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # configuração grafica
        self.import_graphics(monster_name)
        self.status = 'parado'
        self.image = pygame.image.load(
            'graphics/enemies/bug/parado/0.png').convert_alpha()

        # movimento
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # atributos
        self.monster_name = monster_name
        monster_info = settings['monster_data'][self.monster_name]
        self.health = monster_info['vida']
        self.speed = monster_info['velocidade']
        self.attack_damage = monster_info['dano']
        self.resistance = monster_info['resistencia']
        self.attack_radius = monster_info['raio_ataque']
        self.notice_radius = monster_info['raio_percepcao']
        self.attack_type = monster_info['tipo_ataque']

        # interação com jogador
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 800
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.function = function
        self.final_kill = None
        self.final_trigger = False

        # sons
        self.death_sound = pygame.mixer.Sound(
            'audio\death\inimigo_deletado.wav')
        self.death_sound.set_volume(0.2)
        self.attack_sound = pygame.mixer.Sound(monster_info['som_ataque'])
        self.attack_sound.set_volume(0.2)

    def import_graphics(self, name):
        '''carrega os sprites do inimigo'''
        self.animations = {'ataque': [], 'andando': [], 'parado': []}
        main_path = f'graphics\enemies/{name}/'
        for animation in self.animations.keys():
            full_path = main_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_player_distance_direction(self, player):
        '''pega a direção em que o inimigo irá se mover'''
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec-enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec-enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        '''pega o status em que o inimigo está'''
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'ataque':
                self.frame_index = 0
            self.status = 'ataque'
        elif distance <= self.notice_radius:
            self.status = 'andando'
        else:
            self.status = 'parado'

    def actions(self, player):
        '''determina as ações do inimigo'''
        if self.status == 'ataque':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == 'andando':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        '''cria a animação do inimigo'''
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'ataque':
                self.can_attack = False
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        '''tempo de espera entre cada ação do inimigo'''
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time >= self.invicible_duration:
                self.vulnerable = True
        if self.final_trigger:
            current_time = pygame.time.get_ticks()
            if current_time - self.final_kill >= 1000:
                self.function()
                self.kill()

    def get_damage(self, player):
        '''gerencia o dano causado pelo jogador no inimigo'''
        if self.vulnerable:
            self.health -= player.attack
            if self.health <= 0:
                self.trigger_death_particles(
                    self.rect.center, self.monster_name)
                self.death_sound.play()
                if self.monster_name == 'cliente':
                    self.final_kill = pygame.time.get_ticks()
                    self.final_trigger = True
                else:
                    self.kill()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
            self.direction = self.get_player_distance_direction(player)[1]
            self.direction *= -self.resistance

    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldowns()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
