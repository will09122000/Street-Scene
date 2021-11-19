import time
import random
import pygame
import moderngl
from numpy import pi
import numpy
import pyrr
import PIL.Image

from model import Skybox, compile_shaders
from light import LampPostLight, WindowLight, FloodLight
from camera import Camera

def create_skybox(ctx, imageList, width, height):

    dataList = []
    for filename in imageList:
        image = PIL.Image.open(filename)
        if width != image.size[0] or height != image.size[1]:
            raise ValueError(f"image size mismatch: {image.size[0]}x{image.size[1]}")
        
        dataList.append(list(image.getdata()))

    image_data = numpy.array(dataList, numpy.uint8)

    return Skybox(ctx, ctx.texture_cube((width, height), 4, image_data))


class Scene:
    def __init__(self, width, height):

        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 8)

        self.window = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        # These two lines creates a 'virtual mouse' so you can move it freely
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('Street Scene')

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)
        self.ctx.multisample = True

        self.camera = Camera(width / height)
        self.camera.noclip = True

        self.models = []
        self.lights = []

        compile_shaders(self.ctx)

        self.skybox_day = create_skybox(self.ctx,
                                        ['assets/skybox/day/right.png',
                                        'assets/skybox/day/left.png',
                                        'assets/skybox/day/top.png',
                                        'assets/skybox/day/bottom.png',
                                        'assets/skybox/day/back.png',
                                        'assets/skybox/day/front.png'],
                                        1024, 1024)

        self.skybox_night = create_skybox(self.ctx,
                                        ['assets/skybox/night/right.png',
                                        'assets/skybox/night/left.png',
                                        'assets/skybox/night/top.png',
                                        'assets/skybox/night/bottom.png',
                                        'assets/skybox/night/back.png',
                                        'assets/skybox/night/front.png'],
                                        1024, 1024)
        self.skybox = 'night'

    def add_models(self, models):
        self.models = models

        for model in models:
            model.rotate()

    def add_lighting(self):
        for model in self.models:
            if model.__class__.__name__ == 'LightModel':
                if model.light_type == 'lampPost':
                    self.lights.append(LampPostLight(model.position))
                elif model.light_type == 'window':
                    self.lights.append(WindowLight(model.position))
                elif model.light_type == 'floodLight':
                    self.lights.append(FloodLight(model.position))

    def draw(self):
        self.clock.tick(60)

        self.camera.update_view()
        self.camera.update_position(self)

        self.ctx.screen.use()
        self.ctx.screen.clear()

        self.ctx.disable(moderngl.DEPTH_TEST)
        self.ctx.front_face = 'cw'
        if self.skybox == 'night':
            self.skybox_night.update(self.camera)
            self.skybox_night.render()
        else:
            self.skybox_day.update(self.camera)
            self.skybox_day.render()
        self.ctx.front_face = 'ccw'
        self.ctx.enable(moderngl.DEPTH_TEST)

        for model in self.models:
            model.update(self.camera, self.lights)

            if model.__class__.__name__ == 'DynamicModel':
                if model.translation > 0:
                    model.translate()
                elif model.rotation[1] > 0:
                    model.rotate()

            model.render()

        pygame.display.flip()

    def run(self):
        '''
        Draws the scene in a loop until exit.
        '''
        # We have a classic program loop
        self.running = True

        while self.running:
            # otherwise, continue drawing
            self.draw()