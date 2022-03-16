from csv import reader
from os import walk
import pygame


def import_csv_layout(path):  # caminho do cvs para le
    '''
        importa o csv que contêm as informações de objetos e obstaculos
    '''
    terrain_map = []
    with open(path) as level_map:  # abrindo o caminho e arquivo
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    '''
        importa todos os sprites que estão na pasta do caminho passado como parâmetro
    '''
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def input(player):
    if not player.attacking and not player.teleporting:
        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_w]:
            player.direction.y = -1
            player.status = 'up'
        elif keys[pygame.K_s]:
            player.direction.y = 1
            player.status = 'down'
        else:
            player.direction.y = 0

        if keys[pygame.K_d]:
            player.direction.x = 1
            player.status = 'right'
        elif keys[pygame.K_a]:
            player.direction.x = -1
            player.status = 'left'
        else:
            player.direction.x = 0

        # Tecla de disparo
        if keys[pygame.K_SPACE]:
            player.attacking = True
            player.attack_time = pygame.time.get_ticks()
            player.create_attack()
