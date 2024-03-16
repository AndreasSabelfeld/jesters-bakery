#version 140

in vec2 position;

in mat4 model_view_matrix;
in vec4 tex_offsets;
in float blend_factor;

out vec2 texture_coords_1;
out vec2 texture_coords_2;
out float blend;

uniform mat4 projection_matrix;
uniform float number_of_rows;

void main() {

    vec2 texture_coords = position + vec2(0.5, 0.5);
    texture_coords.y = 1.0 - texture_coords.y;
    texture_coords /= number_of_rows;
    texture_coords_1 = texture_coords + tex_offsets.xy;
    texture_coords_2 = texture_coords + tex_offsets.zw;
    blend = blend_factor;

    gl_Position = projection_matrix * model_view_matrix * vec4(position, 0.0, 1.0);

}
