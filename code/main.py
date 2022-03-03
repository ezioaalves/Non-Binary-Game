import pygame
import sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        # configuração geral

        icon = pygame.image.load('../graphics/system/game_icon.png')
        pygame.display.set_caption('Non_Binary')
        pygame.display.set_icon(icon)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #criacao da superficie de exibicao
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self): #loop de eventos e metodo de execucao
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.level.run()
            pygame.display.update() # atualiza a tela
            self.clock.tick(FPS) #controle da taxa de quadros


if __name__ == '__main__': #verificacao do nosso arquivo principal
    game = Game() 
    game.run() #run da class que definimos o que vai executar
