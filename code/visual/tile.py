import pygame
from read_json import settings


class Tile(pygame.sprite.Sprite):
    """
        classe responsavel pela criação dos desenhos e barreiras no mapa 
    """ 
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((settings['general_settings']['tilesize'], settings['general_settings']['tilesize']))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'objects':
            # deslocar o sprite
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-settings['general_settings']['tilesize']))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        if sprite_type == 'boundary':
            self.hitbox = self.rect.inflate(-20, -10)
        elif sprite_type == 'objects':
            self.hitbox = self.rect.inflate(0, -settings['general_settings']['tilesize'])
        else:
            self.hitbox = self.rect.inflate(0, -10)
