import OpenGL.GL as gl

class Shader:
    def __init__(self, path: str, shader_type: int) -> None:
        self.id = gl.glCreateShader(shader_type)
        
        # Load Source
        try:
            with open(path, 'r') as f:
                source = f.read()
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Shader File not Found at: {path}")

        gl.glShaderSource(self.id, source)
        gl.glCompileShader(self.id)

        # Error Checking
        if not gl.glGetShaderiv(self.id, gl.GL_COMPILE_STATUS):
            error_log = gl.glGetShaderInfoLog(self.id).decode()
            shader_name = "Vertex" if shader_type == gl.GL_VERTEX_SHADER else "Fragment"
            
            raise RuntimeError(f"{shader_name} Shader Compilation Failed:\n{error_log}")

    def delete(self) -> None:
        gl.glDeleteShader(self.id)
