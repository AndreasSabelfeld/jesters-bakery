#version 140

/**
https://github.com/kiwipxl/GLSL-shaders/blob/master/outline.glsl
-------------- outline vertex shader -------------

    author: Richman Stewart

    simple vertex shader that sets the position
    to the specified matrix and position while
    passing the vertex colour and tex coords
    to the fragment shader

**/

in vec2 a_position;
in vec2 a_tex_coord;

uniform mat4 matrix;

out vec2 tex_coords;

void main() {
   tex_coords = a_tex_coord;
   gl_Position = matrix * vec4(a_position, 0, 1);
}
