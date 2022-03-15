import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'objects':
            # deslocar o sprite
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        if sprite_type == 'boundary':
            self.hitbox = self.rect.inflate(-20, -10)
        elif sprite_type == 'objects':
            self.hitbox = self.rect.inflate(0, -TILESIZE)
        else:
            self.hitbox = self.rect.inflate(0, -10)
