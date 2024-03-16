#version 150

in vec2 texture_coords;

out vec4 out_Colour;

uniform sampler2D color_texture;

void main(void){

    vec4 color = texture(color_texture, texture_coords);
    float brightness = (color.r * 0.2126) + (color.g * 0.7152) + (color.b * 0.0722);
    out_Colour = color * brightness;

}