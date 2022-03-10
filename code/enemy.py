from ast import Pass
import pygame
from settings import *
from entity import Entity
from utils import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):

        # configuração geral
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # configuração grafica
        self.import_graphics('monster_name')
        self.status = 'baixo'
        self.image = pygame.image.load(
            'graphics/enemies/bug/baixo/baixo_0.png').convert_alpha()

        # movimento
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites
        self.attacking = False

        # atributos
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['vida']
        self.speed = monster_info['velocidade']
        self.attack_damage = monster_info['dano']
        self.resistance = monster_info['resistencia']
        self.attack_radius = monster_info['raio_ataque']
        self.notice_radius = monster_info['raio_percepcao']
        self.attack_type = monster_info['tipo_ataque']

    def import_graphics(self, name):
        self.animations = {'cima': [], 'baixo': [], 'esquerda': [], 'direita': [],
                           'direita_parado': [], 'esquerda_parado': [], 'cima_parado': [], 'baixo_parado': []}
        main_path = f'graphics\enemies/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec-enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec-enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius:
            self.status = 'ataque'
        elif distance <= self.notice_radius:
            self.status = 'andando'
        else:
            self.status = 'parado'

    def actions(self, player):
        if self.attacking == True:
            pass
        elif self.status == 'andando':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

#    def animate(self):
#        animation = self.animations[self.status]
#
#        # loop over the frame index
#        self.frame_index += self.animation_speed
#        if self.frame_index >= len(animation):
#            self.frame_index = 0
#
#        # set the image
#        self.image = animation[int(self.frame_index)]
#        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.move(self.speed)
        # self.animate()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
