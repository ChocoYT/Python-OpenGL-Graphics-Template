import ctypes
import OpenGL.GL as gl

from Buffers.vbo import VBO

class VAO:
    def __init__(self) -> None:
        self.id = gl.glGenVertexArrays(1)

    def link_attrib(
            self,
            vbo: VBO,
            layout: int,
            index: int,
            stride: int,
            offset: int | None = None
        ) -> None:
        
        vbo.bind()
        
        ptr_offset = ctypes.c_void_p(offset) if offset is not None else None
        
        gl.glVertexAttribPointer(layout, index, gl.GL_FLOAT, gl.GL_FALSE, stride, ptr_offset)
        gl.glEnableVertexAttribArray(layout)
        
        vbo.unbind()

    def bind(self) -> None:
        gl.glBindVertexArray(self.id)

    def unbind(self) -> None:
        gl.glBindVertexArray(0)

    def destroy(self) -> None:
        gl.glDeleteVertexArrays(1, [self.id])
