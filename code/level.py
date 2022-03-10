from html import entities
import pygame
from settings import *
from utils import *
from tile import Tile
from player import Player
from weapon import Weapon
from ui import UI
from enemy import Enemy


class Level:
    def __init__(self):

        # busca a surface à ser mostrada
        self.display_surface = pygame.display.get_surface()
        # configuração do grupo de sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # sprites do ataque
        self.current_attack = None

        # configuração de sprite
        self.create_map()

        # Interface de Usuario
        self.ui = UI()

    def create_map(self):  # criando o dicionario
        layouts = {
            # limite que define onde o jogador pode ou nao ir
            'boundary': import_csv_layout('graphics/Tileset/Mapa 1._Divisas.csv'),
            # define as posicoes dos objetos no mapa
            'objects': import_csv_layout('graphics/Tileset/Mapa 1._Objetos.csv'),
            'entities': import_csv_layout('graphics\Tileset\Mapa 1._Inimigos.csv')
        }
        graphics = {
            'objects': import_folder('graphics\Tileset\Objetos')
        }

        for style, layout in layouts.items():  # verificacao cada intem dentro do layouts
            for row_index, row in enumerate(layout):  # percorre as linhas
                # percorrer cada coluna na linha
                for col_index, col in enumerate(row):
                    if col != '-1':
                        # verificar a coluna que estamos andando (reserva o tilesize da coluna)
                        x = col_index * TILESIZE
                        # (reserva o tilesize da linha)
                        y = row_index * TILESIZE
                        # if style == 'boundary':
                        # Tile((x, y), [self.obstacles_sprites],
                        # 'boundary')  # define a colisao
                        if style == 'objects':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [
                                 self.visible_sprites, self.obstacles_sprites], 'objects', surf)
                        if style == 'entities':
                            if col == '266':
                                # define o jogador e sua position inicial
                                self.player = Player((x, y), [
                                                     self.visible_sprites], self.obstacles_sprites, self.create_attack, self.destroy_attack)
                            else:
                                if col == '230':
                                    monster_name = 'bug'
                                Enemy(monster_name, (x, y), [
                                      self.visible_sprites], self.obstacles_sprites)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

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
