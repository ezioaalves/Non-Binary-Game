import pygame
import sys
from level import Level
from read_json import settings
from screen import Screen


class Game:
    def __init__(self):
        # configuração geral

        icon = pygame.image.load('graphics/system/game_icon.png')
        pygame.display.set_caption('Non_Binary')
        pygame.display.set_icon(icon)
        pygame.init()
        # criacao da superficie de exibicao
        self.screen = pygame.display.set_mode(
            (settings["general_settings"]["width"], settings["general_settings"]["height"]))
        self.clock = pygame.time.Clock()
        self.level = Level(self.call_gameover, self.call_final)
        self.title_screen = Screen("title", self.call_level)
        self.gameover_screen = Screen("gameover", self.call_title)
        self.final_screen = Screen("final", self.call_title)
        self.black_screen = Screen("black", self.call_black)
        self.playing = self.title_screen

    def run(self):  # loop de eventos e metodo de execucao
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.playing.run()
            pygame.display.update()  # atualiza a tela
            # controle da taxa de quadros
            self.clock.tick(settings["general_settings"]["fps"])

    def call_title(self):
        self.playing = self.title_screen

    def call_level(self):
        self.playing = self.level

    def call_gameover(self):
        self.playing = self.gameover_screen

    def call_final(self):
        self.playing = self.final_screen


if __name__ == '__main__':  # verificacao do nosso arquivo principal
    game = Game()
    game.run()  # run da class que definimos o que vai executar
