import pyrr
import numpy as np

from model import Base_Model

class Dynamic_Model(Base_Model):
    """
    A class to represent a model that either rotates or transforms while the scene is running.

    Attributes
    ----------
    ctx:  moderngl.context | The ModernGL context exposing OpenGL features.
    position:        tuple | The starting position (XYZ) of the dynamic model in the scene.
    texture:        string | The filepath to the texture image for this model.
    vertices:         list | The model's geometric vertices.
    tex_coords:       list | The model's texture vertices.
    norm_coords:      list | The model's vertex normals.
    rotation:        float | The angle in radians at which the model should be rotated about the
                             Y-axis (Single float as there is no model that needs to be rotated
                             about another axis). 
    scale:           float | The scale at which the model is drawn comparted to the original model.
    translation      tuple | The speed at which models are translated in each dimension.
    """
    def __init__(self,
                 ctx,
                 position,
                 texture,
                 vertices,
                 tex_coords,
                 norm_coords,
                 rotation = 0.0,
                 scale = 1.0,
                 translation = (0.0, 0.0, 0.0)):

        super().__init__(ctx,
                         position,
                         texture,
                         vertices,
                         tex_coords,
                         norm_coords,
                         rotation,
                         scale)

        self.translation = translation
        self.map_edge = 24

    def translate(self):
        """
        Method to translate a dynamic model at each cycle.
        """
        # If the object has reached the end of the map.
        if np.abs(self.position_matrix).max() > self.map_edge:
            # Translate object to the opposite side of the map
            translation_matrix = pyrr.matrix44.create_from_translation([self.map_edge * 2, 0, 0])
            self.position_matrix = pyrr.matrix44.multiply(translation_matrix, self.position_matrix)
        else:
            # Translate object by the translate tuple provided.
            translation_matrix = pyrr.matrix44.create_from_translation([-self.translation[0], -self.translation[1], -self.translation[2]])
            self.position_matrix = pyrr.matrix44.multiply(translation_matrix, self.position_matrix)