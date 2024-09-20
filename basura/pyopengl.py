import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import ctypes

# Inicializar GLFW
if not glfw.init():
    raise Exception("GLFW no se pudo inicializar")

# Crear una ventana
window = glfw.create_window(800, 600, "Cuadrado con PyOpenGL", None, None)
if not window:
    glfw.terminate()
    raise Exception("No se pudo crear la ventana")

# Establecer el contexto de OpenGL
glfw.make_context_current(window)

# Vertex Shader
vertex_shader_code = """
#version 330
layout(location = 0) in vec3 aPos;
void main()
{
    gl_Position = vec4(aPos, 1.0);
}
"""

# Fragment Shader
fragment_shader_code = """
#version 330
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0, 1.0, 1.0, 1.0); // Color blanco
}
"""

# Compilar y enlazar shaders
def compile_shaders(vertex_code, fragment_code):
    vertex_shader = compileShader(vertex_code, GL_VERTEX_SHADER)
    fragment_shader = compileShader(fragment_code, GL_FRAGMENT_SHADER)
    shader_program = compileProgram(vertex_shader, fragment_shader)
    return shader_program

shader_program = compile_shaders(vertex_shader_code, fragment_shader_code)

# Definir los vértices del cuadrado
square_vertices = [
    -0.5, -0.5, 0.0,  # Esquina inferior izquierda
     0.5, -0.5, 0.0,  # Esquina inferior derecha
     0.5,  0.5, 0.0,  # Esquina superior derecha
    -0.5,  0.5, 0.0   # Esquina superior izquierda
]

# Definir los índices para los triángulos
indices = [0, 1, 2, 2, 3, 0]

# Convertir los datos a tipo C float y C uint32
square_vertices = (GLfloat * len(square_vertices))(*square_vertices)
indices = (GLuint * len(indices))(*indices)

# Crear un Vertex Buffer Object (VBO)
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, len(square_vertices) * ctypes.sizeof(GLfloat), square_vertices, GL_STATIC_DRAW)

# Crear un Element Buffer Object (EBO)
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * ctypes.sizeof(GLuint), indices, GL_STATIC_DRAW)

# Crear el Vertex Array Object (VAO)
VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)

# Especificar el layout de los datos en el VAO
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * ctypes.sizeof(GLfloat), ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

# Desvincular el VBO, EBO y VAO
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

# Configurar el color de fondo
glClearColor(0.0, 0.0, 0.0, 1.0)  # Color de fondo negro
glViewport(0, 0, 800, 600)

# Bucle principal
while not glfw.window_should_close(window):
    # Limpiar la pantalla
    glClear(GL_COLOR_BUFFER_BIT)

    # Usar el programa de shaders
    glUseProgram(shader_program)

    # Dibujar el cuadrado
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    glBindVertexArray(0)

    # Intercambiar buffers y manejar eventos
    glfw.swap_buffers(window)
    glfw.poll_events()

# Liberar los recursos
glDeleteVertexArrays(1, [VAO])
glDeleteBuffers(1, [VBO])
glDeleteBuffers(1, [EBO])
glDeleteProgram(shader_program)
glfw.terminate()
