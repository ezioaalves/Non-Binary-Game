# configuração do jogo

WIDTH = 960
HEIGHT = 540
FPS = 60
TILESIZE = 48

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics\Font\Mega-Man-Battle-Network.ttf'
UI_FONT_SIZE = 18

# cores gerais
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# cores da UI
HEALTH_COLOR = 'green'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# inimigos
monster_data = {
    'bug': {'vida': 60, 'dano': 20, 'tipo_ataque': 'erro', 'som_ataque': 'audio/attack\erro.wav', 'velocidade': 3, 'resistencia': 3, 'raio_ataque': 80, 'raio_percepcao': 360},
    'cliente': {'vida': 300, 'dano': 40, 'tipo_ataque': 'alteracao', 'som_ataque': 'audio/attack\erro.wav', 'velocidade': 2, 'resistencia': 0, 'raio_ataque': 400, 'raio_percepcao': 0}
}
