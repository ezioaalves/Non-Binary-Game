import pygame


class YSortCameraGroup(pygame.sprite.Group):
    ''' Classe responsável por criar a câmera que seguira os movimentos do jogador. '''

    def __init__(self):
        # configuração geral
        super().__init__()
        self.display_surface = pygame.display.get_surface()  # criando a superficie
        # a camera vai surgir no meio
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # criando o piso
        self.floor_surf = pygame.image.load(
            'lib/graphics/tileset/map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        ''' Faz com que as sprites sejam desenhadas com um "desvio" para o centro da tela,
        baseado na posição do player.

        '''

        # buscando o offset para centralizar a camera no centro do jogador
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # desenha o piso e garante que ele fique embaixo de todas as outras sprites
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # ordena o desenho de cada sprite baseado na sua posição y
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        '''Procura por todos os sprites de inimigos dentro desse grupo
        e os atualiza

        '''
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(
            sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
