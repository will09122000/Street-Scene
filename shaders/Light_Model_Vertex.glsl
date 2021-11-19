#version 330

// In attributes.
in vec3 position;
in vec2 texture_coord;

// Uniforms.
uniform mat4 projection;
uniform mat4 model;
uniform mat4 view;
uniform vec3 scale;

// Out attributes.
out vec2 v_texture;

void main() {

    vec3 scaled_position = vec3(position.x * scale.x, position.y * scale.y, position.z * scale.z);

    v_texture = texture_coord;
    gl_Position = projection * view * model * vec4(scaled_position, 1.0);;
}