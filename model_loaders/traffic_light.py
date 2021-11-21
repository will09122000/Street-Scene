from math import radians

from object_reader import read_obj, load_obj

def load_traffic_lights(ctx):
    """Loads lamp posts and lamp post lights on the edge of the pavement."""
    traffic_lights = []
    x_spacer = 5
    y_spacer = 8

    traffic_light_obj = read_obj('assets/models/trafficLight.obj')

    traffic_lights.append(load_obj(ctx              = ctx,
                                   obj_file         = traffic_light_obj,
                                   texture_filepath = 'assets/textures/mgr.png',
                                   position         = (4, 0, -2.5),
                                   rotation         = 0,
                                   scale            = 0.015))

    traffic_lights.append(load_obj(ctx              = ctx,
                                   obj_file         = traffic_light_obj,
                                   texture_filepath = 'assets/textures/mgr.png',
                                   position         = (2.5, 0, 4),
                                   rotation         = radians(90),
                                   scale            = 0.015))

    traffic_lights.append(load_obj(ctx              = ctx,
                                   obj_file         = traffic_light_obj,
                                   texture_filepath = 'assets/textures/mgr.png',
                                   position         = (-4, 0, 2.5),
                                   rotation         = radians(180),
                                   scale            = 0.015))

    traffic_lights.append(load_obj(ctx              = ctx,
                                   obj_file         = traffic_light_obj,
                                   texture_filepath = 'assets/textures/mgr.png',
                                   position         = (-2.5, 0, -4),
                                   rotation         = radians(-90),
                                   scale            = 0.015))

    return traffic_lights

    """
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
                        angle1, angle2 = radians(180), 0

                    lamp_post = load_obj(ctx              = ctx,
                                         obj_file         = lamp_post_obj,
                                         texture_filepath = 'assets/textures/lampPost.png',
                                         position         = position,
                                         rotation         = angle1 if left else angle2)

                    if i > 0:
                        light_position = (position[0]+(-0.29*k), position[1]+2.16, position[2])
                    else:
                        light_position = (position[0], position[1]+2.16, position[2]+(-0.29*k))

                    lamp_post_light = load_obj(ctx              = ctx,
                                               obj_file         = lamp_post_light_obj,
                                               texture_filepath = 'assets/textures/lampPostLight.png',
                                               position         = light_position,
                                               rotation         = angle1 if left else angle2,
                                               scale            = 0.15,
                                               light_type       = 'lampPost')

                    lamp_posts.extend([lamp_post, lamp_post_light])
                    left = not left
    """
    return traffic_lights
