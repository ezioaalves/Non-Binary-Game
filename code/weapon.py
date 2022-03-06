import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups) -> None:
        super().__init__(groups)
        direction = player.status.split('_')[0]

        # graficos
        self.image = pygame.Surface((40, 40))

        # posição
        if direction == 'direita':
            self.rect = self.image.get_rect(midleft=player.rect.midright)
        elif direction == 'esquerda':
            self.rect = self.image.get_rect(midright=player.rect.midleft)
        elif direction == 'baixo':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom)
        elif direction == 'cima':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop)
