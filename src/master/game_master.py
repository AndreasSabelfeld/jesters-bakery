from src.entities.camera import Camera
from src.entities.light import Light
from src.entities.player import FirstPersonPlayer
from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.font_rendering.text_master import TextMaster
from src.game_mechanics.game_object import GameObject
from src.game_mechanics.order import MasterOrder
from src.game_mechanics.pick_up import Carry
from src.game_mechanics.scanner import Scanner
from src.game_mechanics.tap import Tap
from src.master import prefabs
from src.models.textured_model import TexturedModel
from src.obj_converter.obj_loader import OBJLoader, NormalMappedOBJLoader
from src.render_engine.display_manager import DisplayManager
from src.render_engine.gui_renderer import GuiRenderer
from src.render_engine.loader import Loader
from src.game_mechanics.coffee_container import CoffeeContainer
from src.render_engine.master_renderer import MasterRenderer
from src.terrain.terrain import Terrain
from src.textures.model_texture import ModelTexture
from src.textures.terrain_texture import TerrainTexture
from src.textures.terrain_texture_pack import TerrainTexturePack
from src.toolbox.raycaster import TerrainRaycaster, ObjectRaycaster


class GameMaster:
    def __init__(self):
        self.__entities = []
        self.__nm_entities = []
        self.__collider_entities = []
        self.__movable_entities = []
        self.__shadow_map_entities = []
        self.__terrains = []
        self.__lights = []

        self.__display = DisplayManager(1920, 1080)
        self.__display.create_display("An-gine")  # creates display
        self.__display.set_backdrop_color(173, 216, 230)

        self.__loader = Loader()
        self.__obj_loader = OBJLoader()
        self.__normal_mapped_obj_loader = NormalMappedOBJLoader()
        CoffeeContainer.add_loaders(self.__loader, self.__obj_loader)
        TextMaster(self.__loader)

        player_model = self.__obj_loader.load_obj_model("objs/legacy/bunny", self.__loader)
        static_player_model = TexturedModel(player_model, ModelTexture(self.__loader.load_texture("white")))

        self.__player = FirstPersonPlayer(static_player_model, [160.5, 5.18, 180], 0, 0, 0, 3)
        self.__player.set_player_size(14)
        self.__camera = Camera(self.__player)

        self.__master_renderer = MasterRenderer(self.__loader, self.__camera)
        self.__master_renderer.set_fog_density(0.0035)
        self.__master_renderer.set_fog_gradient(5)
        self.__master_renderer.get_shadow_map_texture()

        self.__gui_renderer = GuiRenderer(self.__loader)

        self.__terrain_picker = TerrainRaycaster(self.__camera, self.__master_renderer.get_projection_matrix())
        self.__object_picker = ObjectRaycaster(self.__camera, self.__master_renderer.get_projection_matrix())

        self.__sun = Light([100000, 150000, -100000], [1, 1, 1])
        self.__lights.append(self.__sun)

        self.__scanner = Scanner(self.__object_picker, self.__loader)

        size = 1.75
        self.__coffee_machine       = self.__load_coffee_machine(size)
        self.__coffee_machine_lf    = self.__load_coffee_machine_lactose_free(size)
        self.__fridge               = self.__load_fridge(size)
        self.__milk_foamer          = self.__load_milk_foamer()
        self.__mixer_vessel         = self.__load_mixer_vessel()
        self.__counter              = self.__load_counter(size)
        self.__finished_collider    = self.__load_finished_collider(size)

        self.__coffee_os                = self.__coffee_machine.get_attachment()
        self.__coffee_os_lactose_free   = self.__coffee_machine_lf.get_attachment()
        self.__fridge_os                = self.__fridge.get_child_0().get_attachment()
        self.__milk_foamer_os           = self.__milk_foamer.get_attachment()
        self.__mixer_vessel_os          = self.__mixer_vessel.get_attachment()
        self.__master_order             = MasterOrder(self.__loader, self.__obj_loader, self.__gui_renderer, self.__counter)

        self.__finished_collider.set_attachment(self.__master_order)

        self.__carry = Carry(self.__terrain_picker, self.__object_picker, self.__coffee_machine, self.__coffee_machine_lf)
        self.__carry.movable_entities = self.__movable_entities

        self.__load_game()

    def start_game(self):
        ...

    def stop_game(self):
        ...

    def __load_game(self):
        self.__load_terrain()
        self.__load_ui()
        self.__load_machines()

    def __load_terrain(self):
        background_texture = TerrainTexture(self.__loader.load_texture("asphalt"))
        r_texture = TerrainTexture(self.__loader.load_texture("floor_tiles"))
        g_texture = TerrainTexture(self.__loader.load_texture("asphalt"))
        b_texture = TerrainTexture(self.__loader.load_texture(""))

        texture_pack = TerrainTexturePack(background_texture, r_texture, g_texture, b_texture)
        blend_map = TerrainTexture(self.__loader.load_texture("bakery_blendmap"))

        Terrain.set_size(300)
        terrain = Terrain(0, 0, self.__loader, texture_pack, blend_map, "bakery_heightmap")
        self.__terrains.append(terrain)

    def __load_ui(self):
        font = FontType(self.__loader.load_texture("candara"), "res/candara.fnt")
        text1 = GUIText("a sample text!", 15, font, [0, 0.02], 1, False)
        text1.set_color(1, 0, 0)
        text1.set_border_width(0.7)
        text1.set_border_edge(0.1)
        text2 = GUIText("a sample text!", 20, font, [0, 0.1], 1, False)
        text2.set_color(1, 0, 0)
        text2.set_border_width(0.7)
        text2.set_border_edge(0.1)
        text3 = GUIText("a sample text!", 20, font, [0, 0.2], 1, False)
        text3.set_color(1, 0, 0)
        text3.set_border_width(0.7)
        text3.set_border_edge(0.1)

    def __load_machines(self):
        machine_size = 1.75
        ice_machine_door = prefabs.ice_machine([179.5, 5.18, 185.5], [0, -90, 0], machine_size, self.__loader,
                                               self.__obj_loader, self.__entities, self.__collider_entities)
        mixer_game_object = prefabs.mixer([150, 12.5, 185], [0, 90, 0], 0.5, self.__loader, self.__obj_loader)
        grass_texture = ModelTexture(self.__loader.load_texture("grass_block"))
        textures = [ModelTexture(self.__loader.load_texture("pngs/cups/coke_filling_tex")),
                    ModelTexture(self.__loader.load_texture("pngs/cups/schorle_filling_tex")),
                    ModelTexture(self.__loader.load_texture("pngs/cups/water_filling_tex")),
                    ModelTexture(self.__loader.load_texture("pngs/cups/water_filling_tex")),
                    ModelTexture(self.__loader.load_texture("pngs/cups/beer_filling_tex"))]
        tap = Tap(self.__obj_loader, self.__loader, [179.5, 12.5, 185.5], [0, -90, 0], 1, textures)

    def __load_entrance_area(self):
        ...

    def __load_traiteur_area(self):
        ...

    def __load_working_area(self):
        ...

    def __load_kitchen_area(self):
        ...

    def __load_eating_area(self):
        ...

    def __load_chairs(self):
        ...

    def __load_walls(self):
        ...

    def __load_outside_area(self):
        ...

    def __load_coffee_machine(self, size: float) -> GameObject:
        coffee_machine_game_object = prefabs.coffee_machine([150, 12.5, 192], [0, 90, 0], size,
                                                            self.__loader,
                                                            self.__obj_loader,
                                                            self.__gui_renderer,
                                                            self.__object_picker)
        return coffee_machine_game_object

    def __load_coffee_machine_lactose_free(self, size: float) -> GameObject:
        coffee_machine_lactose_free_game_object = prefabs.lactose_free_coffee_machine([150, 12.5, 198], [0, 90, 0],
                                                                                      size,
                                                                                      self.__loader,
                                                                                      self.__obj_loader,
                                                                                      self.__gui_renderer,
                                                                                      self.__object_picker)
        return coffee_machine_lactose_free_game_object

    def __load_fridge(self, size: float) -> GameObject:
        fridge_game_object = prefabs.fridge([149.7, 5.18, 187.6], [0, 90, 0], size, self.__loader,
                                            self.__obj_loader, self.__gui_renderer, self.__object_picker)
        return fridge_game_object

    def __load_milk_foamer(self) -> GameObject:
        milk_foamer_game_object = prefabs.milk_foamer([150, 12.5, 175], [0, 90, 0], 1, self.__loader, self.__obj_loader,
                                                      self.__gui_renderer, self.__object_picker)
        return milk_foamer_game_object

    def __load_mixer_vessel(self) -> GameObject:
        mixer_vessel_game_object = prefabs.mixer_vessel([150, 12.5, 183], [0, 90, 0], 0.5, self.__loader,
                                                        self.__obj_loader)
        return mixer_vessel_game_object

    def __load_counter(self, size: float) -> GameObject:
        counter = prefabs.finished_counter([179.5, 5.18, 185.5], [0, -90, 0], size, self.__loader, self.__obj_loader)
        return counter

    def __load_finished_collider(self, size: float) -> GameObject:
        col = prefabs.finished_collider([179.5, 5.18, 185.5], [0, -90, 0], size, self.__loader, self.__obj_loader)
        return col
