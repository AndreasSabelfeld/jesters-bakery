#version 400

in vec3 position;
out vec3 texture_coords;

uniform mat4 projection_matrix;
uniform mat4 view_matrix;

void main(void){

    gl_ClipDistance[0] = 1;

    vec4 untranslated_view = view_matrix * vec4(position, 0.0f);
    untranslated_view.w = 1.0f;

	gl_Position = projection_matrix * untranslated_view;
	texture_coords = position;

}