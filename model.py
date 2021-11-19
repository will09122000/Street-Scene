import struct
import pygame
import pyrr

class Base_Model:
    '''
    Base model class
    '''
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
        self.shader = ctx.program(vertex_shader = open('shaders/Base_Model_Vertex.glsl').read(),
                                  fragment_shader = open('shaders/Base_Model_Fragment.glsl').read())

        self.position = position
        self.rotation = pyrr.Vector4([0.0, rotation, 0.0, 1.0])
        self.scale = pyrr.Vector3([scale, scale, scale])

        self.position_matrix = pyrr.matrix44.create_from_translation(pyrr.Vector3(position))

        self.model_coords = vertices
        self.texture_coords = tex_coords
        self.norm_coords = norm_coords

        self.create_vao()

        self.surface = pygame.image.load(texture)

        self.surface = self.surface.convert((255, 65280, 16711680, 0))


        self.create_texture()

    def update(self, camera, lights):

        # Vertex
        self.shader['projection'].value = tuple(camera.projection.flatten())
        self.shader['model'].value      = tuple(self.position_matrix.flatten())
        self.shader['view'].value       = tuple(camera.get_view_matrix().flatten())
        self.shader['scale'].value      = tuple(self.scale.tolist())

        # Fragment
        self.shader['view_position'].value  = tuple(camera.position.tolist())
        self.shader['num_lights'].value     = len(lights)
        self.shader['light_position'].value = [tuple(light.position.tolist()) for light in lights]
        self.shader['color'].value          = [light.color for light in lights]
        self.shader['ambient'].value        = [light.ambient for light in lights]
        self.shader['diffuse'].value        = [light.diffuse for light in lights]
        self.shader['specular'].value       = [light.specular for light in lights]
        self.shader['attenuation'].value    = [light.attenuation for light in lights]

    def create_texture(self):
        self.texture = self.ctx.texture(self.surface.get_size(), 3,
                                        pygame.image.tostring(self.surface, 'RGB', True))

        self.texture.repeat_x = False
        self.texture.repeat_y = False

        self.texture.build_mipmaps()

    def update_texture(self):
        self.texture.write(pygame.image.tostring(self.surface, self.texture_format, True))
        self.texture.build_mipmaps()

    def create_vao(self):
        pos = self.ctx.buffer(struct.pack(f'{len(self.model_coords)}f', *self.model_coords))
        uv  = self.ctx.buffer(struct.pack(f'{len(self.texture_coords)}f', *self.texture_coords))
        nor = self.ctx.buffer(struct.pack(f'{len(self.norm_coords)}f', *self.norm_coords))

        self.vao = self.ctx.vertex_array( self.shader, [(pos, '3f', 'position'),
                                                        (uv,  '2f', 'texture_coord'),
                                                        (nor, '3f', 'normal')])

    def render(self, skybox=None):
        self.texture.use(location=0)
        if skybox: skybox.texture.use(location=1)

        self.vao.render()

    def rotate(self):
        rotation_matrix = pyrr.matrix44.create_from_y_rotation(self.rotation[1])
        self.position_matrix = pyrr.matrix44.multiply(rotation_matrix, self.position_matrix)
