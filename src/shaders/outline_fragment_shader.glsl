#version 140

/**
https://github.com/kiwipxl/GLSL-shaders/blob/master/outline.glsl
------------ one pass outline shader ------------

    author: Richman Stewart

    applies a gaussian blur horizontally and vertically
    behind the original texture and makes it black

------------------ use ------------------------

    outline_thickness - outline spread amount
    outline_colour - colour of the outline

**/

in vec2 tex_coords;
out vec4 pixel;

uniform sampler2D model_texture;
uniform float outline_thickness = .2;
uniform vec4 outline_colour = vec4(0, 0, 1, 1);
uniform float outline_threshold = .5;

void main() {
    pixel = texture(model_texture, tex_coords);

    if (pixel.a <= outline_threshold) {
        ivec2 size = textureSize(model_texture, 0);

        float uv_x = tex_coords.x * size.x;
        float uv_y = tex_coords.y * size.y;

        float sum = 0.0;
        for (int n = 0; n < 9; ++n) {
            uv_y = (tex_coords.y * size.y) + (outline_thickness * float(n - 4.5));
            float h_sum = 0.0;
            h_sum += texelFetch(model_texture, ivec2(uv_x - (4.0 * outline_thickness), uv_y), 0).a;
            h_sum += texelFetch(model_texture, ivec2(uv_x - (3.0 * outline_thickness), uv_y), 0).a;
            h_sum += texelFetch(model_texture, ivec2(uv_x - (2.0 * outline_thickness), uv_y), 0).a;
            h_sum += texelFetch(model_texture, ivec2(uv_x - outline_thickness, uv_y), 0).a;
            h_sum += texelFetch(model_texture, ivec2(uv_x, uv_y), 0).a;
            h_sum += texelFetch(model_texture, ivec2(uv_x + outline_thickness, uv_y), 0).a;
            h_sum += texelFetch(model_texture, ivec2(uv_x + (2.0 * outline_thickness), uv_y), 0).a;
            h_sum += texelFetch(model_texture, ivec2(uv_x + (3.0 * outline_thickness), uv_y), 0).a;
            h_sum += texelFetch(model_texture, ivec2(uv_x + (4.0 * outline_thickness), uv_y), 0).a;
            sum += h_sum / 9.0;
        }

        if (sum / 9.0 >= 0.0001) {
            pixel = outline_colour;
        }
    }
}
