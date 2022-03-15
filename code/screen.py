import pygame
from read_json import settings


class Screen:
    def __init__(self, screen_type, function):
        self.display_surface = pygame.display.get_surface()
        self.img_surface = pygame.image.load(
            settings['screen_img'][screen_type])
        self.background_sound = pygame.mixer.Sound(
            'audio/screen/'+screen_type+'.wav')
        self.background_sound.set_volume(0.2)
        self.function = function

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.background_sound.stop()
            self.function()

    def run(self):
        self.display_surface.blit(self.img_surface, (0, 0))
        self.background_sound.play(loops=-1)
        self.input()
