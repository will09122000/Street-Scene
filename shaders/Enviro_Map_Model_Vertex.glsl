#version 330

// In attributes
in vec3 position;
in vec3 normal;

// Uniforms
uniform mat4 projection;
uniform mat4 model;
uniform mat4 view;
uniform vec3 scale;

// Out attributes
out vec3 v_normal;
out vec3 frag_position;

void main() {

    // Scales the postion vector of the model in all dimensions.
    vec3 scaled_position = vec3(position.x * scale.x, position.y * scale.y, position.z * scale.z);

    // Calculate vectors for shading calculations.
    v_normal = mat3(transpose(inverse(model))) * normal;
    frag_position = vec3(model * vec4(scaled_position, 1.0));

    // Transforms the scaled position, this variable is a standard output of the vertex shader.
    gl_Position = projection * view * model * vec4(scaled_position, 1.0);
}
