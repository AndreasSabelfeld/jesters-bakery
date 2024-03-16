#version 150

out vec4 out_colour;

in vec2 blur_texture_coords[11];

uniform sampler2D original_texture;

void main(void){

	out_colour = vec4(0.0);
	out_colour += texture(original_texture, blur_texture_coords[0]) * 0.0093;
    out_colour += texture(original_texture, blur_texture_coords[1]) * 0.028002;
    out_colour += texture(original_texture, blur_texture_coords[2]) * 0.065984;
    out_colour += texture(original_texture, blur_texture_coords[3]) * 0.121703;
    out_colour += texture(original_texture, blur_texture_coords[4]) * 0.175713;
    out_colour += texture(original_texture, blur_texture_coords[5]) * 0.198596;
    out_colour += texture(original_texture, blur_texture_coords[6]) * 0.175713;
    out_colour += texture(original_texture, blur_texture_coords[7]) * 0.121703;
    out_colour += texture(original_texture, blur_texture_coords[8]) * 0.065984;
    out_colour += texture(original_texture, blur_texture_coords[9]) * 0.028002;
    out_colour += texture(original_texture, blur_texture_coords[10]) * 0.0093;

}