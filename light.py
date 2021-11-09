from pyrr import Vector3


class Light:
    '''
    Basic Phong (Ambient & Diffuse & Specular) lighting
    '''
    def __init__(self,
                position: tuple[float, float, float],
                color: tuple[float, float, float] = (1.0, 1.0, 1.0),
                ambient_intensity: float = 0.0,
                diffuse_intensity: float = 0.1,
                specular_intensity: float = 0.1,
                specular_power: float = 1):

        self.position = Vector3(position)
        self.color = color
        self.ambient_intensity = ambient_intensity
        self.diffuse_intensity = diffuse_intensity
        self.specular_intensity = specular_intensity
        self.specular_power = specular_power

class LampPostLight(Light):
    '''
    Unlit model doesn't get effected by any light source
    '''
    def __init__(self,
                position: tuple[float, float, float],
                color: tuple[float, float, float] = (1.0, 0.73, 0),
                ambient_intensity: float = 0.0,
                diffuse_intensity: float = 0.1,
                specular_intensity: float = 0.1,
                specular_power: float = 1):

        super().__init__(
            position,
            color,
            ambient_intensity,
            diffuse_intensity,
            specular_intensity,
            specular_power)
