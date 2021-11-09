from typing import Union

from pathlib import Path
import struct
import pygame
import moderngl
import pyrr
import numpy as np

from objparser import parse
from camera import Camera
from light import BasicLight

map_edge = 24

PROGRAMS = {}
def _compile_programs(ctx: moderngl.Context, force: bool = True):
    '''
    This function caches shader programs for models to use

    'force' keyword recompiles all shaders
    '''
    if len(PROGRAMS) == 0 or force:
        PROGRAMS.clear()
        PROGRAMS['default'] = ctx.program(
            vertex_shader   = open('shaders/default.vsh').read(),
            fragment_shader = open('shaders/default.fsh').read()
        )

        PROGRAMS['unlit'] = ctx.program(
            vertex_shader   = open('shaders/unlit.vsh').read(),
            fragment_shader = open('shaders/unlit.fsh').read()
        )

        PROGRAMS['static'] = ctx.program(
            vertex_shader   = open('shaders/static.vsh').read(),
            fragment_shader = open('shaders/static.fsh').read()
        )

        PROGRAMS['skybox'] = ctx.program(
            vertex_shader   = open('shaders/skybox.vsh').read(),
            fragment_shader = open('shaders/skybox.fsh').read()
        )

        PROGRAMS['shadow'] = ctx.program(
            vertex_shader   = open('shaders/shadow.vsh').read(),
            fragment_shader = open('shaders/shadow.fsh').read()
        )

        PROGRAMS['shadowmap'] = ctx.program(
            vertex_shader   = open('shaders/shadowmap.vsh').read(),
            fragment_shader = open('shaders/shadowmap.fsh').read()
        )

        PROGRAMS['debug'] = ctx.program(
            vertex_shader   = open('shaders/debug.vsh').read(),
            fragment_shader = open('shaders/debug.fsh').read()
        )


