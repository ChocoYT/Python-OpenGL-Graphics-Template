import glfw
from pathlib import Path

from config import config, load_config
load_config()

from Clock.clock   import Clock
from Window.window import Window

from Camera.camera  import Camera
from Mesh.mesh      import Mesh
from Shader.program import Program

def main() -> None:
    root_path = Path(__file__).resolve().parent.parent
    shader_path = root_path / "shaders"
    
    # Config
    WINDOW_WIDTH  = int(config["window"]["width"])
    WINDOW_HEIGHT = int(config["window"]["height"])
    WINDOW_FPS    = float(config["window"]["fps"])
    WINDOW_NAME   = str(config["window"]["name"])

    # Create Objects
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_NAME)
    clock  = Clock()
    
    camera = Camera()
    
    shader_program = Program(
        str(shader_path / "vert.glsl"),
        str(shader_path / "frag.glsl")
    )
    
    # Create Mesh
    vertices = [
        # X,    Y,    Z,    R,   G,   B,   A,   NX,   NY,   NZ
        # Back Face
        -0.5, -0.5, -0.5,  1.0, 0.5, 0.0, 1.0,  0.0,  0.0, -1.0,
         0.5,  0.5, -0.5,  1.0, 0.5, 0.0, 1.0,  0.0,  0.0, -1.0,
         0.5, -0.5, -0.5,  1.0, 0.5, 0.0, 1.0,  0.0,  0.0, -1.0,
        -0.5,  0.5, -0.5,  1.0, 0.5, 0.0, 1.0,  0.0,  0.0, -1.0,

        # Front Face
        -0.5, -0.5,  0.5,  1.0, 0.0, 0.0, 1.0,  0.0,  0.0,  1.0,
         0.5, -0.5,  0.5,  1.0, 0.0, 0.0, 1.0,  0.0,  0.0,  1.0,
         0.5,  0.5,  0.5,  1.0, 0.0, 0.0, 1.0,  0.0,  0.0,  1.0,
        -0.5,  0.5,  0.5,  1.0, 0.0, 0.0, 1.0,  0.0,  0.0,  1.0,

        # Left Face
        -0.5,  0.5,  0.5,  0.0, 0.0, 1.0, 1.0,  -1.0,  0.0,  0.0,
        -0.5,  0.5, -0.5,  0.0, 0.0, 1.0, 1.0,  -1.0,  0.0,  0.0,
        -0.5, -0.5, -0.5,  0.0, 0.0, 1.0, 1.0,  -1.0,  0.0,  0.0,
        -0.5, -0.5,  0.5,  0.0, 0.0, 1.0, 1.0,  -1.0,  0.0,  0.0,

        # Right Face
         0.5,  0.5,  0.5,  0.0, 1.0, 0.0, 1.0,  1.0,  0.0,  0.0,
         0.5, -0.5,  0.5,  0.0, 1.0, 0.0, 1.0,  1.0,  0.0,  0.0,
         0.5, -0.5, -0.5,  0.0, 1.0, 0.0, 1.0,  1.0,  0.0,  0.0,
         0.5,  0.5, -0.5,  0.0, 1.0, 0.0, 1.0,  1.0,  0.0,  0.0,

        # Bottom Face
        -0.5, -0.5, -0.5,  1.0, 1.0, 1.0, 1.0,  0.0, -1.0,  0.0,
         0.5, -0.5, -0.5,  1.0, 1.0, 1.0, 1.0,  0.0, -1.0,  0.0,
         0.5, -0.5,  0.5,  1.0, 1.0, 1.0, 1.0,  0.0, -1.0,  0.0,
        -0.5, -0.5,  0.5,  1.0, 1.0, 1.0, 1.0,  0.0, -1.0,  0.0,

        # Top Face
        -0.5,  0.5, -0.5,  1.0, 1.0, 0.0, 1.0,  0.0,  1.0,  0.0,
        -0.5,  0.5,  0.5,  1.0, 1.0, 0.0, 1.0,  0.0,  1.0,  0.0,
         0.5,  0.5,  0.5,  1.0, 1.0, 0.0, 1.0,  0.0,  1.0,  0.0,
         0.5,  0.5, -0.5,  1.0, 1.0, 0.0, 1.0,  0.0,  1.0,  0.0,
    ]
    
    indices = [
        0,  1,  2,  0,  3,  1,  # Back
        4,  5,  6,  4,  6,  7,  # Front
        8,  9,  10, 8,  10, 11, # Left
        12, 13, 14, 12, 14, 15, # Right
        16, 17, 18, 16, 18, 19, # Bottom
        20, 21, 22, 20, 22, 23  # Top
    ]
    
    mesh = Mesh(vertices, indices, has_colors=True, has_normals=True)
    
    # Uniforms
    proj_matrix = shader_program.create_uniform("uCameraProjMatrix")
    view_matrix = shader_program.create_uniform("uCameraViewMatrix")

    # Main loop
    dt = 0.0
    while not window.should_close():
        # Inputs
        if window.get_key_pressed(glfw.KEY_ESCAPE):
            window.set_should_close()

        # Clear Window
        window.clear(0.0, 0.0, 0.0, 1.0)
        
        # Update Camera
        camera.update(window, dt)
        
        # Use Shader
        shader_program.use()

        shader_program.set_mat4(proj_matrix, camera.get_proj_matrix(window))
        shader_program.set_mat4(view_matrix, camera.get_view_matrix())
        
        # Draw
        mesh.draw()
        
        # Cycle
        window.update()
        dt = clock.tick(WINDOW_FPS)

    # Destroy Resources
    shader_program.destroy()
    mesh.destroy()

    window.destroy()

if __name__ == "__main__":
    main()
