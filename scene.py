import time
import random
import pygame
import moderngl
from numpy import pi
import pyrr

from model import load_obj, create_skybox, _compile_programs
from light import BasicLight
from camera import FirstPersonController
from ui import Image, Text

class Scene:
    def __init__(self, width=1280, height=720):

        WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
        self.window_size = (width, height)

        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 8)
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        # These two lines creates a 'virtual mouse' so you can move it freely
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('Street Scene')

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)
        self.ctx.multisample = True

        self.camera = FirstPersonController(WINDOW_WIDTH / WINDOW_HEIGHT)
        self.camera.noclip = True

        self.light_source = BasicLight()
        self.light_source.ambient_intensity = 0.1

        self.models = []

        self.top = pygame.image.load('assets/skybox/generic_top.png').convert((255, 65280, 16711680, 0))
        self.bottom = pygame.image.load('assets/skybox/generic_bottom.png').convert((255, 65280, 16711680, 0))
        self.left = pygame.image.load('assets/skybox/generic_left.png').convert((255, 65280, 16711680, 0))
        self.front = pygame.image.load('assets/skybox/generic_front.png').convert((255, 65280, 16711680, 0))
        self.right = pygame.image.load('assets/skybox/generic_right.png').convert((255, 65280, 16711680, 0))
        self.back = pygame.image.load('assets/skybox/generic_back.png').convert((255, 65280, 16711680, 0))

        self.data = self.right.get_view('1').raw + self.left.get_view('1').raw + self.top.get_view('1').raw + self.bottom.get_view('1').raw + self.front.get_view('1').raw + self.back.get_view('1').raw

        self.cubemap = self.ctx.texture_cube((900, 900), 3,self. data)
        _compile_programs(self.ctx)
        self.skybox = create_skybox(self.ctx, self.cubemap)

    def add_models(self, models):
        self.models = models

    def draw(self):
        self.clock.tick(120)

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
            model.update(self.camera, self.light_source)
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