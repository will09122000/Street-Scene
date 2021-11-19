#version 330

// In attributes.
in vec3 v_texture;

// Uniforms.
uniform samplerCube cube_map;

// Out attributes.
out vec4 out_color;

void main() {
    out_color = texture(cube_map, v_texture);
}