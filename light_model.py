import struct

from model import Base_Model

class Light_Model(Base_Model):
    '''
    Unlit model doesn't get effected by any light source
    '''
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

        super().__init__(
            ctx,
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
        pos = self.ctx.buffer(struct.pack(f'{len(self.model_coords)}f', *self.model_coords))
        uv  = self.ctx.buffer(struct.pack(f'{len(self.texture_coords)}f', *self.texture_coords))

        self.vao = self.ctx.vertex_array(self.shader, [(pos, '3f', 'position'),
                                                       (uv,  '2f', 'texture_coord')])

    def update(self, camera, lights=None):
        self.shader['projection'].value = tuple(camera.projection.flatten())
        self.shader['model'].value      = tuple(self.position_matrix.flatten())
        self.shader['view'].value       = tuple(camera.get_view_matrix().flatten())
        self.shader['scale'].value      = tuple(self.scale.tolist())

