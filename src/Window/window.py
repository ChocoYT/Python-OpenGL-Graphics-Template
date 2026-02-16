import glfw
import OpenGL.GL as gl
from typing import Any

class Window:
    def __init__(self, width: int, height: int, name: str):
        self._width = width
        self._height = height
        self._name = name

        # Initialize GLFW
        if not glfw.init():
            raise RuntimeError("Failed to Initialize GLFW.")

        # Set Window Hints (OpenGL 4.6 Core)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)

        # Create Window
        self._handle = glfw.create_window(self._width, self._height, self._name, None, None)
        if not self._handle:
            glfw.terminate()
            raise RuntimeError("Failed to Create GLFW Window.")

        # Make Context
        glfw.make_context_current(self._handle)
        gl.glViewport(0, 0, self._width, self._height)
        
        # Settings
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glCullFace(gl.GL_BACK)
        gl.glFrontFace(gl.GL_CCW)
        
        # V-Sync
        glfw.swap_interval(1)

    def update(self) -> None:
        glfw.swap_buffers(self._handle)
        glfw.poll_events()

    def destroy(self) -> None:
        glfw.destroy_window(self._handle)
        glfw.terminate()
        
    def clear(self, r: float, g: float, b: float, a: float) -> None:
        gl.glClearColor(r, g, b, a)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)  # type: ignore
    
    # Getters
    def get_width(self) -> int:
        return self._width
    
    def get_height(self) -> int:
        return self._height
    
    def get_name(self) -> str:
        return self._name
    
    def get_size(self) -> tuple[int, int]:
        return self._width, self._height
    
    def get_aspect_ratio(self) -> float:
        width, height = glfw.get_framebuffer_size(self._handle)
        return width / height
    
    def should_close(self) -> bool:
        return glfw.window_should_close(self._handle)
        
    def get_key_pressed(self, key: Any) -> bool:
        return glfw.get_key(self._handle, key) == glfw.PRESS
    
    def get_mouse_button_pressed(self, button: Any) -> bool:
        return glfw.get_mouse_button(self._handle, button)

    def get_mouse_pos(self) -> tuple[float, float]:
        return glfw.get_cursor_pos(self._handle)

    # Setters
    def set_should_close(self) -> None:
        glfw.set_window_should_close(self._handle, glfw.TRUE)
        
    def set_mouse_pos(self, x: float, y: float) -> None:
        glfw.set_cursor_pos(self._handle, x, y)

    def set_mouse_visible(self, visible: bool) -> None:
        mode = glfw.CURSOR_NORMAL if visible else glfw.CURSOR_HIDDEN
        glfw.set_input_mode(self._handle, glfw.CURSOR, mode)

