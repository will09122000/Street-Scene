from object_reader import read_obj, load_obj

def load_floor(ctx):
    """Loads the floor plane which includes the road, road markings, pavement and grass."""

    return [load_obj(ctx              = ctx,
                     obj_file         = read_obj('assets/models/floor.obj'),
                     texture_filepath = 'assets/textures/floor.png',
                     position         = (0, 0, 0))]


def load_statue(ctx):
    """Loads the Statue of Liberty to demonstrate environmental mapping."""

    return [load_obj(ctx = ctx,
                     obj_file = read_obj('assets/models/statue.obj'),
                     texture_filepath = 'assets/textures/white.png',
                     position = (20, 0, -20),
                     scale = 15,
                     mirror = True)]
