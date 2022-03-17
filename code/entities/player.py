import pygame
from weapon import Weapon
from utils import import_folder, input
from . import Entity
from read_json import settings
from visual import AnimationPlayer


class Player(Entity):
    """
        nesta class contém as sprites(parte responsavel pelas imagens de movimentação do jogador) e suas informações.
        configurações das movimentações do jogador com suas direções.
        teletransporte do jogador com suas configurações.
        status do jogador, se está em movimentação ou parado.
        configurações dos ataques.
        animação do jogador e configurações da arma
    """

    def __init__(self, pos, groups, obstacle_sprites, portal_sprites, point_sprites, attackable_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(
            'lib/graphics/player/down/down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, -26)

        # graphics setup
        self.import_player_assets()
        self.status = 'down'

        # attacking
        self.attacking = False
        self.attack_cooldown = 300
        self.attack_time = None
        self.current_attack = None
        self.visible_sprites = groups[0]

        # teleporting
        self.teleporting = False
        self.teleport_cooldown = 300
        self.teleport_time = None
        self.teleport_sound = pygame.mixer.Sound(
            'lib/audio/portal/portal.wav')
        self.teleport_sound.set_volume(0.5)

        # attributes
        self.stats = {'health': 100, 'energy': 60,
                      'attack': 30, 'speed': 6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.attack = self.stats['attack']
        self.speed = self.stats['speed']

        # grupos de sprites
        self.point_sprites = point_sprites
        self.attackable_sprites = attackable_sprites
        self.obstacle_sprites = obstacle_sprites
        self.portal_sprites = portal_sprites

        # temporizador dano
        self.vulnerable = True
        self.hurt_time = None
        self.invicible_duration = 500

        # particulas
        self.animation_player = AnimationPlayer()

    def import_player_assets(self):
        '''carrega todos os sprites de todos os estados do jogador'''
        character_path = 'lib/graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def move(self, speed):
        '''responsável pela movimentação do jogador'''
        if self.attacking or self.teleporting:
            self.direction.x = 0
            self.direction.y = 0

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        self.teleport()

    def get_status(self):
        '''verifica os status do jogador e a posição em que ele parou'''

        # parado status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status:
                self.status = self.status + '_idle'

    def cooldowns(self):
        '''confere a pausa entre ações'''
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invicible_duration:
                self.vulnerable = True

        if self.teleporting:
            if current_time - self.teleport_time >= self.teleport_cooldown:
                self.teleporting = False

    def animate(self):
        '''animação do sprite do jogador'''
        animation = self.animations[self.status]

        # loop over the frame index
        self.set_frame_index(self.get_frame_index() +
                             self.get_animation_speed())
        if self.get_frame_index() >= len(animation):
            self.set_frame_index(0)

        # set the image
        self.image = animation[int(self.get_frame_index())]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # piscar
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def recover(self):
        '''recarrega a saúde e energia do jogador'''
        if self.energy <= self.stats['energy']:
            self.energy += 0.1
        else:
            self.energy = self.stats['energy']
        if self.health <= self.stats['health']:
            self.health += 0.01
        else:
            self.health = self.stats['health']

    def teleport(self):
        '''verifica a área do teletransporte e se o jogador entrou nela, com as informações para acontecer o teletransporte'''
        for sprite in self.portal_sprites:
            centralize = pygame.math.Vector2(24, 24)
            if sprite.hitbox.colliderect(self.hitbox):
                self.teleport_sound.play()
                self.teleport_time = pygame.time.get_ticks()

                self.teleporting = True

                if 3400 < sprite.rect.topleft[0] < 3500:
                    self.hitbox.center = (1776, 624)
                elif 1700 < sprite.rect.topleft[0] < 1800:
                    self.hitbox.center = (3456, 624)
                elif 2200 < sprite.rect.topleft[0] < 2300:
                    self.hitbox.center = (3936, 3888)
                else:
                    self.teleporting = False
                    break
                self.hitbox.center += centralize
                self.status = 'down_idle'

    def create_attack(self):
        '''cria o sprite de disparo'''
        if self.energy >= 10:
            self.current_attack = Weapon(self, [self.visible_sprites])
            self.current_attack.shot_play()
            self.energy -= 10
            # direção em que o tiro vai se mover
            facing = self.status.split('_')[0]
            if facing == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif facing == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif facing == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(1, 10):
                # horizontal
                if direction.x:
                    offset_x = (direction.x * i) * \
                        settings['general_settings']['tilesize']
                    shot_x = self.rect.centerx + offset_x
                    shot_y = self.rect.centery
                    self.animation_player.create_particles('pointing', (shot_x, shot_y), [
                                                           self.visible_sprites, self.point_sprites])
                # vertical
                else:
                    offset_y = (direction.y * i) * \
                        settings['general_settings']['tilesize']
                    shot_x = self.rect.centerx
                    shot_y = self.rect.centery + offset_y
                    self.animation_player.create_particles(
                        'pointing', (shot_x, shot_y), [self.visible_sprites, self.point_sprites])
                for point_sprite in self.point_sprites:
                    hit = pygame.sprite.spritecollide(
                        point_sprite, self.obstacle_sprites, False)
                    hit_damage = pygame.sprite.spritecollide(
                        point_sprite, self.attackable_sprites, False)
                    if hit:
                        for target_sprite in hit:
                            position = target_sprite.rect.center
                            self.animation_player.create_particles(
                                'gun', position, [self.visible_sprites])
                    if hit_damage:
                        for target_sprite in hit_damage:
                            target_sprite.get_damage(self)
                            position = target_sprite.rect.center
                            self.animation_player.create_particles(
                                'gun', position, [self.visible_sprites])
                if hit or hit_damage:
                    self.current_attack.hit_play()
                    break

    '''destrói o sprite de disparo'''

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def update(self):
        input(self)
        self.get_status()
        self.animate()
        self.cooldowns()
        self.move(self.speed)
        self.recover()
