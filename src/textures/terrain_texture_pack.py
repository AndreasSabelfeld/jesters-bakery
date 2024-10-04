
class TerrainTexturePack:
    """
    Class for a pack of terrain textures.
    """

    def __init__(self, background_texture, r_texture, g_texture, b_texture):
        """
        Initializes a new TerrainTexturePack.

        :params background_texture: The background texture.
        :params r_texture: The red texture.
        :params g_texture: The green texture.
        :params b_texture: The blue texture.
        """
        self.__background_texture = background_texture
        self.__r_texture = r_texture
        self.__g_texture = g_texture
        self.__b_texture = b_texture

    def get_background_texture(self):
        """
        Returns the background texture.

        :return: The background texture.
        """
        return self.__background_texture

    def get_r_texture(self):
        """
        Returns the red texture.

        :return: The red texture.
        """
        return self.__r_texture

    def get_g_texture(self):
        """
        Returns the green texture.

        :return: The green texture.
        """
        return self.__g_texture

    def get_b_texture(self):
        """
        Returns the blue texture.

        :return: The blue texture.
        """
        return self.__b_texture
