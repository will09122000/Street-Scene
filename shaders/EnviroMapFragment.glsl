#version 330

//in vec2 v_texture;
in vec3 v_normal;
in vec3 FragPos;

//in vec3 R;

out vec4 out_color;

uniform vec3 viewpos;

uniform sampler2D s_texture;
uniform samplerCube skybox;
uniform sampler2D shadowMap;

uniform mat3 VT;

void main() {

    //vec3 result = texture(s_texture, v_texture).xyz * (ambient + diffuse + specular);
    //out_color = vec4(result, 1.0) * refl;

    //vec3 reflected = reflect(normalize(-FragPos), normalize(v_normal));

    //out_color = vec4(texture(skybox, normalize(VT*reflected)).rgb, 1.0);
    vec3 I = normalize(FragPos - viewpos);
    vec3 R = reflect(I, normalize(v_normal));
    vec4 refl = vec4(texture(skybox, R).rgb, 1.0);

    out_color = refl;

}