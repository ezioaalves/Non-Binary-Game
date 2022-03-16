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
        full_path = f'lib/graphics/weapons/twelve_{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        # sons
        self.hit_sound = pygame.mixer.Sound('lib/audio/attack/hit.wav')
        self.hit_sound.set_volume(0.2)
        self.shot_sound = pygame.mixer.Sound('lib/audio/attack/shot.wav')
        self.shot_sound.set_volume(0.2)

        # posição
        if direction == 'right':
            self.rect = self.image.get_rect(
                midleft=player.rect.midright+pygame.math.Vector2(-18, 10))
        elif direction == 'left':
            self.rect = self.image.get_rect(
                midright=player.rect.midleft+pygame.math.Vector2(18, 10))
        elif direction == 'down':
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom+pygame.math.Vector2(0, 0))
        elif direction == 'up':
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop+pygame.math.Vector2(0, 0))

    def shot_play(self):
        self.shot_sound.play()

    def hit_play(self):
        self.hit_sound.play()
