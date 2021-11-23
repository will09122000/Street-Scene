#version 330

// In attributes
in vec2 v_texture;

// Uniforms
uniform sampler2D s_texture;

// Out attributes
out vec4 out_colour;

void main() {
    out_colour = texture(s_texture, v_texture);
}
