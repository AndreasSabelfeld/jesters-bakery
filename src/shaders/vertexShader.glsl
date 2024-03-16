#version 400 core

in vec3 position;
in vec2 texture_coords;
in vec3 normal;

out vec2 pass_texture_coords;
out vec3 surface_normal;
out vec3 to_light_vector[5];
out vec3 to_camera_vector;
out float visibility;
out vec4 shadow_coords;

uniform mat4 transformation_matrix;
uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform vec3 light_position[5];

uniform float use_fake_lighting;

uniform float number_of_rows;
uniform vec2 offset;

uniform mat4 shadow_offset;
uniform mat4 ortho_projection_matrix;
uniform mat4 light_view_matrix;

uniform float fog_density;
uniform float fog_gradient;

uniform float shadow_distance;
const float transition_distance = 10.0;

uniform vec4 plane;

void main(void){

    vec4 world_position = transformation_matrix * vec4(position, 1.0);

    mat4 projection_view_matrix = ortho_projection_matrix * light_view_matrix;
    mat4 to_shadow_map_space = shadow_offset * projection_view_matrix;
    shadow_coords = to_shadow_map_space * world_position;

    gl_ClipDistance[0] = dot(world_position, plane);

    vec4 position_relative_to_cam = view_matrix * world_position;
    gl_Position = projection_matrix * position_relative_to_cam;
    pass_texture_coords = (texture_coords / number_of_rows) + offset;

    vec3 actual_normal = mix(normal, vec3(0, 1, 0), use_fake_lighting);

    surface_normal = (transformation_matrix * vec4(actual_normal, 0.0)).xyz;
    for(int i=0; i<5;i++){
        to_light_vector[i] = light_position[i] - world_position.xyz;
    }
    to_camera_vector = (inverse(view_matrix) * vec4(0.0, 0.0, 0.0, 1.0)).xyz - world_position.xyz;

    float distance = length(position_relative_to_cam.xyz);
    visibility = exp(-pow((distance*fog_density), fog_gradient));
    visibility = clamp(visibility, 0.0, 1.0);

    distance = distance - (shadow_distance - transition_distance);
    distance = distance / transition_distance;
    shadow_coords.w = clamp(1.0-distance, 0.0, 1.0);

}