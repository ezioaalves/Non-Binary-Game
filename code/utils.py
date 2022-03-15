from csv import reader
from os import walk
import pygame

def import_csv_layout(path): #caminho do cvs para le 
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