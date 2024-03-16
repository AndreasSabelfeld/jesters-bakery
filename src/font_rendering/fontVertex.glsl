#version 330

in vec2 position;
in vec2 texture_coords;

out vec2 pass_texture_coords;

uniform vec2 translation;

void main() {

    gl_Position = vec4(position + translation * vec2(2.0, -2.0), 0.0, 1.0);
    pass_texture_coords = texture_coords;

}
