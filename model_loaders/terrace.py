import numpy as np
from random import shuffle

from object_reader import read_obj, load_obj

def load_terraces(ctx):
    """Load the terrace housing including the fences, chimneys and windows."""

    terraces = []

    # Read the housing object files.
    terrace_obj = read_obj('assets/models/terrace.obj')
    terrace_fence_obj = read_obj('assets/models/terrace_fence.obj')
    chimney_obj = read_obj('assets/models/chimney.obj')
    window_obj = read_obj('assets/models/window.obj')

    for i in range(0, -60, -30):

        # Terrace
        terraces.append(load_obj(ctx              = ctx,
                                 obj_file         = terrace_obj,
                                 texture_filepath = 'assets/textures/terrace.png',
                                 position         = (15+i, 0, 10)))
        # Garden fencing
        terraces.append(load_obj(ctx              = ctx,
                                 obj_file         = terrace_fence_obj,
                                 texture_filepath = 'assets/textures/terrace_fence.png',
                                 position         = (15+i, 0, 10)))
        # Terrace chimneys
        for j in np.arange(8.5, 23.5, 5):
            terraces.append(load_obj(ctx              = ctx,
                                     obj_file         = chimney_obj,
                                     texture_filepath = 'assets/textures/chimney.png',
                                     position         = (j+i, 0, 9.5)))

        # Half the windows will will emit light, the other half will not.
        light_on = [True] * 12 + [False] * 12
        # Shuffle the order so random windows emit light.
        shuffle(light_on)
        light_index = 0

        # Terrace windows
        for j in np.arange(7.51, 12.5, 4.975):
            for k in np.arange(0, 10.3, 5.1):
                terraces.append(load_obj(ctx              = ctx,
                                         obj_file         = window_obj,
                                         texture_filepath = 'assets/textures/{}.png'
                                                            .format('white' if light_on[light_index] else 'grey'),
                                         position         = (i+k+8.5, 0.75, j),
                                         light_type       = 'window' if light_on[light_index] else None))
                light_index += 1
                terraces.append(load_obj(ctx              = ctx,
                                         obj_file         = window_obj,
                                         texture_filepath = 'assets/textures/{}.png'
                                                            .format('white' if light_on[light_index] else 'grey'),
                                         position         = (i+k+11.2, 0.75, j),
                                         light_type       = 'window' if light_on[light_index] else None))
                light_index += 1
                terraces.append(load_obj(ctx              = ctx,
                                         obj_file         = window_obj,
                                         texture_filepath = 'assets/textures/{}.png'
                                                            .format('white' if light_on[light_index] else 'grey'),
                                         position         = (i+k+8.5, 2.25, j),
                                         light_type       = 'window' if light_on[light_index] else None))
                light_index += 1
                terraces.append(load_obj(ctx              = ctx,
                                         obj_file         = window_obj,
                                         texture_filepath = 'assets/textures/{}.png'
                                                            .format('white' if light_on[light_index] else 'grey'),
                                         position         = (i+k+11.2, 2.25, j),
                                         light_type       = 'window' if light_on[light_index] else None))
                light_index += 1

    return terraces
