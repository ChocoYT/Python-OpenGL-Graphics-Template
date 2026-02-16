import pygame
import numpy as np

from config import config

# Config Setup
SCREEN_WIDTH  = int(config['screen']['width'])
SCREEN_HEIGHT = int(config['screen']['height'])

Z_NEAR = float(config['screen']['zNear'])
Z_FAR  = float(config['screen']['zFar'])

class Camera():
    def __init__(self) -> None:
        self.position = pygame.Vector3(0.0, 0.0, 0.0)
        self.rotation = pygame.Vector3(0.0, 0.0, 0.0)

        self.objRot_x, self.objrot_y, self.objrot_z = 0.0, 0.0, 0.0
        
        self.zNear = Z_NEAR
        self.zFar  = Z_FAR
        
        self.front      = pygame.Vector3(0.0, 0.0, -1.0)
        self.up         = pygame.Vector3(0.0, 1.0,  0.0)
        self.look_vector = pygame.Vector3(0.0, 0.0, -1.0)

        self.move_speed   = 0.1
        self.rotate_speed = 1
        self.sensitivity = 0.15

    def update(self) -> None:
        keys_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_rel = pygame.mouse.get_rel()

        # Rotate Based on Key Presses
        key_rotate_vector = pygame.Vector3(
            int(keys_pressed[pygame.K_UP])    - int(keys_pressed[pygame.K_DOWN]),
            int(keys_pressed[pygame.K_RIGHT]) - int(keys_pressed[pygame.K_LEFT]),
            int(keys_pressed[pygame.K_z])     - int(keys_pressed[pygame.K_z]),
        )
        if key_rotate_vector.length_squared() > 1.0:
            key_rotate_vector.normalize()

        # Rotate Based on Mouse Movement
        mouse_rotate_vector = pygame.Vector3(0.0, 0.0, 0.0)
        if mouse_pressed[2]:
            mouse_rotate_vector = pygame.Vector3(
                mouse_rel[1] * self.sensitivity,
                mouse_rel[0] * self.sensitivity,
                0.0
            )
            if mouse_rotate_vector.length_squared() > 1.0:
                mouse_rotate_vector.normalize()

        self.look_vector = self.rotation.copy()
        if self.look_vector.length_squared() > 1:
            self.look_vector.normalize()

        self.rotate(self.look_vector)
        
        if self.front.length() > 1:
            self.front.normalize()
        
        self.up = self.front.cross(pygame.Vector3(0.0, 1, 0.0)).cross(self.front)

        # Moves Camera
        self.move()

    def move(self) -> None:
        keys_pressed = pygame.key.get_pressed()
        
        move_x = int(keys_pressed[pygame.K_d]) - int(keys_pressed[pygame.K_a])
        move_y = int(keys_pressed[pygame.K_q]) - int(keys_pressed[pygame.K_e])
        move_z = int(keys_pressed[pygame.K_w]) - int(keys_pressed[pygame.K_s])

        move_vector = pygame.Vector3(move_x, move_y, move_z)
        if move_vector.length() > 1:
            move_vector.normalize()
        
        # Calculates movement
        if move_vector.x != 0.0:
            self.position.x += 

        if vector.y != 0.0:
            self.move_x += vector.y * self.yDirCos * self.zDirSin
            self.move_y += vector.y * self.x_dirCos * self.zDirCos
            self.move_z += vector.y * self.x_dirSin * self.yDirCos

        if vector.z != 0.0:
            self.move_x += vector.z * self.yDirSin * self.zDirCos
            self.move_y -= vector.z * self.x_dirSin * self.zDirCos
            self.move_z -= vector.z * self.x_dirCos * self.yDirCos

        self.position += move_vector * self.move_speed

    def rotate(self, vector: pygame.Vector3) -> None:
        self.rotation += vector * self.rotate_speed

        self.rotation.x %= 360
        self.rotation.y %= 360
        self.rotation.z %= 360
