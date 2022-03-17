from .particle_effect import ParticleEffect
from utils import import_folder


class GetParticle:
    ''' Classe responsável pelas animações do player, no qual tem a interação do inimigo e jogador. '''

    def __init__(self):
        self.frames = {
            # inimigos
            'error': import_folder('lib/graphics/animation/claw'),
            'alteration': import_folder('lib/graphics/animation/alteration'),

            # jogador
            'gun': import_folder('lib/graphics/animation/gun'),
            'pointing': import_folder('lib/graphics/animation/pointing'),

            # morte inimigo
            'client': import_folder('lib/graphics/animation/death_client'),
            'bug': import_folder('lib/graphics/animation/death_bug')
        }

    def create_particles(self, animation_type, pos, groups):
        ''' Cria as partículas de efeito. '''
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)
