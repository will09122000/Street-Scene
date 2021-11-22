from math import radians
import numpy as np

from object_reader import read_obj, load_obj

def load_football_pitch(ctx):
    """Loads football goals and floodlights in one corner of the map."""

    football_pitch_items = []

    goal_obj = read_obj('assets/models/goal.obj')
    floodLight_obj = read_obj('assets/models/floodLight.obj')
    floodLightLight_obj = read_obj('assets/models/floodLightLight.obj')

    # Football goals
    football_pitch_items.append(load_obj(ctx              = ctx,
                                         obj_file         = goal_obj,
                                         texture_filepath = 'assets/textures/white.png',
                                         position         = (-16.59, 0, -7.1),
                                         rotation         = 0,
                                         scale            = 0.006))

    football_pitch_items.append(load_obj(ctx              = ctx,
                                         obj_file         = goal_obj,
                                         texture_filepath = 'assets/textures/white.png',
                                         position         = (-13.6, 0, -23.7),
                                         rotation         = radians(180),
                                         scale            = 0.006))

    # Floodlights
    for i in np.arange(-7.5, -27, -7.9):
        for j in np.arange(-9, -33.4, -12.2):
            football_pitch_items.append(load_obj(ctx              = ctx,
                                                 obj_file         = floodLight_obj,
                                                 texture_filepath = 'assets/textures/lampPost.png',
                                                 position         = (j, 0, i),
                                                 rotation         = radians(90)))

            football_pitch_items.append(load_obj(ctx              = ctx,
                                                 obj_file         = floodLightLight_obj,
                                                 texture_filepath = 'assets/textures/white.png',
                                                 position         = (j, -0.01, i-0.445),
                                                 rotation         = 0,
                                                 light_type       = 'floodLight'))

            football_pitch_items.append(load_obj(ctx              = ctx,
                                                 obj_file         = floodLightLight_obj,
                                                 texture_filepath = 'assets/textures/white.png',
                                                 position         = (j, -0.01, i+0.45),
                                                 rotation         = 0,
                                                 light_type       = 'floodLight'))

    return football_pitch_items
