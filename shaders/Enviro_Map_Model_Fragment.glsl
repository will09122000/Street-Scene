#version 330

// In attributes.
in vec3 v_normal;
in vec3 frag_position;

// Uniforms.
uniform vec3 view_position;
uniform samplerCube skybox;

// Out attributes.
out vec4 out_color;

void main() {

    vec3 I = normalize(frag_position - view_position);
    vec3 R = reflect(I, normalize(v_normal));
    vec4 reflection = vec4(texture(skybox, R).rgb, 1.0);

    out_color = reflection;
}