import time
import random
import pygame
import moderngl
from numpy import pi
import numpy
import pyrr
import PIL.Image

from model import Skybox, _compile_programs
from light import LampPostLight, Light
from camera import FirstPersonController
from ui import Image, Text

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

        self.camera = FirstPersonController(width / height)
        self.camera.noclip = True

        self.models = []
        self.lights = []

        _compile_programs(self.ctx)

        self.skybox = create_skybox(self.ctx,
                                           ['assets/skybox/night/right.png',
                                            'assets/skybox/night/left.png',
                                            'assets/skybox/night/top.png',
                                            'assets/skybox/night/bottom.png',
                                            'assets/skybox/night/back.png',
                                            'assets/skybox/night/front.png'],
                                            1024, 1024)


    def add_models(self, models):
        self.models = models

    def add_lighting(self):
        for model in self.models:
            if model.__class__.__name__ == 'LightModel':
                self.lights.append(LampPostLight(model.position))

    def draw(self):
        self.clock.tick(60)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False


        keys = pygame.key.get_pressed()
        mx, my = pygame.mouse.get_pos()
        rx, ry = pygame.mouse.get_rel()
        ry *= -1

        self.camera.process(rx, ry, events, keys)

        self.ctx.screen.use()
        self.ctx.screen.clear()

        self.ctx.disable(moderngl.DEPTH_TEST)
        self.ctx.front_face = 'cw'
        self.skybox.update(self.camera)
        self.skybox.render()
        self.ctx.front_face = 'ccw'
        self.ctx.enable(moderngl.DEPTH_TEST)

        for model in self.models:
            if model.__class__.__name__ == 'LightModel':
                model.update(self.camera)
            else:
                model.update(self.camera, self.lights)

            if model.__class__.__name__ == 'DynamicModel':
                model.translate()
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