from pyrr import Vector3

class Light:
    '''
    Basic Phong (Ambient & Diffuse & Specular) lighting
    '''
    def __init__(self,
                position: tuple[float, float, float],
                color: tuple[float, float, float] = (1.0, 1.0, 1.0),
                ambient: float = 0.0,
                diffuse: float = 0.1,
                specular: float = 0.1,
                specular_power: float = 1,
                attenuation: tuple[float, float, float] = (1.0, 0.09, 0.032)):

        self.position = Vector3(position)
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.specular_power = specular_power
        self.attenuation = attenuation

class LampPostLight(Light):
    '''
    Light model doesn't get effected by any light source
    '''
    def __init__(self,
                position: tuple[float, float, float],
                color: tuple[float, float, float] = (1.0, 0.73, 0.0),
                ambient: float = 0.0,
                diffuse: float = 0.5,
                specular: float = 0.2,
                specular_power: float = 1.0,
                attenuation: tuple[float, float, float] = (0.5, 0.1, 0.05)):

        super().__init__(
            position,
            color,
            ambient,
            diffuse,
            specular,
            specular_power,
            attenuation)

class WindowLight(Light):
    '''
    Light model doesn't get effected by any light source
    '''
    def __init__(self,
                position: tuple[float, float, float],
                color: tuple[float, float, float] = (0.2, 0.2, 0.2),
                ambient: float = 0.0,
                diffuse: float = 0.5,
                specular: float = 0.2,
                specular_power: float = 1.0,
                attenuation: tuple[float, float, float] = (0.5, 0.1, 0.05)):

        super().__init__(
            position,
            color,
            ambient,
            diffuse,
            specular,
            specular_power,
            attenuation)
