#version 400 core

in vec2 pass_texture_coords;
in vec3 to_light_vector[5];
in vec3 to_camera_vector;
in float visibility;

layout (location = 0) out vec4 out_color;
layout (location = 1) out vec4 out_bright_color;

uniform sampler2D model_texture;
uniform sampler2D specular_map;
uniform float uses_specular_map;
uniform sampler2D normal_map;
uniform vec3 light_color[5];
uniform vec3 attenuation[5];
uniform float shine_damper;
uniform float reflectivity;
uniform vec3 sky_color;

void main(void){
    vec4 texture_color = texture(model_texture, pass_texture_coords);
    if(texture_color.a < 0.5){
        discard;
    }

    vec4 normal_map_value = 2.0 * texture(normal_map, pass_texture_coords) - 1.0;

    vec3 unit_vector_to_camera = normalize(to_camera_vector);
    vec3 unit_normal = normalize(normal_map_value.rgb);

    vec3 total_diffuse = vec3(0.0);
    vec3 total_specular = vec3(0.0);

    for(int i=0;i<5;i++){
        float distance = length(to_light_vector[i]);
        float att_factor = attenuation[i].x + (attenuation[i].y * distance) + (attenuation[i].z * distance * distance);
        vec3 unit_light_vector = normalize(to_light_vector[i]);

        float n_dot1 = dot(unit_normal, unit_light_vector);
        float brightness = max(n_dot1, 0.4);

        vec3 light_direction = -unit_light_vector;
        vec3 reflected_light_direction = reflect(light_direction, unit_normal);

        float specular_factor = dot(reflected_light_direction, unit_vector_to_camera);
        specular_factor = max(specular_factor, 0.2);
        float damped_factor = pow(specular_factor, shine_damper);
        total_diffuse = total_diffuse + (brightness * light_color[i]) / att_factor;
        total_specular = total_specular + (damped_factor * reflectivity * light_color[i]) / att_factor;
    }
    total_diffuse = max(total_diffuse, 0.4);

    out_bright_color = vec4(0.0);
    if(uses_specular_map > 0.5){
        vec4 map_info = texture(specular_map, pass_texture_coords);
        total_specular *= map_info.r;
        if(map_info.g > 0.5){
            out_bright_color = texture_color + vec4(total_specular, 1.0);
            total_diffuse = vec3(1.0);
        }
    }

    out_color = vec4(total_diffuse, 1.0) * texture_color + vec4(total_specular, 1.0);
    out_color = mix(vec4(sky_color, 1.0), out_color, visibility);


}