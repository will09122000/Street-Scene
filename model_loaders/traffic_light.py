from math import radians
import numpy as np

from object_reader import read_obj, load_obj

def load_traffic_lights(ctx):
    """Loads green and red traffic lights on each corner of the pavement."""
    traffic_lights = []

    traffic_light_obj = read_obj('assets/models/trafficLight.obj')
    traffic_light_light_obj = read_obj('assets/models/trafficLightLight.obj')

    # Green traffic lights
    for i in range(-1, 2, 2):
        print(i)
        traffic_lights.append(load_obj(ctx              = ctx,
                                       obj_file         = traffic_light_obj,
                                       texture_filepath = 'assets/textures/mgr.png',
                                       position         = (4*i, 0, -2.5*i),
                                       rotation         = 0 if i == 1 else radians(180),
                                       scale            = 0.015))
        for j in np.arange(2.051, 2.5, 0.2):
            traffic_lights.append(load_obj(ctx              = ctx,
                                           obj_file         = traffic_light_light_obj,
                                           texture_filepath = 'assets/textures/{}.png'
                                                              .format('green' if j == 2.051 else 'black'),
                                           position         = (4.11*i, j, -2.5*i),
                                           rotation         = 0,
                                           scale            = 0.2,
                                           light_type       = 'greenLight' if j == 2.051 else None))

    # Red traffic lights
    for i in range(-1, 2, 2):
        print(i)
        traffic_lights.append(load_obj(ctx              = ctx,
                                       obj_file         = traffic_light_obj,
                                       texture_filepath = 'assets/textures/mgr.png',
                                       position         = (-2.5*i, 0, -4*i),
                                       rotation         = radians(90) if i == -1 else radians(-90),
                                       scale            = 0.015))
        for j in np.arange(2.451, 2, -0.2):
            traffic_lights.append(load_obj(ctx              = ctx,
                                           obj_file         = traffic_light_light_obj,
                                           texture_filepath = 'assets/textures/{}.png'
                                                              .format('red' if j == 2.451 else 'black'),
                                           position         = (-2.5*i, j, -4.11*i),
                                           rotation         = radians(90),
                                           scale            = 0.2,
                                           light_type       = 'redLight' if j == 2.451 else None))

    return traffic_lights
