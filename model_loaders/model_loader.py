from math import radians

from objparser import parse, load_obj

from model_loaders.car import load_cars
from model_loaders.tree import load_trees
from model_loaders.lamp_post import load_lamp_posts
from model_loaders.terrace import load_terraces
from model_loaders.football_pitch import load_football_pitch

def load_models(ctx):
    models = []
    model_list = [load_floor, load_cars, load_trees, load_lamp_posts, load_terraces, load_statue, load_football_pitch]

    for loader in model_list:
        model = loader(ctx)
        models.extend(model)

    models.append(load_obj(ctx, parse('assets/models/mgr.obj'), 'assets/textures/mgr.png', (10, 0, -10), radians(1), 1, rotate=True))

    return models

def load_floor(ctx):
    return [load_obj(ctx, parse('assets/models/floor.obj'), 'assets/textures/floor.png', (0, 0, 0))]


def load_statue(ctx):
    return [load_obj(ctx, parse('assets/models/statue.obj'), 'assets/textures/white.png', (15, 0, -15), 0, 15, mirror=True)]
