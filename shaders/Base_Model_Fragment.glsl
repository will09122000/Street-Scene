#version 330

// In attributes
in vec2 v_texture;
in vec3 v_normal;
in vec3 frag_position;

// Uniforms
uniform vec3 view_position;
uniform sampler2D s_texture;

uniform int num_lights;
uniform vec3 light_position[64];
uniform vec3 colour[64];
uniform float ambient[64];
uniform float diffuse[64];
uniform float specular[64];
uniform vec3 attenuation[64];

// Out attributes
out vec4 out_colour;

void main() {

    // As it's a night scene, there is no ambient lighting.
    vec3 total_lighting = ambient[0] * colour[0];

    for (int i = 0; i < num_lights; i++)
    {

        // Attenuation
        float distance = length(light_position[i] - frag_position);
        // Calculates attentuation from constant, linear, and quadratic attentuation values.
        float attenuation = 1.0 / (attenuation[i].x +
                                   attenuation[i].y * distance +
                                   attenuation[i].z * distance * distance);

        // Diffuse
        vec3 normal = normalize(v_normal);
        vec3 light_dir = normalize(light_position[i] - frag_position);
        float diffuse_value = max(dot(normal, light_dir), 0.0);
        vec3 diffuse = diffuse_value * colour[i] * diffuse[i] * attenuation;

        // Specular
        vec3 view_dir = normalize(view_position - frag_position);
        vec3 reflect_dir = reflect(-light_dir, normal);
        float specular_value = max(dot(view_dir, reflect_dir), 0.0);
        vec3 specular = specular_value * colour[i] * specular[i] * attenuation;

        // Add to total lighting.
        total_lighting += (texture(s_texture, v_texture).xyz * (diffuse + specular));
    }

    out_colour = vec4(total_lighting, 1.0);
}
