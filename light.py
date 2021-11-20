from pyrr import Vector3

class Light:
    """
    A class to represent a point light in the scene.

    Attributes
    ----------
    position :           Vector3 | The position of the light as a 3D vector.
    color :                tuple | The color of light emitted in an RGB format.
    ambient                float | Strength of ambient lighting from 0 to 1.
    diffuse                float | Strength of diffuse lighting from 0 to 1.
    specular               float | Strength of specular lighting from 0 to 1.
    attenuation            tuple | The constant, linear and quadratic attenuation.
    """

    def __init__(self,
                 position,
                 color,
                 ambient,
                 diffuse,
                 specular,
                 attenuation):

        self.position = Vector3(position)
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.attenuation = attenuation

class LampPostLight(Light):
    """
    An orange light to emit from the top of the lamp post.
    """
    def __init__(self,
                 position,
                 color       = (1.0, 0.73, 0.0),
                 ambient     = 0.0,
                 diffuse     = 0.5,
                 specular    = 0.2,
                 attenuation = (0.5, 0.1, 0.05)):

        super().__init__(
            position,
            color,
            ambient,
            diffuse,
            specular,
            attenuation)

class WindowLight(Light):
    """
    A white light emitting from a house window.
    """
    def __init__(self,
                 position,
                 color       = (0.2, 0.2, 0.2),
                 ambient     = 0.0,
                 diffuse     = 0.5,
                 specular    = 0.2,
                 attenuation = (0.5, 0.1, 0.05)):

        super().__init__(position,
                         color,
                         ambient,
                         diffuse,
                         specular,
                         attenuation)

class FloodLight(Light):
    """
    An orange light to emit from the top of the football pitch floodlight.
    """
    def __init__(self,
                 position,
                 color       = (1.0, 1.0, 1.0),
                 ambient     = 0.0,
                 diffuse     = 0.5,
                 specular    = 0.2,
                 attenuation = (0.5, 0.1, 0.05)):

        super().__init__(position,
                         color,
                         ambient,
                         diffuse,
                         specular,
                         attenuation)
