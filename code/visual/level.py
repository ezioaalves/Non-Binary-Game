import pygame
from .import YSortCameraGroup
from .import Tile
from .import UI
from utils import *
from entities import Player
from entities import Enemy
from read_json import settings


class Level:
    '''
        Classe responsavel por todas 
    '''

    def __init__(self, call_gameover, call_final):

        # busca a surface à ser mostrada
        self.display_surface = pygame.display.get_surface()
        # configuração do grupo de sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.portals_sprites = pygame.sprite.Group()

        # sprites do ataque
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.point_sprites = pygame.sprite.Group()

        # player
        self.player = Player((0, 0), [self.visible_sprites], self.obstacles_sprites,
                             self.portals_sprites, self.point_sprites, self.attackable_sprites, 'lib/graphics/player/down/down_0.png', 'down', (-15, -26))

        # screens
        self.call_gameover = call_gameover
        self.call_final = call_final

        # sons
        self.background = pygame.mixer.Sound('lib/audio/background/level.wav')
        self.background.set_volume(0.05)
        pygame.mixer.Channel(1).play(self.background, loops=-1)

        # criação do mapa
        self.create_map()

        # Interface de Usuario
        self.ui = UI()

    def create_map(self):
        ''' 
        Lê os arquivos do tipo csv com o layout do mapa, e dependendo dos valores nele cria os tiles e os sprites nas posições designadas
        '''
        layouts = {
            # limite que define onde o jogador pode ou nao ir
            'boundary': import_csv_layout('lib/data/map_grids/map_boundary.csv'),
            # define as posicoes dos objetos no mapa
            'objects': import_csv_layout('lib/data/map_grids/map_objects.csv'),
            'entities': import_csv_layout('lib/data/map_grids/map_entities.csv'),
            'portals': import_csv_layout('lib/data/map_grids/map_portals.csv')
        }
        graphics = {
            'objects': import_folder('lib/graphics/tileset/objects')
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
                                self.player.hitbox.center = (x+24, y+24)
                            else:
                                if col == '374':
                                    monster_name = 'client'
                                else:
                                    monster_name = 'bug'
                                Enemy(monster_name, (x, y), [
                                    self.visible_sprites, self.attackable_sprites], self.obstacles_sprites, self.function_final, self.function_gameover, 'lib/graphics/enemies/bug/idle/0.png', 'idle', (0, -10))

    def function_final(self):
        ''' Chama a função de tela final.'''
        self.background.stop()
        self.call_final()

    def function_gameover(self):
        ''' Chama a função tela de gameover'''
        self.background.stop()
        self.call_gameover()

    def run(self):
        ''' Atualiza e desenha o jogo. '''
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)
