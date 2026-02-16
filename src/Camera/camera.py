import glfw
import glm

from Window.window import Window
from Camera import constants

class Camera:
    def __init__(
            self,
            position: glm.vec3 | None = None,
            rotation: glm.vec3 | None = None
        ) -> None:

        self.position = position if position else constants.DEFAULT_CAMERA_POSITION
        self.rotation = rotation if rotation else constants.DEFAULT_CAMERA_ROTATION
        
        self.fov  = constants.DEFAULT_CAMERA_FOV
        self.near = constants.DEFAULT_CAMERA_NEAR
        self.far  = constants.DEFAULT_CAMERA_FAR

        self.move_speed  = constants.DEFAULT_CAMERA_MOVE_SPEED
        self.look_speed  = constants.DEFAULT_CAMERA_LOOK_SPEED
        self.sensitivity = constants.DEFAULT_CAMERA_SENSITIVITY

        self.update_vectors()

    def update(self, window: Window, dt: float) -> None:
        self.rotate(window, dt)
        self.update_vectors()
        self.move(window, dt)

    def move(self, window: Window, dt: float) -> None:
        move_right = int(window.get_key_pressed(glfw.KEY_D)) - int(window.get_key_pressed(glfw.KEY_A))
        move_up    = int(window.get_key_pressed(glfw.KEY_Q)) - int(window.get_key_pressed(glfw.KEY_E))
        move_front = int(window.get_key_pressed(glfw.KEY_W)) - int(window.get_key_pressed(glfw.KEY_S))
        
        move_vector = glm.vec3(move_right, move_up, move_front)
        if glm.length(move_vector) > 1:  # type: ignore
            move_vector = glm.normalize(move_vector)
            
        move_vector *= self.move_speed * dt

        if move_front or move_right or move_up:
            self.position += self.right * move_vector.x + self.up * move_vector.y + self.front * move_vector.z

    def rotate(self, window: Window, dt: float) -> None:
        window_width, window_height = window.get_size()

        if window.get_mouse_button_pressed(glfw.MOUSE_BUTTON_LEFT):
            half_window_width  = window_width  * 0.5
            half_window_height = window_height * 0.5

            window.set_mouse_visible(False)
            
            if self.first_click:
                window.set_mouse_pos(half_window_width, half_window_height)
                self.first_click = False

            mouse_x, mouse_y = window.get_mouse_pos()

            rotation_y = (mouse_x - half_window_width)  / window_width
            rotation_x = (mouse_y - half_window_height) / window_height

            rotation_vector = glm.vec3(-rotation_x, rotation_y, 0.0)
            
            self.rotation += rotation_vector * self.sensitivity * dt

            if   self.rotation.x >  89.0: self.rotation.x =  89.0
            elif self.rotation.x < -89.0: self.rotation.x = -89.0
            
            window.set_mouse_pos(half_window_width, half_window_height)
        else:
            window.set_mouse_visible(True)
            self.first_click = True

    def get_proj_matrix(self, window: Window) -> glm.mat4x4:
        return glm.perspective(self.fov, window.get_aspect_ratio(), self.near, self.far)

    def get_view_matrix(self) -> glm.mat4x4:
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def update_vectors(self) -> None:
        # Calculate Front Vector
        self.front = glm.normalize(glm.vec3(
            glm.cos(glm.radians(self.rotation.x)) * glm.cos(glm.radians(self.rotation.y)),
            glm.sin(glm.radians(self.rotation.x)),
            glm.cos(glm.radians(self.rotation.x)) * glm.sin(glm.radians(self.rotation.y))
        ))

        world_up = glm.vec3(0.0, 1.0, 0.0)

        # Calculate Right and Up Vectors
        self.right = glm.normalize(glm.cross(self.front, world_up))
        self.up    = glm.normalize(glm.cross(self.right, self.front))
