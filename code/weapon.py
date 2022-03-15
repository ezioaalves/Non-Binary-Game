import pygame


"""
    class responsável pela movimentação do jogador atravez das teclas W A S D,
    com as  informações das direções, velocidade.
"""
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups) -> None:
        super().__init__(groups)
        direction = player.status.split('_')[0]

        # graficos
        full_path = f'graphics/weapons/twelve_{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        # posição
        if direction == 'direita':
            self.rect = self.image.get_rect(
                midleft=player.rect.midright+pygame.math.Vector2(-18, 10))
        elif direction == 'esquerda':
            self.rect = self.image.get_rect(
                midright=player.rect.midleft+pygame.math.Vector2(18, 10))
        elif direction == 'baixo':
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom+pygame.math.Vector2(0, 0))
        elif direction == 'cima':
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop+pygame.math.Vector2(0, 0))
