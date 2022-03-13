from particle_effect import ParticleEffect
from utils import import_folder


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # inimigos
            'garra': import_folder('graphics/animation\garra'),
            'magia': import_folder('graphics/animation\magia'),

            # jogador
            'arma': import_folder('graphics/animation/arma'),

            # morte inimigo
            'morte_cliente': import_folder('graphics/animation/morte_cliente'),
            'morte_bug': import_folder('graphics/animation/morte_bug')
        }

    def create_gun_particles(self, pos, groups):
        animation_frames = self.frames['arma']
        ParticleEffect(pos, animation_frames, groups)
