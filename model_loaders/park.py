from math import radians
import numpy as np

from object_reader import read_obj, load_obj

def load_park(ctx):
    """Loads park objects into one corner of the crossroads."""

    park_objects = []

    # Fence
    park_objects.append(load_obj(ctx              = ctx,
                                 obj_file         = read_obj('assets/models/parkFence.obj'),
                                 texture_filepath = 'assets/textures/terrace_fence.png',
                                 position         = (11, 0, -8.5),
                                 scale            = 0.2))

    # Merry-go-round
    park_objects.append(load_obj(ctx = ctx,
                                 obj_file = read_obj('assets/models/mgr.obj'),
                                 texture_filepath = 'assets/textures/metal.png',
                                 position = (10, 0, -10),
                                 rotation = radians(1),
                                 rotate = True))

    # Seesaws
    for i in range(-13, -15, -1):
        park_objects.append(load_obj(ctx              = ctx,
                                     obj_file         = read_obj('assets/models/seesaw.obj'),
                                     texture_filepath = 'assets/textures/blue.png',
                                     position         = (10, 0, i),
                                     scale            = 0.1,
                                     rotation         = 0))

    # Benches
    for i in np.arange(-10, -14, -3.5):
        park_objects.append(load_obj(ctx = ctx,
                                     obj_file = read_obj('assets/models/bench.obj'),
                                     texture_filepath = 'assets/textures/bench.png',
                                     position = (13.5, 0, i),
                                     rotation = radians(90)))
 
    return park_objects
