#version 150

in vec3 in_position;
in vec2 in_texture_coords;

uniform mat4 light_view_matrix;
uniform mat4 projection_matrix;
uniform mat4 model_matrix;

out vec2 texture_coords;

void main(void){

	mat4 mvp_matrix = projection_matrix * light_view_matrix * model_matrix;
	gl_Position = mvp_matrix * vec4(in_position, 1.0);

	texture_coords = in_texture_coords;

}