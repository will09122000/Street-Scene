import struct

from model import Base_Model

class Enviro_Map_Model(Base_Model):
    """
    A class to represent a model that reflects the skybox texture.

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
        self.shader['projection'].value    = tuple(camera.projection.flatten())
        self.shader['model'].value         = tuple(self.position_matrix.flatten())
        self.shader['view'].value          = tuple(camera.get_view_matrix().flatten())
        self.shader['scale'].value         = tuple(self.scale.tolist())
        self.shader['view_position'].value = tuple(camera.position.tolist())