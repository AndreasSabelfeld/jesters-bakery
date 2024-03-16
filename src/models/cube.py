cube_vertices = [
    -0.5, 0.5, -0.5,
    -0.5, -0.5, -0.5,
    0.5, -0.5, -0.5,
    0.5, 0.5, -0.5,

    -0.5, 0.5, 0.5,
    -0.5, -0.5, 0.5,
    0.5, -0.5, 0.5,
    0.5, 0.5, 0.5,

    0.5, 0.5, -0.5,
    0.5, -0.5, -0.5,
    0.5, -0.5, 0.5,
    0.5, 0.5, 0.5,

    -0.5, 0.5, -0.5,
    -0.5, -0.5, -0.5,
    -0.5, -0.5, 0.5,
    -0.5, 0.5, 0.5,

    -0.5, 0.5, 0.5,
    -0.5, 0.5, -0.5,
    0.5, 0.5, -0.5,
    0.5, 0.5, 0.5,

    -0.5, -0.5, 0.5,
    -0.5, -0.5, -0.5,
    0.5, -0.5, -0.5,
    0.5, -0.5, 0.5

]

cube_texture_coords = [

    0, 0,
    0, 1,
    1, 1,
    1, 0,
    0, 0,
    0, 1,
    1, 1,
    1, 0,
    0, 0,
    0, 1,
    1, 1,
    1, 0,
    0, 0,
    0, 1,
    1, 1,
    1, 0,
    0, 0,
    0, 1,
    1, 1,
    1, 0,
    0, 0,
    0, 1,
    1, 1,
    1, 0

]

cube_indices = [
    0, 1, 3,
    3, 1, 2,
    4, 5, 7,
    7, 5, 6,
    8, 9, 11,
    11, 9, 10,
    12, 13, 15,
    15, 13, 14,
    16, 17, 19,
    19, 17, 18,
    20, 21, 23,
    23, 21, 22

]

cube_normals = []
# doesn't really work but whatever
for i in range(len(cube_vertices) // 3):
    try:
        u = [cube_vertices[3 + 3 * i] - cube_vertices[0 + 3 * i], cube_vertices[4 + 3 * i] - cube_vertices[1 + 3 * i],
             cube_vertices[5 + 3 * i] - cube_vertices[2 + 3 * i]]
        v = [cube_vertices[6 + 3 * i] - cube_vertices[0 + 3 * i], cube_vertices[7 + 3 * i] - cube_vertices[1 + 3 * i],
             cube_vertices[8 + 3 * i] - cube_vertices[2 + 3 * i]]

        normal = [0, 0, 0]
        normal[0] = u[1] * v[2] - u[2] * v[1]
        normal[1] = u[2] * v[0] - u[0] * v[2]
        normal[2] = u[0] * v[1] - u[1] * v[0]

        cube_normals.append(normal)
    except IndexError:
        break            # lazy way
