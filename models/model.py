import struct
import pygame
import pyrr

class Base_Model:
    """
    A class to represent a the main model used in the scene from which all other model types
    except the skybox are inherited from.

    Attributes
    ----------
    ctx:              moderngl.context | The ModernGL context exposing OpenGL features.
    shader:           moderngl.program | The compiled executable shader for this model.
    position:                    tuple | The position (XYZ) of the model in the scene.
    rotation:                    float | The angle in radians at which the model should be rotated
                                         about the Y-axis (Single float as there is no model that
                                         needs to be rotated about another axis). 
    scale:                       float | The scale at which the model is drawn comparted to the
                                         original model.
    position_matrix:     pyrr.matrix44 | The position of the model in the form of a 4x4 matrix.
    texture:                    string | The filepath to the texture image for this model.
    model_coords:                 list | The model's geometric vertices.
    texture_coords:               list | The model's texture vertices.
    norm_coords:                  list | The model's vertex normals.
    vao: moderngl.context.vertex_array | An array to store all of the values input to the vertex
                                         shader.
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

        self.ctx = ctx

        # Compile the base model shader.
        self.shader = ctx.program(vertex_shader = open('shaders/Base_Model_Vertex.glsl').read(),
                                  fragment_shader = open('shaders/Base_Model_Fragment.glsl').read())

        self.position = position
        self.rotation = pyrr.Vector4([0.0, rotation, 0.0, 1.0])
        self.scale = pyrr.Vector3([scale, scale, scale])

        self.position_matrix = pyrr.matrix44.create_from_translation(pyrr.Vector3(position))

        self.model_coords = vertices
        self.texture_coords = tex_coords
        self.norm_coords = norm_coords

        # Create VAO
        position = self.ctx.buffer(struct.pack(f'{len(self.model_coords)}f', *self.model_coords))
        texture_coords  = self.ctx.buffer(struct.pack(f'{len(self.texture_coords)}f', *self.texture_coords))
        normal = self.ctx.buffer(struct.pack(f'{len(self.norm_coords)}f', *self.norm_coords))

        self.vao = self.ctx.vertex_array( self.shader, [(position, '3f', 'position'),
                                                        (texture_coords,  '2f', 'texture_coord'),
                                                        (normal, '3f', 'normal')])

        self.create_texture(texture)

    def update(self, camera, lights):
        """Updates both vertex and fragment shader uniforms."""

        # Vertex
        self.shader['projection'].value = tuple(camera.projection.flatten())
        self.shader['model'].value      = tuple(self.position_matrix.flatten())
        self.shader['view'].value       = tuple(camera.get_view_matrix().flatten())
        self.shader['scale'].value      = tuple(self.scale.tolist())

        # Fragment
        self.shader['view_position'].value  = tuple(camera.position.tolist())
        self.shader['num_lights'].value     = len(lights)
        self.shader['light_position'].value = [tuple(light.position.tolist()) for light in lights]
        self.shader['colour'].value          = [light.colour for light in lights]
        self.shader['ambient'].value        = [light.ambient for light in lights]
        self.shader['diffuse'].value        = [light.diffuse for light in lights]
        self.shader['specular'].value       = [light.specular for light in lights]
        self.shader['attenuation'].value    = [light.attenuation for light in lights]

    def create_texture(self, texture):
        """Creates a texture object from the image provided."""

        image = pygame.image.load(texture)

        self.texture = self.ctx.texture(image.get_size(), 3,
                                        pygame.image.tostring(image, 'RGB', True))

        self.texture.build_mipmaps()

    def render(self):
        """Render the model."""

        self.texture.use(location=0)
        self.vao.render()

    def rotate(self):
        """Rotate the model about the y-axis."""

        rotation_matrix = pyrr.matrix44.create_from_y_rotation(self.rotation[1])
        self.position_matrix = pyrr.matrix44.multiply(rotation_matrix, self.position_matrix)
