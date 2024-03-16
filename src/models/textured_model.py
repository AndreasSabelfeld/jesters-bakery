
class TexturedModel:
    """
    Class that creates a TexturedModel object which holds a RawModel and a texture
    """
    def __init__(self, model, texture):
        self.__raw_model = model
        self.__texture = texture

    def get_raw_model(self):
        return self.__raw_model

    def get_texture(self):
        return self.__texture

    def set_texture(self, texture):
        self.__texture = texture
