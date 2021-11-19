import pyrr
import struct
import PIL.Image
import numpy as np

from objparser import parse

class Skybox:
    def __init__(self, ctx, imageList, width, height):
        self.ctx = ctx

        objfile = parse('assets/models/cube.obj')

        self.shader = ctx.program(vertex_shader = open('shaders/Skybox_Vertex.glsl').read(),
                                  fragment_shader = open('shaders/Skybox_Fragment.glsl').read())

        self.position_matrix = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))

        self.model_coords = objfile.vertices
        self.texture_coords = objfile.uv_coords
        self.norm_coords = objfile.vertex_normals

        self.texture = self.create_skybox(imageList, width, height)

        self.create_vao()

    def create_skybox(self, imageList, width, height):
        dataList = []
        for filename in imageList:
            image = PIL.Image.open(filename)
            if width != image.size[0] or height != image.size[1]:
                raise ValueError(f"image size mismatch: {image.size[0]}x{image.size[1]}")
            
            dataList.append(list(image.getdata()))

        image_data = np.array(dataList, np.uint8)

        return self.ctx.texture_cube((width, height), 4, image_data)

    def update(self, camera):
        self.shader['projection'].value = tuple(camera.projection.flatten())
        viewmatrix = camera.get_view_matrix()

        viewmatrix[3][0] = 0
        viewmatrix[3][1] = 0
        viewmatrix[3][2] = 0
        self.shader['view'].value = tuple(viewmatrix.flatten())


    def render(self):
        self.texture.use()
        self.vao.render()

    def create_vao(self):
        pos = self.ctx.buffer(struct.pack(f'{len(self.model_coords)}f', *self.model_coords))

        self.vao = self.ctx.vertex_array(self.shader, [(pos, '3f', 'position')])

