#version 330

// In attributes
in vec3 position;

// Uniforms
uniform mat4 projection;
uniform mat4 view;

// Out attributes
out vec3 v_texture;

void main() {

    // Forward on variable.
    v_texture = position;

    // Transforms the position, this variable is a standard output of the vertex shader.
    gl_Position = (projection * view * vec4(position, 1.0)).xyww;
}
