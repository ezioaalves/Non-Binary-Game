import pygame


class ParticleEffect(pygame.sprite.Sprite):
    ''' Classe para os efeitos especiais. '''

    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.24
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        ''' Cria a animação das partículas de efeito. '''
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        ''' Atualização das animações '''
        self.animate()
