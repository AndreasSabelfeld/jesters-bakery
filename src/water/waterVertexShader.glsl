#version 400 core

in vec2 position;

out vec4 clip_space;
out vec2 texture_coords;
out vec3 to_camera_vector;
out vec3 from_light_vector;

uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform mat4 model_matrix;
uniform vec3 light_position;

uniform vec3 camera_position;

const float tiling = 4.0;

void main(void) {

	gl_ClipDistance[0] = 1;

	vec4 world_position = model_matrix * vec4(position.x, 0.0, position.y, 1.0);
	clip_space = projection_matrix * view_matrix * world_position;
	gl_Position = clip_space;
	texture_coords = vec2(position.x / 2.0 + 0.5, position.y / 2.0 + 0.5) * tiling;
	to_camera_vector = camera_position - world_position.xyz;
	from_light_vector = world_position.xyz - light_position;

}