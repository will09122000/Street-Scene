import pyrr
import numpy as np

from model import Base_Model

class Dynamic_Model(Base_Model):
    def __init__(self,
        ctx,
        position,
        texture,
        vertices,
        tex_coords,
        norm_coords,
        rotation = 0.0,
        scale = 1.0,
        translation = 0.0):

        super().__init__(
            ctx,
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
        if np.abs(self.position_matrix).max() > self.map_edge:
            translation_matrix = pyrr.matrix44.create_from_translation([self.map_edge * 2, 0, 0])
            self.position_matrix = pyrr.matrix44.multiply(translation_matrix, self.position_matrix)
        else:
            translation_matrix = pyrr.matrix44.create_from_translation([-self.translation, 0, 0])
            self.position_matrix = pyrr.matrix44.multiply(translation_matrix, self.position_matrix)