#version 330

// In attributes.
in vec3 position;

// Uniforms.
uniform mat4 projection;
uniform mat4 view;

// Out attributes.
out vec3 v_texture;

void main() {
    v_texture = position;
    gl_Position = (projection * view * vec4(position, 1.0)).xyww;
}