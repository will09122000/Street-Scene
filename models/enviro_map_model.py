import struct

from models.model import Base_Model

class Enviro_Map_Model(Base_Model):
    """
    A class to represent a model that reflects the skybox texture.

    No additional attributes from Base_Model.
    """
    def __init__(self,
                 ctx,
                 position,
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

        # Compile environmental mapping shader.
        self.shader = ctx.program(vertex_shader = open('shaders/Enviro_Map_Model_Vertex.glsl').read(),
                                  fragment_shader = open('shaders/Enviro_Map_Model_Fragment.glsl').read())

        # Creates model's VAO.
        position = self.ctx.buffer(struct.pack(f'{len(self.model_coords)}f', *self.model_coords))
        normal = self.ctx.buffer(struct.pack(f'{len(self.norm_coords)}f', *self.norm_coords))

        self.vao = self.ctx.vertex_array(self.shader, [(position, '3f', 'position'),
                                                       (normal, '3f', 'normal')])

    def update(self, camera, lights=None):
        """Updates both vertex and fragment shader uniforms."""

        # Vertex
        self.shader['projection'].value    = tuple(camera.projection.flatten())
        self.shader['model'].value         = tuple(self.position_matrix.flatten())
        self.shader['view'].value          = tuple(camera.get_view_matrix().flatten())
        self.shader['scale'].value         = tuple(self.scale.tolist())

        # Fragment
        self.shader['view_position'].value = tuple(camera.position.tolist())