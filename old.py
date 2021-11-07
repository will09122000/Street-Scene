import time
import random
import pygame
import moderngl
from numpy import pi
import pyrr

from model import load_obj, create_skybox
from light import BasicLight
from camera import FirstPersonController
from ui import Image, Text


pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 8)
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()
# These two lines creates a 'virtual mouse' so you can move it freely
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
pygame.display.set_caption('Street Scene')
running = True

ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)
ctx.multisample = True

camera = FirstPersonController(WINDOW_WIDTH / WINDOW_HEIGHT)
camera.noclip = True

light_source = BasicLight()
light_source.ambient_intensity = 0.6


obj = load_obj(ctx, 'assets/models/obamium.obj', 'assets/textures/obamium.png', (-4, -3.5, -5), flip_texture=True)

obj3 = load_obj(ctx, 'assets/models/cube.obj', 'assets/textures/green.png', (3, -3.4, 4))
obj3.rotation.x = 0.7
obj3.rotation.z = -0.2

obj4 = load_obj(ctx, 'assets/models/sphere.obj', 'assets/textures/white.png', (1.0, 0.0, 1.0), unlit=True)

obj6 = load_obj(ctx, 'assets/models/wolf.obj', 'assets/textures/white.png', (9, -5.2, 6))
obj6.rotation.y = 1.5

car = load_obj(ctx, 'assets/models/car0.obj', 'assets/textures/car0.png', (2, -5.2, 6))

floor = load_obj(ctx, 'assets/models/floor.obj', 'assets/textures/floor.png', (2, -5.2, 6))

top = pygame.image.load('assets/skybox/generic_top.png').convert((255, 65280, 16711680, 0))
bottom = pygame.image.load('assets/skybox/generic_bottom.png').convert((255, 65280, 16711680, 0))
left = pygame.image.load('assets/skybox/generic_left.png').convert((255, 65280, 16711680, 0))
front = pygame.image.load('assets/skybox/generic_front.png').convert((255, 65280, 16711680, 0))
right = pygame.image.load('assets/skybox/generic_right.png').convert((255, 65280, 16711680, 0))
back = pygame.image.load('assets/skybox/generic_back.png').convert((255, 65280, 16711680, 0))

data = right.get_view('1').raw + left.get_view('1').raw + top.get_view('1').raw + bottom.get_view('1').raw + front.get_view('1').raw + back.get_view('1').raw

cubemap = ctx.texture_cube((900, 900), 3, data)

skybox = create_skybox(ctx, cubemap)

while running:
    clock.tick(120)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


    keys = pygame.key.get_pressed()
    mx, my = pygame.mouse.get_pos()
    rx, ry = pygame.mouse.get_rel()
    ry *= -1

    camera.process(rx, ry, events, keys)

    ctx.screen.use()
    ctx.screen.clear()

    ctx.disable(moderngl.DEPTH_TEST)
    ctx.front_face = 'cw'
    skybox.update(camera)
    skybox.render()
    ctx.front_face = 'ccw'
    ctx.enable(moderngl.DEPTH_TEST)

    obj.update(camera, light_source)

    obj3.update(camera, light_source)
    obj3.render(skybox)

    obj4.update(camera)
    obj4.render()

    obj6.update(camera, light_source)
    obj6.render()

    car.update(camera, light_source)
    car.render()

    floor.update(camera, light_source)
    floor.render()

    pygame.display.flip()

pygame.quit()
