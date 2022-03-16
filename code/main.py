import pygame
import sys
from visual import Level
from read_json import settings
from visual import Screen


class Game:
    """
    classe que é responsavel pela execução do jogo,
    pelas configurações gerais, pela criação da superficie de exibição e pela 
    verificação do arquivo princiapal.
    """

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
        self.playing = self.title_screen

    '''método que começa o jogo'''

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
        self.title_screen = Screen("title", self.call_level)
        self.playing = self.title_screen

    def call_level(self):
        self.level = Level(self.call_gameover, self.call_final)
        self.playing = self.level

    def call_gameover(self):
        self.gameover_screen = Screen("gameover", self.call_title)
        self.playing = self.gameover_screen

    def call_final(self):
        self.final_screen = Screen("final", self.call_title)
        self.playing = self.final_screen


if __name__ == '__main__':  # verificacao do nosso arquivo principal
    game = Game()
    game.run()  # run da class que definimos o que vai executar
