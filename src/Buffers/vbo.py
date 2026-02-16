import numpy as np
import OpenGL.GL as gl

class VBO:
    def __init__(self, data: np.ndarray) -> None:
        self.id = gl.glGenBuffers(1)
        
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.id)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_STATIC_DRAW)

    def bind(self) -> None:
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.id)
        
    def unbind(self) -> None:
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    def destroy(self) -> None:
        gl.glDeleteBuffers(1, [self.id])
