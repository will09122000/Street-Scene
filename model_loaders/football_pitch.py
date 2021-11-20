from math import radians
import numpy as np

from objparser import parse, load_obj

def load_football_pitch(ctx):
    """Loads football goals and floodlights in one corner of the map."""

    football_pitch_items = []

    goal_obj = parse('assets/models/goal.obj')
    floodLight_obj = parse('assets/models/floodLight.obj')
    floodLightLight_obj = parse('assets/models/floodLightLight.obj')

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

    for i in np.arange(-9, -33.4, -12.2):
        football_pitch_items.append(load_obj(ctx              = ctx,
                                             obj_file         = floodLight_obj,
                                             texture_filepath = 'assets/textures/lampPost.png',
                                             position         = (i, 0, -15.4),
                                             rotation         = radians(90)))

        football_pitch_items.append(load_obj(ctx              = ctx,
                                             obj_file         = floodLightLight_obj,
                                             texture_filepath = 'assets/textures/white.png',
                                             position         = (i, 0, -15.845),
                                             rotation         = 0,
                                             light_type       = 'floodLight'))

        football_pitch_items.append(load_obj(ctx              = ctx,
                                             obj_file         = floodLightLight_obj,
                                             texture_filepath = 'assets/textures/white.png',
                                             position         = (i, 0, -14.95),
                                             rotation         = 0,
                                             light_type       = 'floodLight'))

    return football_pitch_items
