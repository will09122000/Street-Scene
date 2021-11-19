#version 330

// In attributes.
in vec3 position;
in vec2 texture_coord;
in vec3 normal;

// Uniforms.
uniform mat4 projection;
uniform mat4 model;
uniform mat4 view;
uniform vec3 scale;

// Out attributes.
out vec2 v_texture;
out vec3 v_normal;
out vec3 frag_position;

void main() {

    vec3 scaled_position = vec3(position.x * scale.x, position.y * scale.y, position.z * scale.z);

    v_texture = texture_coord;
    v_normal = mat3(transpose(inverse(model))) * normal;
    frag_position = vec3(model * vec4(scaled_position, 1.0));
    gl_Position = projection * view * model * vec4(scaled_position, 1.0);
}