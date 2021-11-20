from random import choices
from math import radians

from object_reader import read_obj, load_obj

def load_cars(ctx):
    """Loads both moving and stationary cars."""

    cars = []
    # 3 different colours possible, 9 cars total.
    colour = choices([0, 1, 2], k=9)
    map_edge = 24

    car_types = []
    # Load the 3 car objects.
    for i in range(0, 3):
        car_types.append(read_obj(f'assets/models/car{i}.obj'))

    # Moving cars
    cars.append(load_obj(ctx              = ctx,
                         obj_file         = car_types[colour[0]],
                         texture_filepath = f'assets/textures/car{colour[0]}.png',
                         position         = (map_edge, 0, -1.1),
                         rotation         = 0,
                         scale            = 0.6,
                         translation      = (0.08, 0.0, 0.0),
                         translate        = True))

    cars.append(load_obj(ctx              = ctx,
                         obj_file         = car_types[colour[1]],
                         texture_filepath = f'assets/textures/car{colour[1]}.png',
                         position         = (map_edge/4, 0, -1.1),
                         rotation         = 0,
                         scale            = 0.6,
                         translation      = (0.08, 0.0, 0.0),
                         translate        = True))

    cars.append(load_obj(ctx              = ctx,
                         obj_file         = car_types[colour[2]],
                         texture_filepath = f'assets/textures/car{colour[2]}.png',
                         position         = (map_edge, 0, 1.1),
                         rotation         = radians(180),
                         scale            = 0.6,
                         translation      = (0.08, 0.0, 0.0),
                         translate        = True))

    cars.append(load_obj(ctx              = ctx,
                         obj_file         = car_types[colour[3]],
                         texture_filepath = f'assets/textures/car{colour[3]}.png',
                         position         = (map_edge/4, 0, 1.1),
                         rotation         = radians(180),
                         scale            = 0.6,
                         translation      = (0.08, 0.0, 0.0),
                         translate        = True))

    # Stationary cars  
    cars.append(load_obj(ctx              = ctx,
                         obj_file         = car_types[colour[4]],
                         texture_filepath = f'assets/textures/car{colour[4]}.png',
                         position         = (1.1, 0, 8),
                         rotation         = radians(90),
                         scale            = 0.6))

    cars.append(load_obj(ctx              = ctx,
                         obj_file         = car_types[colour[5]],
                         texture_filepath = f'assets/textures/car{colour[5]}.png',
                         position         = (1.1, 0, 12),
                         rotation         = radians(90),
                         scale            = 0.6))

    cars.append(load_obj(ctx              = ctx,
                         obj_file         = car_types[colour[6]],
                         texture_filepath = f'assets/textures/car{colour[6]}.png',
                         position         = (1.1, 0, 16),
                         rotation         = radians(90),
                         scale            = 0.6))

    cars.append(load_obj(ctx              = ctx,
                         obj_file         = car_types[colour[7]],
                         texture_filepath = f'assets/textures/car{colour[7]}.png',
                         position         = (-1.1, 0, -8),
                         rotation         = radians(-90),
                         scale            = 0.6))

    cars.append(load_obj(ctx              = ctx,
                         obj_file         = car_types[colour[8]],
                         texture_filepath = f'assets/textures/car{colour[8]}.png',
                         position         = (-1.1, 0, -12),
                         rotation         = radians(-90),
                         scale            = 0.6))

    return cars