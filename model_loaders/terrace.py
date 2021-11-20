import numpy as np

from object_reader import read, load_obj

def load_terraces(ctx):
    """Load the terrace housing including the fences, chimneys and windows."""

    terraces = []

    terrace_obj = read('assets/models/terrace.obj')
    terrace_fence_obj = read('assets/models/terrace_fence.obj')
    chimney_obj = read('assets/models/chimney.obj')
    window_obj = read('assets/models/window.obj')

    for i in range(0, -60, -30):
        terraces.append(load_obj(ctx              = ctx,
                                 obj_file         = terrace_obj,
                                 texture_filepath = 'assets/textures/terrace.png',
                                 position         = (15+i, 0, 10)))
        terraces.append(load_obj(ctx              = ctx,
                                 obj_file         = terrace_fence_obj,
                                 texture_filepath = 'assets/textures/terrace_fence.png',
                                 position         = (15+i, 0, 10)))

        for j in np.arange(8.5, 23.5, 5):
            terraces.append(load_obj(ctx              = ctx,
                                     obj_file         = chimney_obj,
                                     texture_filepath = 'assets/textures/chimney.png',
                                     position         = (j+i, 0, 9.5)))

        for j in np.arange(7.52, 12.48, 4.96):
            for k in np.arange(0, 10.3, 5.1):
                terraces.append(load_obj(ctx              = ctx,
                                         obj_file         = window_obj,
                                         texture_filepath = 'assets/textures/white.png',
                                         position         = (i+k+8.5, 0.75, j),
                                         light_type       = 'window'))

                terraces.append(load_obj(ctx              = ctx,
                                         obj_file         = window_obj,
                                         texture_filepath = 'assets/textures/grey.png',
                                         position         = (i+k+11.2, 0.75, j)))

                terraces.append(load_obj(ctx              = ctx,
                                         obj_file         = window_obj,
                                         texture_filepath = 'assets/textures/grey.png',
                                         position         = (i+k+8.5, 2.25, j)))

                terraces.append(load_obj(ctx              = ctx,
                                         obj_file         = window_obj,
                                         texture_filepath = 'assets/textures/grey.png',
                                         position         = (i+k+11.2, 2.25, j)))

    return terraces
