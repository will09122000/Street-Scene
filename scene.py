import pygame
import moderngl

from light import LampPostLight, WindowLight, FloodLight, GreenLight, RedLight
from camera import Camera
from models.skybox import Skybox

class Scene:
    """
    This is the main class for drawing the OpenGL street scene.

    Attributes
    ----------
    width: int  | The display width in pixels.
    height: int | The display height in pixels.
    """
    def __init__(self, width, height):

        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 8)

        self.window = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        # Disables the cursor.
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        pygame.display.set_caption('Street Scene')

        # Creates ModernGL context.
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)
        self.ctx.multisample = True

        # Initialise the scene's camera to view the scene.
        self.camera = Camera(width / height)
        self.camera.noclip = True

        self.models = []
        self.lights = []

        # Creates day and night skyboxes.
        self.skybox_day = Skybox(self.ctx, 1024, 1024,
                                 ['assets/skybox/day/right.png',
                                 'assets/skybox/day/left.png',
                                 'assets/skybox/day/top.png',
                                 'assets/skybox/day/bottom.png',
                                 'assets/skybox/day/back.png',
                                 'assets/skybox/day/front.png'])

        self.skybox_night = Skybox(self.ctx, 1024, 1024,
                                   ['assets/skybox/night/right.png',
                                   'assets/skybox/night/left.png',
                                   'assets/skybox/night/top.png',
                                   'assets/skybox/night/bottom.png',
                                   'assets/skybox/night/back.png',
                                   'assets/skybox/night/front.png'])
        self.skybox = 'night'

    def add_models(self, models):
        """Adds models to the scene."""

        self.models = models

        for model in models:
            model.rotate()

    def add_lighting(self):
        """Adds lighting in the same position as light models."""

        for model in self.models:
            if model.__class__.__name__ == 'Light_Model':
                if model.light_type == 'lampPost':
                    self.lights.append(LampPostLight(model.position))
                elif model.light_type == 'window':
                    self.lights.append(WindowLight(model.position))
                elif model.light_type == 'floodLight':
                    self.lights.append(FloodLight(model.position))
                elif model.light_type == 'greenLight':
                    self.lights.append(GreenLight(model.position))
                elif model.light_type == 'redLight':
                    self.lights.append(RedLight(model.position))

    def draw(self):
        """Draws the scene."""

        self.clock.tick(60)

        # Updates the camera's view and position controlled by user inputs.
        self.camera.update_view()
        self.camera.update_position(self)

        # Clear the screen.
        self.ctx.screen.use()
        self.ctx.screen.clear()

        # Draw the skybox.
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

        # Update the position of dynamic models and render each model.
        for model in self.models:
            model.update(self.camera, self.lights)

            if model.__class__.__name__ == 'Dynamic_Model':
                if sum(model.translation) > 0:
                    model.translate()
                elif model.rotation[1] > 0:
                    model.rotate()

            model.render()

        pygame.display.flip()

    def run(self):
        """Draws the scene in a loop until exit."""

        self.running = True

        # Keep drawing the scene while running is true.
        while self.running:
            self.draw()
