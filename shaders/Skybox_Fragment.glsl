#version 330

// In attributes.
in vec3 v_texture;

// Uniforms.
uniform samplerCube cube_map;

// Out attributes.
out vec4 out_colour;

void main() {
    out_colour = texture(cube_map, v_texture);
}
