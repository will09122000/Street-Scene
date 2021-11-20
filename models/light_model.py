import struct

from models.model import Base_Model

class Light_Model(Base_Model):
    """
    A class to represent a model that is not affected by any light source. Used in conjunction
    with a light object to give the appearance of a light.

    No additional attributes from Base_Model.
    """
    def __init__(self,
                 ctx,
                 position,
                 light_type,
                 texture,
                 vertices,
                 tex_coords,
                 norm_coords,
                 rotation = 0.0,
                 scale = 1.0):

        super().__init__(ctx,
                         position,
                         texture,
                         vertices,
                         tex_coords,
                         norm_coords,
                         rotation,
                         scale)

        self.light_type = light_type
        self.shader = ctx.program(vertex_shader = open('shaders/Light_Model_Vertex.glsl').read(),
                                  fragment_shader = open('shaders/Light_Model_Fragment.glsl').read())
        self.create_vao()

    def create_vao(self):
        position = self.ctx.buffer(struct.pack(f'{len(self.model_coords)}f', *self.model_coords))
        texture_coords  = self.ctx.buffer(struct.pack(f'{len(self.texture_coords)}f', *self.texture_coords))

        self.vao = self.ctx.vertex_array(self.shader, [(position, '3f', 'position'),
                                                       (texture_coords,  '2f', 'texture_coord')])

    def update(self, camera, lights=None):
        """Updates vertex shader uniforms."""

        self.shader['projection'].value = tuple(camera.projection.flatten())
        self.shader['model'].value      = tuple(self.position_matrix.flatten())
        self.shader['view'].value       = tuple(camera.get_view_matrix().flatten())
        self.shader['scale'].value      = tuple(self.scale.tolist())
