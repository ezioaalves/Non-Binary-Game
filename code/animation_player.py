from particle_effect import ParticleEffect
from utils import import_folder


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
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)
