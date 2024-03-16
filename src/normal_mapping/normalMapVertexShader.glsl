#version 400 core

in vec3 position;
in vec2 texture_coords;
in vec3 normal;
in vec3 tangent;

out vec2 pass_texture_coords;
out vec3 to_light_vector[5];
out vec3 to_camera_vector;
out float visibility;

uniform mat4 transformation_matrix;
uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform vec3 light_position_eye_space[5];

uniform float use_fake_lighting;

uniform float number_of_rows;
uniform vec2 offset;

uniform float fog_density;
uniform float fog_gradient;

uniform vec4 plane;

void main(void){
    vec4 world_position = transformation_matrix * vec4(position, 1.0);

    gl_ClipDistance[0] = dot(world_position, plane);

    mat4 model_view_matrix = view_matrix * transformation_matrix;
    vec4 position_relative_to_cam = model_view_matrix * vec4(position, 1.0);
    gl_Position = projection_matrix * position_relative_to_cam;

    pass_texture_coords = (texture_coords / number_of_rows) + offset;

    vec3 surface_normal = (model_view_matrix * vec4(normal, 0.0)).xyz;

    vec3 norm = normalize(surface_normal);
    vec3 tang = normalize((model_view_matrix * vec4(tangent, 0.0)).xyz);
    vec3 bitang = normalize(cross(norm, tang));

    mat3 to_tangent_space = mat3(
        tang.x, bitang.x, norm.x,
        tang.y, bitang.y, norm.y,
        tang.z, bitang.z, norm.z
    );

    for(int i=0; i<5;i++){
        to_light_vector[i] = to_tangent_space * (light_position_eye_space[i] - position_relative_to_cam.xyz);
    }
    to_camera_vector = to_tangent_space * (-position_relative_to_cam.xyz);

    float distance = length(position_relative_to_cam.xyz);
    visibility = exp(-pow((distance*fog_density), fog_gradient));
    visibility = clamp(visibility, 0.0, 1.0);

}