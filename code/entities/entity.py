import pygame
import abc
from math import sin


class Entity(pygame.sprite.Sprite, abc.ABC):
    '''
        Classe genérica para as entidades player e enemy
    '''

    def __init__(self, groups, default_image_path, pos, status, hitbox_inflation):
        super().__init__(groups)

        self.image = pygame.image.load(default_image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(
            hitbox_inflation[0], hitbox_inflation[1])
        self.status = status

        self.__frame_index = 0
        self.__animation_speed = 0.06
        self.direction = pygame.math.Vector2()
        self.vulnerable = True
        self.hit_time = None
        self.__invicible_duration = 300

    def set_frame_index(self, value):
        self.__frame_index = value

    def get_frame_index(self):
        return self.__frame_index

    def set_animation_speed(self, value):
        self.__animation_speed = value

    def get_animation_speed(self):
        return self.__animation_speed

    def set_invicible_duration(self, value):
        self.__invicible_duration = value

    def get_invicible_duration(self):
        return self.__invicible_duration

    def move(self, speed):
        ''' 
        Define a movimentação da entidade. 
        :param speed: int.
        '''

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        ''' 
        Recebe a direção na qual a entidade está se movendo e verifica as colisões nessa direção.
        :param direction: string.
        '''

        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    @abc.abstractmethod
    def animate(self):
        '''Exige que seus implementem uma função de animação'''
        pass

    @abc.abstractmethod
    def cooldowns(self):
        '''Exige que seus implementem uma função de pausa entre ações'''
        pass

    def wave_value(self):
        ''' 
        Efeito de piscar no jogador.
        Retorna int.
        '''

        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
