
class TerrainTexturePack:

    def __init__(self, background_texture, r_texture, g_texture, b_texture):
        self.__background_texture = background_texture
        self.__r_texture = r_texture
        self.__g_texture = g_texture
        self.__b_texture = b_texture

    def get_background_texture(self):
        return self.__background_texture

    def get_r_texture(self):
        return self.__r_texture

    def get_g_texture(self):
        return self.__g_texture

    def get_b_texture(self):
        return self.__b_texture
