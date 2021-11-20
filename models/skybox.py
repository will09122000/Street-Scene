import pyrr
import struct
import PIL.Image
import numpy as np

from object_reader import read_obj

class Skybox:
    """
    A class to represent the cube surrounding the scene acting as the sky.

    Attributes
    ----------
    ctx:              moderngl.context | The ModernGL context exposing OpenGL features.
    shader:           moderngl.program | The compiled executable shader for this model.
    position_matrix:     pyrr.matrix44 | The position of the model in the form of a 4x4 matrix.
    texture:                    string | The filepath to the texture image for this model.
    model_coords:                 list | The model's geometric vertices.
    texture_coords:               list | The model's texture vertices.
    norm_coords:                  list | The model's vertex normals.
    vao: moderngl.context.vertex_array | An array to store all of the values input to the vertex
                                         shader.
    """
    def __init__(self, ctx, width, height, image_list):
        self.ctx = ctx

        obj_file = read_obj('assets/models/cube.obj')

        self.shader = ctx.program(vertex_shader = open('shaders/Skybox_Vertex.glsl').read(),
                                  fragment_shader = open('shaders/Skybox_Fragment.glsl').read())

        self.model_coords = obj_file.vertices
        self.texture_coords = obj_file.uv_coords
        self.norm_coords = obj_file.vertex_normals

        self.position_matrix = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))

        self.texture = self.create_skybox(image_list, width, height)

        # Creates VAO
        position = self.ctx.buffer(struct.pack(f'{len(self.model_coords)}f', *self.model_coords))
        self.vao = self.ctx.vertex_array(self.shader, [(position, '3f', 'position')])

    def create_skybox(self, imageList, width, height):
        """Creates a texture cube from 6 images."""
        dataList = []
        for filename in imageList:
            image = PIL.Image.open(filename)
            if width != image.size[0] or height != image.size[1]:
                raise ValueError(f'Images are not of equal size: {image.size[0]}x{image.size[1]}.')
            dataList.append(list(image.getdata()))

        image_data = np.array(dataList, np.uint8)

        return self.ctx.texture_cube((width, height), 4, image_data)

    def update(self, camera):
        """Updates the vertex shader uniforms."""

        self.shader['projection'].value = tuple(camera.projection.flatten())

        view_matrix = camera.get_view_matrix()
        view_matrix[3][0] = 0
        view_matrix[3][1] = 0
        view_matrix[3][2] = 0
        self.shader['view'].value = tuple(view_matrix.flatten())

    def render(self):
        """Render the skybox."""
        self.texture.use()
        self.vao.render()
