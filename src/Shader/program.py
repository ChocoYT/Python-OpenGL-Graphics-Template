import OpenGL.GL as gl
import glm

from Shader.shader import Shader

class Program:
    def __init__(self, vertex_path: str, fragment_path: str):
        self.id = gl.glCreateProgram()
        
        vertex_shader   = Shader(vertex_path, gl.GL_VERTEX_SHADER)
        fragment_shader = Shader(fragment_path, gl.GL_FRAGMENT_SHADER)
        
        gl.glAttachShader(self.id, vertex_shader.id)
        gl.glAttachShader(self.id, fragment_shader.id)
        
        gl.glLinkProgram(self.id)

        # Check for Linking Errors
        if not gl.glGetProgramiv(self.id, gl.GL_LINK_STATUS):
            error_log = gl.glGetProgramInfoLog(self.id).decode()
            
            raise RuntimeError(f"Shader Program Linking Failed:\n{error_log}")

    def use(self) -> None:
        gl.glUseProgram(self.id)
        
    def destroy(self) -> None:
        gl.glDeleteProgram(self.id)
        
    def create_uniform(self, name: str) -> int:
        return gl.glGetUniformLocation(self.id, name)

    def set_vec3(self, location: int, value: glm.vec3) -> None:
        gl.glUniform3fv(location, 1, 1, glm.value_ptr(value))
        
    def set_mat4(self, location: int, matrix: glm.mat4) -> None:
        gl.glUniformMatrix4fv(location, 1, gl.GL_FALSE, glm.value_ptr(matrix))