class BaseModel:
    '''
    Base model class
    '''
    def __init__(self,
            ctx: moderngl.Context,
            position: tuple[float, float, float],
            texture: str,
            texture_format: str,
            vertices: list[tuple[float, float, float]],
            tex_coords: list[tuple[float, float]],
            norm_coords: list[tuple[float, float, float]],
            flip_texture: bool,
            rotation: float = 0.0,
            scale: float = 1.0,
            from_filepath: bool = True,
            build_mipmaps: bool = True):

        self.ctx = ctx
        self.program = PROGRAMS['default']
        self.shadowmap_program = PROGRAMS['shadowmap']
        self.debug_program = PROGRAMS['debug']

        self.position = position
        self.rotation = pyrr.Vector3([0.0, rotation, 0.0])
        self.scale = pyrr.Vector3([scale, scale, scale])

        self.texture_format = texture_format
        self.build_mipmaps = build_mipmaps

        self.pos_matrix = pyrr.matrix44.create_from_translation(pyrr.Vector3(position))

        self.model_coords = vertices
        self.texture_coords = tex_coords
        self.norm_coords = norm_coords

        self.create_vao()

        if from_filepath:
            surf = pygame.image.load(texture)
            if flip_texture: surf = pygame.transform.flip(surf, False, True)
            self.surface = surf
        else:
            self.surface = pygame.Surface((1, 1))

        if texture_format == 'RGB':
            self.surface = self.surface.convert((255, 65280, 16711680, 0))
        elif texture_format == 'RGBA':
            self.surface = self.surface.convert_alpha()

        self.create_texture()

    def create_texture(self):
        self.texture = self.ctx.texture(
            self.surface.get_size(),
            len(self.texture_format),
            pygame.image.tostring(self.surface, self.texture_format, True)
        )

        self.texture.repeat_x = False
        self.texture.repeat_y = False

        #self.texture.anisotropy = 16
        if self.build_mipmaps: self.texture.build_mipmaps()

    def update_texture(self):
        self.texture.write(pygame.image.tostring(self.surface, self.texture_format, True))
        if self.build_mipmaps: self.texture.build_mipmaps()

    def create_vao(self):
        pos = self.ctx.buffer(struct.pack(f'{len(self.model_coords)}f', *self.model_coords))
        uv  = self.ctx.buffer(struct.pack(f'{len(self.texture_coords)}f', *self.texture_coords))
        nor = self.ctx.buffer(struct.pack(f'{len(self.norm_coords)}f', *self.norm_coords))

        if self.program == PROGRAMS['unlit']:
            self.vao = self.ctx.vertex_array(
                self.program, [
                    (pos, '3f', 'a_position'),
                    (uv,  '2f', 'a_texture')
                ])
        else:
            self.vao = self.ctx.vertex_array(
                self.program, [
                    (pos, '3f', 'a_position'),
                    (uv,  '2f', 'a_texture'),
                    (nor, '3f', 'a_normal')
                ])

        self.shadow_vao = self.ctx.vertex_array(
            self.shadowmap_program, [
                (pos, '3f', 'a_position')
            ])

        self.debug_vao = self.ctx.vertex_array(
            self.debug_program, [
                (pos, '3f', 'a_position'),
                (uv,  '2f', 'a_texture'),
                (pos, '3f', 'a_position')
            ])

    def update(self, camera: Camera, lights):

        self.program['projection'].value = tuple(camera.projection.flatten())
        self.program['view'].value = tuple(camera.get_view_matrix().flatten())
        self.program['model'].value = tuple(self.pos_matrix.flatten())
        self.program['angle'].value = tuple(self.rotation.tolist())
        self.program['scale'].value = tuple(self.scale.tolist())

        self.program['viewpos'].value = tuple(camera.final_position.tolist())
        #self.program['lightpos'].value = tuple(lights[0].position.tolist())
        #self.program['lightpos2'].value = tuple(lights[1].position.tolist())


        self.program['color'].value = lights[0].color
        self.program['ambient_intensity'].value = lights[0].ambient_intensity
        #self.program['diffuse_intensity'].value = lights[0].diffuse_intensity
        #self.program['specular_intensity'].value = lights[0].specular_intensity
        #self.program['specular_power'].value = lights[0].specular_power

    def update_shadow(self, camera: Camera, camera2: Camera, lights):
        self.program['projection'].value = tuple(camera.projection.flatten())
        self.program['view'].value = tuple(camera.get_view_matrix().flatten())
        self.program['model'].value = tuple(self.pos_matrix.flatten())
        self.program['lightprojection'].value = tuple(camera2.projection.flatten())
        self.program['lightview'].value = tuple(camera2.get_view_matrix().flatten())
        self.program['angle'].value = tuple(self.rotation.tolist())
        self.program['scale'].value = tuple(self.scale.tolist())

        self.program['viewpos'].value = tuple(camera.final_position.tolist())
        self.program['lightpos'].value = tuple(lights[0].position.tolist())

        self.program['color'].value = lights[0].color
        self.program['ambient_intensity'].value = lights[0].ambient_intensity
        self.program['diffuse_intensity'].value = lights[0].diffuse_intensity
        self.program['specular_intensity'].value = lights[0].specular_intensity
        self.program['specular_power'].value = lights[0].specular_power

    def update_shadowmap(self, camera: Camera):
        self.shadowmap_program['projection'].value = tuple(camera.projection.flatten())
        self.shadowmap_program['view'].value = tuple(camera.get_view_matrix().flatten())
        self.shadowmap_program['model'].value = tuple(self.pos_matrix.flatten())

    def update_debug(self, camera: Camera):
        self.debug_program['projection'].value = tuple(camera.projection.flatten())
        self.debug_program['view'].value = tuple(camera.get_view_matrix().flatten())
        self.debug_program['model'].value = tuple(self.pos_matrix.flatten())

    def render(self, skybox=None):
        self.texture.use(location=0)
        if skybox: skybox.texture.use(location=1)

        self.vao.render()

    def render_shadow(self):
        self.shadow_vao.render()

    def render_debug(self):
        self.debug_vao.render()

class DynamicModel(BaseModel):
    def __init__(self,
        ctx: moderngl.Context,
        position: tuple[float, float, float],
        texture: str,
        texture_format: str,
        vertices: list[tuple[float, float, float]],
        tex_coords: list[tuple[float, float]],
        norm_coords: list[tuple[float, float, float]],
        flip_texture: bool,
        rotation: float = 0.0,
        scale: float = 1.0,
        translation: float = 0.0,
        direction: int = 1,
        from_filepath: bool = True,
        build_mipmaps: bool = True):

        super().__init__(
            ctx,
            position,
            texture,
            texture_format,
            vertices,
            tex_coords,
            norm_coords,
            flip_texture,
            rotation,
            scale,
            from_filepath,
            build_mipmaps)

        self.translation = translation
        self.direction = direction

    def translate(self):
        if np.abs(self.pos_matrix).max() > map_edge:
            translation_matrix = pyrr.matrix44.create_from_translation([map_edge * self.direction * 2, 0, 0])
            self.pos_matrix = pyrr.matrix44.multiply(translation_matrix, self.pos_matrix)
        else:
            translation_matrix = pyrr.matrix44.create_from_translation([self.translation * -self.direction, 0, 0])
            self.pos_matrix = pyrr.matrix44.multiply(translation_matrix, self.pos_matrix)

