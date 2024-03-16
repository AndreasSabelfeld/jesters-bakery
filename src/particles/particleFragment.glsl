#version 140

out vec4 out_color;

in vec2 texture_coords_1;
in vec2 texture_coords_2;
in float blend;

uniform sampler2D particle_texture;

void main() {

    vec4 color_1 = texture(particle_texture, texture_coords_1);
    vec4 color_2 = texture(particle_texture, texture_coords_2);

    out_color = mix(color_1, color_2, blend);

}
