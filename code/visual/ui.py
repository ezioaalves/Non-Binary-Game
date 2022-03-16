import pygame
from read_json import settings


class UI:
    '''
        classe responsável pela interface do usuário (barra que mostra saúde que o jogador tem e a energia da arma dele)
    '''
    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface()

        # configurações das barras
        self.health_bar_rect = pygame.Rect(
            10, 10, settings['ui']['health_bar_width'], settings['ui']['bar_height'])
        self.energy_bar_rect = pygame.Rect(
            10, 34, settings['ui']['energy_bar_width'], settings['ui']['bar_height'])

    def show_bar(self, current, max_amount, bg_rect, color):
        '''cria a barra da UI'''
        # desenha o fundo
        pygame.draw.rect(self.display_surface,
                         settings['ui_colors']['bg_color'], bg_rect)

        # convertendo atributos para pixels
        ratio = current/max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # desenhando a barra
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface,
                         settings['ui_colors']['border_color'], bg_rect, 3)

    def display(self, player):
        '''mostra a atualização das barras da UI'''
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, settings['ui_colors']['health_color'])
        self.show_bar(
            player.energy, player.stats['energy'], self.energy_bar_rect, settings['ui_colors']['energy_color'])
