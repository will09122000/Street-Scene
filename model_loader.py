from model import load_obj
from random import choices
from math import radians

map_edge = 24

def load_models(ctx):
    models = []
    model_list = [load_floor, load_cars, load_trees, load_lamp_posts]

    for i, loader in enumerate(model_list):
        model = loader(ctx)
        models.extend(model)

    models.append(load_obj(ctx, 'assets/models/house.obj', 'assets/textures/wood.png', (11, 0.001, 11), radians(180), 0.01))

    return models

def load_floor(ctx):
    return [load_obj(ctx, 'assets/models/floor.obj', 'assets/textures/floor.png', (0, 0, 0))]

def load_buildings(ctx):
    buildings = []

    buildings.append(load_obj(ctx, 'assets/models/building.obj', 'assets/textures/building.png', (17, 1.4, -10)))

    return buildings

def load_cars(ctx):
    cars = []
    colour = choices([0, 1, 2], k=9)

    # Moving cars
    cars.append(load_obj(ctx, 'assets/models/car' + str(colour[0]) +'.obj', 'assets/textures/car' + str(colour[4]) +'.png', (map_edge, 0, -1.1), 0, 0.6, 0.08, 1))
    cars.append(load_obj(ctx, 'assets/models/car' + str(colour[1]) +'.obj', 'assets/textures/car' + str(colour[4]) +'.png', (map_edge/4, 0, -1.1), 0, 0.6, 0.08, 1))
    cars.append(load_obj(ctx, 'assets/models/car' + str(colour[2]) +'.obj', 'assets/textures/car' + str(colour[4]) +'.png', (-map_edge, 0, 1.1), radians(180), 0.6, 0.09, -1))
    cars.append(load_obj(ctx, 'assets/models/car' + str(colour[3]) +'.obj', 'assets/textures/car' + str(colour[4]) +'.png', (-map_edge/4, 0, 1.1), radians(180), 0.6, 0.09, -1))

    # Stationary cars
    cars.append(load_obj(ctx, 'assets/models/car' + str(colour[4]) +'.obj', 'assets/textures/car' + str(colour[4]) +'.png', (1.1, 0, 8), radians(90), 0.6))
    cars.append(load_obj(ctx, 'assets/models/car' + str(colour[5]) +'.obj', 'assets/textures/car' + str(colour[5]) +'.png', (1.1, 0, 12), radians(90), 0.6))
    cars.append(load_obj(ctx, 'assets/models/car' + str(colour[6]) +'.obj', 'assets/textures/car' + str(colour[6]) +'.png', (1.1, 0, 16), radians(90), 0.6))
    cars.append(load_obj(ctx, 'assets/models/car' + str(colour[7]) +'.obj', 'assets/textures/car' + str(colour[7]) +'.png', (-1.1, 0, -8), radians(-90), 0.6))
    cars.append(load_obj(ctx, 'assets/models/car' + str(colour[8]) +'.obj', 'assets/textures/car' + str(colour[8]) +'.png', (-1.1, 0, -12), radians(-90), 0.6))

    return cars

def load_trees(ctx):
    trees = []
    x_spacer = 3.75
    y_spacer = 8

    repeat = False
    for i in range(0, 2):
        for j in range(-20, 28, y_spacer):
            # Prevent trees being placed too near the cross roads.
            if j < -8 or j > 8:
                left = True
                for k in range(0, 2):
                    if repeat:
                        position = [-x_spacer if left else x_spacer, 0, j]
                    else:
                        position = [j, 0, -x_spacer if left else x_spacer]

                    tree = load_obj(ctx, 'assets/models/tree.obj', 'assets/textures/tree.png', (position))
                    trees.append(tree)
                    left = not left
        repeat = True

    return trees

def load_lamp_posts(ctx):
    lamp_posts = []
    x_spacer = 5
    y_spacer = 8

    for i in range(0, 2):
        for j in range(-24, 32, y_spacer):
            # Prevent lamp posts being placed on the center of the map where the road is.
            if j != 0:
                left = True
                for k in range(-1, 2, 2):
                    if i > 0:
                        position = [-x_spacer if left else x_spacer, 0, j]
                        angle1, angle2 = radians(90), radians(-90)
                    else:
                        position = [j, 0, -x_spacer if left else x_spacer]
                        angle1, angle2 = radians(190), 0

                    lamp_post = load_obj(ctx, 'assets/models/lampPost.obj', 'assets/textures/lampPost.png', position, angle1 if left else angle2)
                    if i > 0:
                        light_position = (position[0]+(-0.29*k), position[1]+2.16, position[2]-((0.009 if left else -0.009)*k))
                    else:
                        light_position = (position[0]+((0.018 if left else 0.0008)*k), position[1]+2.16, position[2]+(-0.29*k))
                    lamp_post_light = load_obj(ctx, 'assets/models/lampPostLight.obj', 'assets/textures/lampPostLight.png', light_position, angle1 if left else angle2, 0.15, light=True)
                    lamp_posts.extend([lamp_post, lamp_post_light])
                    left = not left

    return lamp_posts
