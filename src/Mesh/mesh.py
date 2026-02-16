import numpy as np
import OpenGL.GL as gl

from Buffers.vao import VAO
from Buffers.vbo import VBO
from Buffers.ebo import EBO

class Mesh:
    def __init__(
            self,
            vertices: list | np.ndarray,
            indices:  list | np.ndarray,
            has_colors:  bool = False,
            has_normals: bool = False
        ) -> None:
        
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)
        
        self.index_count = len(self.indices.flatten())
        
        elements_per_vertex = 3
        if has_colors:  elements_per_vertex += 4
        if has_normals: elements_per_vertex += 3
        
        stride = elements_per_vertex * 4
        
        # Setup Buffers
        self.vao = VAO()
        self.vao.bind()

        self.vbo = VBO(self.vertices)
        self.ebo = EBO(self.indices)
        
        offset = 0
        
        # Attribute 0: Position (Size 3)
        self.vao.link_attrib(self.vbo, 0, 3, stride, offset)
        offset += 3 * 4
        
        # Attribute 1: Color (Size 4)
        if has_colors:
            self.vao.link_attrib(self.vbo, 1, 4, stride, offset)
            offset += 4 * 4
        
        # Attribute 2: Normal (Size 3)
        if has_normals:
            self.vao.link_attrib(self.vbo, 2, 3, stride, offset)
            offset += 3 * 4

        self.vao.unbind()
        self.vbo.unbind()

    def draw(self) -> None:
        self.vao.bind()
        gl.glDrawElements(gl.GL_TRIANGLES, self.index_count, gl.GL_UNSIGNED_INT, None)
        self.vao.unbind()

    def destroy(self) -> None:
        self.vao.destroy()
        self.vbo.destroy()
        self.ebo.destroy()
