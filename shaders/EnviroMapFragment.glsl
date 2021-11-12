#version 330

in vec2 v_texture;
in vec3 v_normal;
in vec3 FragPos;

in vec3 R;

out vec4 out_color;

uniform vec3 viewpos;

uniform int num_lights;
uniform vec3 lightpos[24];
uniform vec3 color[24];
uniform float ambient[24];
uniform float diffuse[24];
uniform float specular[24];
uniform float specular_power[24];
uniform vec3 attenuation[24];

uniform sampler2D s_texture;
uniform samplerCube skybox;
uniform sampler2D shadowMap;

void main() {

    // Ambient
    vec3 totalLighting = ambient[0] * color[0];

    for (int i = 0; i < num_lights; i++)
    {

        float distance = length(lightpos[i] - FragPos);
        float attenuation = 1.0 / (attenuation[i].x +
                                   attenuation[i].y * distance +
                                   attenuation[i].z * distance * distance);

        // Diffuse
        vec3 norm = normalize(v_normal);
        vec3 lightDir = normalize(lightpos[i] - FragPos);
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = diff * color[i] * diffuse[i] * attenuation;
        
        // Specular
        vec3 viewDir = normalize(viewpos - FragPos);
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), specular_power[i]);
        vec3 specular = specular[i] * spec * color[i] * attenuation;

        totalLighting = totalLighting + (texture(s_texture, v_texture).xyz * (diffuse + specular));
    }

    //vec3 result = texture(s_texture, v_texture).xyz * (ambient + diffuse + specular);
    //out_color = vec4(result, 1.0) * refl;


    //vec3 I = normalize(FragPos - viewpos);
    //vec3 R = reflect(I, normalize(v_normal));
    //vec4 test = vec4(texture(skybox, R).rgb, 1.0);

    //out_color = vec4(totalLighting, 1.0) * test;

    #extension GL_NV_shadow_samplers_cube : enable
    vec4 texColor = textureCube(skybox, R);
    out_color = texColor;

    //out_color = vec4(vec3(depth), 1.0);
}