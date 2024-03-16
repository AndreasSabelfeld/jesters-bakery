#version 330

in vec2 texture_coords;

uniform sampler2D model_texture;

out vec4 out_colour;

void main(void){

    float alpha = texture(model_texture, texture_coords).a;
    if(alpha < 0.5){
        discard;
    }

}