class UnlitModel(BaseModel):
    '''
    Unlit model doesn't get effected by any light source
    '''
    def __init__(self,
            ctx: moderngl.Context,
            position: tuple[float, float, float],
            texture: str,
            texture_format: str,
            vertices: list[tuple[float, float, float]],
            tex_coords: list[tuple[float, float]],
            norm_coords: list[tuple[float, float, float]],
            flip_texture: bool,
            from_filepath: bool = True,
            build_mipmaps: bool = True):

        super().__init__(
            ctx,
            position,
            texture,
            texture_format,
            vertices,
            tex_coords,
            norm_coords,
            flip_texture,
            from_filepath,
            build_mipmaps)

        self.program = PROGRAMS['unlit']
        self.create_vao()

    def update(self, camera: Camera):
        self.program['projection'].value = tuple(camera.projection.flatten())
        self.program['view'].value = tuple(camera.get_view_matrix().flatten())
        self.program['model'].value = tuple(self.pos_matrix.flatten())
        self.program['angle'].value = tuple(self.rotation.tolist())
        self.program['scale'].value = tuple(self.scale.tolist())


class StaticModel(BaseModel):
    '''
    Static model doesn't get effected by camera view
    mostly meant to be used as UI objects
    '''
    def __init__(self,
            ctx: moderngl.Context,
            position: tuple[float, float, float],
            texture: str,
            texture_format: str,
            vertices: list[tuple[float, float, float]],
            tex_coords: list[tuple[float, float]],
            flip_texture: bool,
            from_filepath: bool = True,
            build_mipmaps: bool = False):
        
        super().__init__(
            ctx,
            position,
            texture,
            texture_format,
            vertices,
            tex_coords,
            [0],
            flip_texture,
            from_filepath,
            build_mipmaps)

        self.program = PROGRAMS['static']
        self.create_vao()

    def create_vao(self):
        pos = self.ctx.buffer(struct.pack(f'{len(self.model_coords)}f', *self.model_coords))
        uv  = self.ctx.buffer(struct.pack(f'{len(self.texture_coords)}f', *self.texture_coords))

        self.vao = self.ctx.vertex_array(
            self.program, [
                (pos, '3f', 'a_position'),
                (uv,  '2f', 'a_texture'),
            ])

class Skybox:
    def __init__(self, ctx, texture):
        self.ctx = ctx

        objfile = parse('assets/models/cube.obj')

        self.program = PROGRAMS['skybox']

        self.rotation = pyrr.Vector3([0.0, 0.0, 0.0])
        self.scale = pyrr.Vector3([1.0, 1.0, 1.0])

        self.texture_format = 'rgb'

        self.pos_matrix = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))

        self.model_coords = objfile.vertices
        self.texture_coords = objfile.uv_coords
        self.norm_coords = objfile.vertex_normals

        self.texture = texture

        #self.texture.anisotropy = 4

        self.create_vao()

    def update(self, camera: Camera):
        self.program['projection'].value = tuple(camera.projection.flatten())
        viewmatrix = camera.get_view_matrix()

        viewmatrix[3][0] = 0
        viewmatrix[3][1] = 0
        viewmatrix[3][2] = 0
        self.program['view'].value = tuple(viewmatrix.flatten())
        #self.program['model'].value = tuple(pyrr.matrix44.create_from_translation(camera.position).flatten())#tuple(self.pos_matrix.flatten())

        #self.program['viewpos'].value = tuple(camera.position.tolist())

    def render(self):
        self.texture.use()
        self.vao.render()

    def create_vao(self):
        pos = self.ctx.buffer(struct.pack(f'{len(self.model_coords)}f', *self.model_coords))
        uv  = self.ctx.buffer(struct.pack(f'{len(self.texture_coords)}f', *self.texture_coords))
        nor = self.ctx.buffer(struct.pack(f'{len(self.norm_coords)}f', *self.norm_coords))

        self.vao = self.ctx.vertex_array(
            self.program, [
                (pos, '3f', 'a_position'),
            ])

def load_obj(
        ctx: moderngl.Context,
        obj_filepath: Union[Path, str],
        texture_filepath: Union[Path, str],
        position: tuple[float, float, float],
        rotation: float = 0.0,
        scale: float = 1.0,
        translation: float = 0.0,
        direction: int = 1,
        texture_format: str = 'RGB',
        flip_texture: bool = False,
        unlit: bool = False) -> Union[BaseModel, UnlitModel]:

    objfile = parse(obj_filepath)
    
    if unlit:
        return UnlitModel(
            ctx,
            position,
            texture_filepath,
            texture_format,
            objfile.vertices,
            objfile.uv_coords,
            objfile.vertex_normals,
            flip_texture)
    elif translation != 0.0:
        return DynamicModel(
            ctx,
            position,
            texture_filepath,
            texture_format,
            objfile.vertices,
            objfile.uv_coords,
            objfile.vertex_normals,
            flip_texture,
            rotation,
            scale,
            translation,
            direction)
    else:
        return BaseModel(
            ctx,
            position,
            texture_filepath,
            texture_format,
            objfile.vertices,
            objfile.uv_coords,
            objfile.vertex_normals,
            flip_texture,
            rotation,
            scale)


def create_skybox(ctx, texture):
    return Skybox(ctx, texture)