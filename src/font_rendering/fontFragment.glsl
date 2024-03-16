#version 330

in vec2 pass_texture_coords;

out vec4 out_color;

uniform vec3 color;
uniform sampler2D font_atlas;

uniform float width;
uniform float edge;

uniform float border_width;
uniform float border_edge;

uniform vec2 offset;

uniform vec3 outline_color;

void main(void){

    float distance = 1.0 - texture(font_atlas, pass_texture_coords).a;
    float alpha = 1.0 - smoothstep(width, width + edge, distance);

    float distance2 = 1.0 - texture(font_atlas, pass_texture_coords + offset).a;
    float outline_alpha = 1.0 - smoothstep(border_width, border_width + border_edge, distance2);

    float overall_alpha = alpha + (1.0 - alpha) * outline_alpha;
    vec3 overall_color = mix(outline_color, color, alpha / overall_alpha);

    out_color = vec4(overall_color, overall_alpha);

}