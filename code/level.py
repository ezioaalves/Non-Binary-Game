import pygame
from animation_player import AnimationPlayer
from utils import *
from tile import Tile
from player import Player
from weapon import Weapon
from ui import UI
from enemy import Enemy
from read_json import settings


class Level:
    def __init__(self):

        # busca a surface à ser mostrada
        self.display_surface = pygame.display.get_surface()
        # configuração do grupo de sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.portals_sprites = pygame.sprite.Group()

        # sprites do ataque
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.point_sprites = pygame.sprite.Group()

        # configuração de sprite
        self.create_map()

        # Interface de Usuario
        self.ui = UI()

        # particulas
        self.animation_player = AnimationPlayer()

        # sons
        self.hit_sound = pygame.mixer.Sound('audio/attack/acerto.wav')
        self.hit_sound.set_volume(0.2)
        self.shot_sound = pygame.mixer.Sound('audio/attack/disparo.wav')
        self.shot_sound.set_volume(0.2)

    def create_map(self):  # criando o dicionario
        layouts = {
            # limite que define onde o jogador pode ou nao ir
            'boundary': import_csv_layout('graphics/Tileset/Mapa 1._Divisas.csv'),
            # define as posicoes dos objetos no mapa
            'objects': import_csv_layout('graphics/Tileset/Mapa 1._Objetos.csv'),
            'entities': import_csv_layout('graphics/Tileset/Mapa 1._Inimigos.csv'),
            'portals': import_csv_layout('graphics/Tileset/Mapa 1._Teletransporte.csv')
        }
        graphics = {
            'objects': import_folder('graphics/Tileset/Objetos')
        }

        for style, layout in layouts.items():  # verificacao cada intem dentro do layouts
            for row_index, row in enumerate(layout):  # percorre as linhas
                # percorrer cada coluna na linha
                for col_index, col in enumerate(row):
                    if col != '-1':
                        # verificar a coluna que estamos andando (reserva o tilesize da coluna)
                        x = col_index * \
                            settings['general_settings']['tilesize']
                        # (reserva o tilesize da linha)
                        y = row_index * \
                            settings['general_settings']['tilesize']
                        if style == 'objects':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [
                                 self.visible_sprites, self.obstacles_sprites], 'objects', surf)
                        if style == 'boundary':
                            Tile((x, y), [self.obstacles_sprites],
                                 'boundary')
                        if style == 'portals':
                            Tile((x, y), [self.portals_sprites],
                                 'portal')
                        if style == 'entities':
                            if col == '266':
                                # define o jogador e sua position inicial
                                self.player = Player((x, y), [
                                                     self.visible_sprites], self.obstacles_sprites, self.portals_sprites,  self.create_attack, self.destroy_attack)
                            else:
                                if col == '230':
                                    monster_name = 'bug'
                                if col == '374':
                                    monster_name = 'cliente'
                                Enemy(monster_name, (x, y), [
                                      self.visible_sprites, self.attackable_sprites], self.obstacles_sprites, self.damage_player, self.trigger_death_particles)

    def create_attack(self):
        if self.player.energy >= 10:
            self.shot_sound.play()
            self.current_attack = Weapon(
                self.player, [self.visible_sprites])
            self.player.energy -= 10
            facing = self.player.status.split('_')[0]
            if facing == 'direita':
                direction = pygame.math.Vector2(1, 0)
            elif facing == 'esquerda':
                direction = pygame.math.Vector2(-1, 0)
            elif facing == 'cima':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)
            for i in range(1, 10):
                # horizontal
                if direction.x:
                    offset_x = (direction.x*i) * \
                        settings['general_settings']['tilesize']
                    shot_x = self.player.rect.centerx + offset_x
                    shot_y = self.player.rect.centery
                    self.animation_player.create_particles(
                        'apontar', (shot_x, shot_y), [self.visible_sprites, self.point_sprites])
                else:
                    offset_y = (direction.y*i) * \
                        settings['general_settings']['tilesize']
                    shot_x = self.player.rect.centerx
                    shot_y = self.player.rect.centery + offset_y
                    self.animation_player.create_particles(
                        'apontar', (shot_x, shot_y), [self.visible_sprites, self.point_sprites])
                for point_sprite in self.point_sprites:
                    hit = pygame.sprite.spritecollide(
                        point_sprite, self.obstacles_sprites, False)
                    hit_damage = pygame.sprite.spritecollide(
                        point_sprite, self.attackable_sprites, False)
                    if hit:
                        for target_sprite in hit:
                            position = target_sprite.rect.center
                            self.animation_player.create_particles('arma',
                                                                   position, [self.visible_sprites])
                    if hit_damage:
                        for target_sprite in hit_damage:
                            target_sprite.get_damage(self.player)
                            position = target_sprite.rect.center
                            self.animation_player.create_particles(
                                'arma', position, [self.visible_sprites])
                if hit or hit_damage:
                    self.hit_sound.play()
                    break

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(
                attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(
            particle_type, pos, self.visible_sprites)

    def run(self):
        # atualiza e desenha o jogo
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # configuração geral
        super().__init__()
        self.display_surface = pygame.display.get_surface()  # criando a superficie
        # a camera vai surgir no meio
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # criando o piso
        self.floor_surf = pygame.image.load(
            'graphics/Tileset/Mapa 1.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # buscando o offset para centralizar a camera no centro do jogador
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # desenhando o piso
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # funcao para os sprites ficar na frente do jogador
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(
            sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
