#version 330

in vec3 a_position;
in vec2 a_texture;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

uniform vec3 scale;

out vec2 v_texture;

void main() {
    vec3 spos = vec3(a_position.x*scale.x, a_position.y*scale.y, a_position.z*scale.z);

    vec4 glpos = projection * view * model * vec4(spos, 1.0);
    gl_Position = glpos;
    v_texture = a_texture;
}