from .particle_effect import ParticleEffect
from utils import import_folder


"""
    Class responsavel pelas animações do player,
    no qual tem a interação do inimigo e jogador. 
"""


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # inimigos
            'erro': import_folder('graphics/animation\garra'),
            'alteracao': import_folder('graphics/animation\magia'),

            # jogador
            'arma': import_folder('graphics/animation/arma'),
            'apontar': import_folder('graphics/animation/apontar'),

            # morte inimigo
            'cliente': import_folder('graphics/animation/morte_cliente'),
            'bug': import_folder('graphics/animation/morte_bug')
        }

    def create_particles(self, animation_type, pos, groups):
        '''cria as partículas de efeito'''
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)
