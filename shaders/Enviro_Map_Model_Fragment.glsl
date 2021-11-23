#version 330

// In attributes
in vec3 v_normal;
in vec3 frag_position;

// Uniforms
uniform vec3 view_position;
uniform samplerCube skybox;

// Out attributes
out vec4 out_colour;

void main() {

    // Incident vector from the normalised position in the view space.
    vec3 incident_vector = normalize(frag_position - view_position);
    // Incident vector is reflected around the normal.
    vec3 reflected_vector = reflect(incident_vector, normalize(v_normal));
    // Final reflection vector using the skybox texture.
    vec4 reflection = vec4(texture(skybox, reflected_vector).rgb, 1.0);

    out_colour = reflection;
}
