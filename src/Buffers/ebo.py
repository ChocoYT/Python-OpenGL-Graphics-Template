import numpy as np
import OpenGL.GL as gl

class EBO:
    def __init__(self, indices: np.ndarray) -> None:
        self.id = gl.glGenBuffers(1)
        
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.id)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW)

    def bind(self) -> None:
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.id)
    
    def unbind(self) -> None:
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

    def destroy(self) -> None:
        gl.glDeleteBuffers(1, [self.id])
