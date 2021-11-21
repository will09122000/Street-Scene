from math import radians
from model_loaders.traffic_light import load_traffic_lights

from object_reader import read_obj, load_obj

from model_loaders.car import load_cars
from model_loaders.tree import load_trees
from model_loaders.lamp_post import load_lamp_posts
from model_loaders.terrace import load_terraces
from model_loaders.football_pitch import load_football_pitch
from model_loaders.other import load_floor, load_statue

def load_models(ctx):
    """Loads all models into a single model list."""

    models = []
    model_list = [load_floor, load_cars, load_trees, load_lamp_posts, load_terraces, load_statue,
                  load_football_pitch, load_traffic_lights]

    for loader in model_list:
        model = loader(ctx)
        models.extend(model)

    models.append(load_obj(ctx, read_obj('assets/models/mgr.obj'), 'assets/textures/mgr.png', (10, 0, -10), radians(1), 1, rotate=True))

    return models
