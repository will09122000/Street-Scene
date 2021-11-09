#version 330

in vec2 v_texture;
in vec3 v_normal;
in vec3 FragPos;

out vec4 out_color;

uniform vec3 viewpos;

uniform vec3 lightpos;
uniform vec3 color;
uniform float ambient_intensity;
uniform float diffuse_intensity;
uniform float specular_intensity;
uniform float specular_power;

uniform vec3 lightpos2;

uniform sampler2D s_texture;
uniform samplerCube skybox;
uniform sampler2D shadowMap;

struct lightSource
{
  vec3 lightpos;
  vec3 color;
  float ambient_intensity;
  float diffuse_intensity;
  float specular_intensity;
  float specular_power;
};
const int numberOfLights = 2;
lightSource lights[numberOfLights];

lightSource light0 = lightSource(
  vec3(20, 10, 20),
  vec3(1, 1, 1),
  0.0,
  0.7,
  0.8,
  32
);
lightSource light1 = lightSource(
  vec3(-20, 10, -20),
  vec3(1, 1, 1),
  0.0,
  0.7,
  0.8,
  32
);

void main() {

    lights[0] = light0;
    lights[1] = light1;

    // Ambient CHANGE COLOR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    vec3 totalLighting = ambient_intensity * color;

    for (int i = 0; i < numberOfLights; i++)
    {
        // Diffuse
        vec3 norm = normalize(v_normal);
        vec3 lightDir = normalize(lights[i].lightpos - FragPos);
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = diff * lights[i].color * lights[i].diffuse_intensity;
        
        // Specular
        vec3 viewDir = normalize(viewpos - FragPos);
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), lights[i].specular_power);
        vec3 specular = lights[i].specular_intensity * spec * lights[i].color;

        // Reflection
        vec3 I = normalize(FragPos - viewpos);
        vec3 R = reflect(I, normalize(v_normal));
        vec4 refl = vec4(texture(skybox, R).rgb, 1.0);

        totalLighting = totalLighting + (texture(s_texture, v_texture).xyz * (diffuse + specular));
    }

    //vec3 result = texture(s_texture, v_texture).xyz * (ambient + diffuse + specular);
    //out_color = vec4(result, 1.0) * refl;
    out_color = vec4(totalLighting, 1.0);

    //out_color = vec4(vec3(depth), 1.0);
}