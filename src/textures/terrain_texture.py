
class TerrainTexture:
    """
    Class for the texture for a terrain.
    """

    def __init__(self, texture_id: int):
        """
        Initializes a new TerrainTexture.

        :params texture_id: The ID of the terrain texture.
        """
        self.__texture_id = texture_id

    def get_texture_id(self) -> int:
        """
        Returns the terrain texture ID.

        :return: The terrain texture ID.
        """
        return self.__texture_id
