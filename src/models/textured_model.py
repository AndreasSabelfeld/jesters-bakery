
class TexturedModel:
    """
    Class that creates a TexturedModel object which holds a RawModel and a texture
    """
    def __init__(self, model, texture):
        """
        Initialize a new textured model.

        :params model: The raw model of this textured model.
        :params texture: The texture to apply to the raw model.
        """
        self.__raw_model = model
        self.__texture = texture

    def get_raw_model(self):
        """
        Get the raw model.

        :return: The related RawModel object.
        """
        return self.__raw_model

    def get_texture(self):
        """
        Get the texture.

        :return: The related texture.
        """
        return self.__texture

    def set_texture(self, texture):
        """
        Set a new texture.

        :params texture: The new texture to apply.
        """
        self.__texture = texture
