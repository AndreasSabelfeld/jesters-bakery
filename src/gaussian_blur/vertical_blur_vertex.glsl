#version 150

in vec2 position;

out vec2 blur_texture_coords[11];

uniform float target_height;

void main(void){

	gl_Position = vec4(position, 0.0, 1.0);
	vec2 centerTexCoords = position * 0.5 + 0.5;
	float pixel_size = 1.0 / target_height;

	for(int i=-5;i<=5;i++){
		blur_texture_coords[i+5] = centerTexCoords + vec2(0.0, pixel_size * i);
	}

}