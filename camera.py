import pygame
import pyrr
from math import radians, sin, cos

class Camera:
    """
    A class to represent the camera for which the scene is viewed through.

    Attributes
    ----------
    movement_sensitivity:  float | Defines how sensitive WASD key press movements are terms of the
                                   camera's velocity.
    mouse_sensitivity:     float | Defines how sensitive mouse movements in terms of the camera's
                                   projection.
    aspect_ratio:          float | Aspect Ratio of the window (screen width / screen height).
    fov:                   float | Field of view of the camera.
    position:       pyrr.Vector3 | The current position of the camera as a 3D vector.
    projection:      numpy.array | The perspective projection matrix of the camera.
    front:          pyrr.Vector3 | A 3D vector representing forward and backward directions.
    side:           pyrr.Vector3 | A 3D vector representing left and right directions.
    yaw:                   float | The relative angle from which the camera has rotated horizontally.
    pitch:                 float | The relative angle from which the camera has rotated vertically.
    """
    def __init__(self,
                 aspect_ratio,
                 fov                  = 90.0,
                 start_position       = (0.0, 5.0, 0.0),
                 movement_sensitivity = 0.2,
                 mouse_sensitivity    = 0.15):

        self.movement_sensitivity = movement_sensitivity
        self.mouse_sensitivity = mouse_sensitivity

        self.aspect_ratio = aspect_ratio
        self.fov = fov
        self.position = pyrr.Vector3(start_position)
        self.projection = pyrr.matrix44.create_perspective_projection_matrix(fovy   = self.fov,
                                                                             aspect = self.aspect_ratio,
                                                                             near   = 0.01,
                                                                             far    = 100)

        self.front = pyrr.Vector3([0.0, 0.0, -1.0])
        self.side = pyrr.Vector3([1.0, 0.0, 0.0])

        self.yaw = 0
        self.pitch = 0

    def get_view_matrix(self):
        """Returns the view matrix of the camera."""

        return pyrr.matrix44.create_look_at(eye    = self.position,
                                            target = self.position + self.front,
                                            up     = pyrr.Vector3([0.0, 1.0, 0.0]))

    def update_view(self):
        """Updates the view direction of the camera based on mouse input."""

        # Relative mouse movement.
        x_movement, y_movement = pygame.mouse.get_rel()

        self.yaw += x_movement * self.mouse_sensitivity
        self.pitch -= y_movement * self.mouse_sensitivity

        # Prevents the camera from looking past vertically up and down.
        if self.pitch > 89: self.pitch = 89
        if self.pitch < -89: self.pitch = -89

        x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        y = sin(radians(self.pitch))
        z = sin(radians(self.yaw)) * cos(radians(self.pitch))

        self.front = pyrr.vector.normalise(pyrr.Vector3([x, y, z]))
        self.side = pyrr.vector.normalise(pyrr.vector3.cross(self.front,
                                                             pyrr.Vector3([0.0, 1.0, 0.0])))

    def update_position(self, scene):
        """
        Updates the camera's position and scene controls based on keyboard input.
        """

        inputs = pygame.key.get_pressed()

        # Single key press events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scene.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    scene.running = False
                elif event.key == pygame.K_1:
                    scene.skybox = 'day' if scene.skybox == 'night' else 'night'

        # Key press events that can be held.
        if inputs[pygame.K_w]:
            self.position += self.front * self.movement_sensitivity

        if inputs[pygame.K_s]:
            self.position -= self.front * self.movement_sensitivity

        if inputs[pygame.K_a]:
            self.position -= self.side * self.movement_sensitivity

        if inputs[pygame.K_d]:
            self.position += self.side * self.movement_sensitivity
