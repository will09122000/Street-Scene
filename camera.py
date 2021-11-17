from math import sin, cos, radians
import pygame
import pyrr


class Camera:
    '''
    Base camera class
    '''
    def __init__(self,
            aspect_ratio: float,
            fov: float = 80.0,
            position: tuple[float, float, float] = (0.0, 0.0, 0.0),
            ortho: bool = False):

        self.ortho = ortho

        self.aspect_ratio = aspect_ratio
        self._fov = fov
        self.fov = fov # create projection matrix
        self.position = pyrr.Vector3(position)

        self.final_position = pyrr.Vector3(position)
        self.front = pyrr.Vector3([0.0, 0.0, -1.0])
        self.up    = pyrr.Vector3([0.0, 1.0, 0.0])
        self.right = pyrr.Vector3([1.0, 0.0, 0.0])

        self.yaw = -90
        self.pitch = 0

    def get_view_matrix(self):
        return pyrr.matrix44.create_look_at(self.final_position, self.final_position + self.front, self.up)

    def update_vectors(self):
        front = pyrr.Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))

        self.front = pyrr.vector.normalise(front)
        self.right = pyrr.vector.normalise(pyrr.vector3.cross(self.front, pyrr.Vector3([0.0, 1.0, 0.0])))
        self.up    = pyrr.vector.normalise(pyrr.vector3.cross(self.right, self.front))

    @property
    def fov(self):
        return self._fov

    @fov.setter
    def fov(self, new_fov):
        self._fov = new_fov
        if self.ortho:
            self.projection = pyrr.matrix44.create_orthogonal_projection_matrix(0, 1280, 720, 0, 0.1, 100)
        else:
            self.projection = pyrr.matrix44.create_perspective_projection_matrix(self._fov, self.aspect_ratio, 0.1, 1000)


class FirstPersonController(Camera):
    '''
    First-person controlled camera
    '''
    def __init__(self,
            aspect_ratio: float,
            fov: float = 80.0,
            position: tuple[float, float, float] = (0.0, 0.0, 0.0),
            movement_speed: float = 0.09):
        super().__init__(aspect_ratio, fov, position)

        self.velocity = pyrr.Vector3([0.0, 0.0, 0.0])
        self.jump_height = 0.2

        self.movement_speed = movement_speed
        self._default_movement_speed = movement_speed
        self.mouse_sensitivity = 0.17

    def process(self, scene):

        keys = pygame.key.get_pressed()
        rx, ry = pygame.mouse.get_rel()

        rx *= self.mouse_sensitivity
        ry *= self.mouse_sensitivity

        self.yaw += rx
        self.pitch -= ry

        if self.pitch > 90: self.pitch = 90
        if self.pitch < -90: self.pitch = -90

        self.update_vectors()

        # Controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scene.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene.running = False
                elif event.key == pygame.K_1:
                    scene.skybox = 'day' if scene.skybox == 'night' else 'night'

        if keys[pygame.K_w]:
            self.position += self.front * self.movement_speed

        if keys[pygame.K_s]:
            self.position -= self.front * self.movement_speed

        if keys[pygame.K_a]:
            self.position -= self.right * self.movement_speed

        if keys[pygame.K_d]:
            self.position += self.right * self.movement_speed

        self.final_position = self.position.copy()
