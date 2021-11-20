import pyrr
import numpy as np

from models.model import Base_Model

class Dynamic_Model(Base_Model):
    """
    A class to represent a model that either rotates or transforms while the scene is running.

    Additional attributes from Base_Model
    ----------
    translation: tuple | The speed at which models are translated in each dimension.
    map_edge:      int | The edge of the floor plane to reset cars when they move off the
                         edge of the map.
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

    def rotate(self):
        """Rotate the model."""
        rotation_matrix = pyrr.matrix44.create_from_y_rotation(self.rotation[1])
        self.position_matrix = pyrr.matrix44.multiply(rotation_matrix, self.position_matrix)