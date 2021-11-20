import struct

from model import Base_Model

class Light_Model(Base_Model):
    """
    A class to represent a model that is not affected by any light source. Used in conjunction
    with a light object to give the appearance of a light.

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
        self.shader['projection'].value = tuple(camera.projection.flatten())
        self.shader['model'].value      = tuple(self.position_matrix.flatten())
        self.shader['view'].value       = tuple(camera.get_view_matrix().flatten())
        self.shader['scale'].value      = tuple(self.scale.tolist())

