import pygame
from settings import *
from utils import *
from tile import Tile
from player import Player

#from random import choice


class Level:
    def __init__(self):

        # busca a surface à ser mostrada
        self.display_surface = pygame.display.get_surface()
        # configuração do grupo de sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        # configuração de sprite'
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../graphics/Tileset/Mapa 1._Divisas.csv'),
            'objects': import_csv_layout('../graphics/Tileset/Mapa 1._Objetos.csv'),
            # 'junk': import_csv_layout('../graphics/Tileset/Mapa 1._Junk.csv')
        }
        """ graphics = {
            'junk': import_folder('../graphics/Tileset/junk')
        } """

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacles_sprites], 'boundary')
                        """ if style == 'junk':
                            random_junk_image = choice(graphics['junk'])
                            Tile((x, y), [
                                 self.visible_sprites, self.obstacles_sprites], 'junk', random_junk_image) """
                        if style == 'objects':
                            Tile((x, y), [self.obstacles_sprites], 'object')
                    """if col == 'x':
                        Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                    if col == 'p':
                        self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites) """
        self.player = Player(
            (2736, 1100), [self.visible_sprites], self.obstacles_sprites)

    def run(self):
        # atualiza e desenha o jogo
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # configuração geral
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # criando o piso
        self.floor_surf = pygame.image.load(
            '../graphics/Tileset/Mapa 1.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # buscando o offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # desenhando o piso
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
