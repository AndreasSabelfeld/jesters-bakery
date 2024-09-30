from OpenGL.GLUT import *

from src.audio.audio_master import AudioMaster
from src.font_rendering.text_master import TextMaster
from src.game_mechanics.coffee_container import CoffeeContainer
from src.game_mechanics.coffee_machine_os import CoffeeMachineOS
from src.game_mechanics.coffee_product import CoffeeProduct
from src.game_mechanics.game_object import GameObject
from src.game_mechanics.tap import Tap
from src.game_mechanics.tea_bag_spawn import TeaBagSpawn
from src.guis.gui_texture import GuiTexture
from src.master.prefabs import plate
from src.render_engine.display_manager import DisplayManager
from src.render_engine.gui_renderer import GuiRenderer
from src.render_engine.master_renderer import MasterRenderer
from src.render_engine.loader import Loader
from src.render_engine.time import Time
from src.render_engine.input_controller import KeyboardInput

from src.textures.model_texture import ModelTexture
from src.models.textured_model import TexturedModel

from src.entities.entity import Entity
from src.entities.camera import Camera
from src.entities.light import Light
from src.entities.player import FirstPersonPlayer

from src.obj_converter.obj_loader import OBJLoader, NormalMappedOBJLoader

import src.master.prefabs as prefabs

from src.game_mechanics.coffee_page import CoffeePage


def main():
    # ~~~~~~~~~~~~DISPLAY~~~~~~~~~~~~~~
    display = DisplayManager(1920, 1080)
    display.create_display("An-gine")  # creates display
    display.set_backdrop_color(173, 216, 230)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    audio_master = AudioMaster()
    audio_master.set_listener_data([0, 0, 0], [0, 0, 0])

    # ~~~~~~~~~~~~LOADERS~~~~~~~~~~~~~~
    loader = Loader()
    obj_loader = OBJLoader()
    normal_mapped_obj_loader = NormalMappedOBJLoader()
    CoffeeContainer.add_loaders(loader, obj_loader)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~PLAYER~~~~~~~~~~~~~~
    bunny_model = obj_loader.load_obj_model("bunny", loader)
    static_bunny_model = TexturedModel(bunny_model, ModelTexture(loader.load_texture("white")))

    player = FirstPersonPlayer(static_bunny_model, [50, 0, 66], 0, 0, 0, 3)
    player.set_player_size(14)
    camera = Camera(player)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    TextMaster(loader)

    # ~~~~~~~~~~~RENDERER~~~~~~~~~~~~~~~
    master_renderer = MasterRenderer(loader, camera)
    master_renderer.set_fog_density(0.0035)
    master_renderer.set_fog_gradient(5)
    master_renderer.get_shadow_map_texture()

    gui_renderer = GuiRenderer(loader)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    entities = []
    collider_entities = []

    CoffeeProduct(f"Espresso",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=6,
                  allows_double=False,
                  container_type=CoffeeProduct.ESPRESSO_CUP,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/coffee_filling_tex")),
                  content=["Espresso"])
    CoffeeProduct(f"Doppio",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.COFFEE_CUP,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/coffee_filling_tex")),
                  content=["Espresso", "Espresso"])
    CoffeeProduct(f"Cafe Creme",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.COFFEE_CUP,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/coffee_creme_filling_tex")),
                  content=["Cafe Creme"])
    CoffeeProduct(f"2 Cafe Creme",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=10,
                  allows_double=True,
                  container_type=CoffeeProduct.COFFEE_CUP,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/coffee_creme_filling_tex")),
                  content=["Cafe Creme", "Cafe Creme"])
    CoffeeProduct(f"Milk Coffee",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.COFFEE_CUP,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/milk_coffee_filling_tex")),
                  content=["Milk Coffee"])
    CoffeeProduct(f"2 Milk Coffee",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=10,
                  allows_double=True,
                  container_type=CoffeeProduct.COFFEE_CUP,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/milk_coffee_filling_tex")),
                  content=["Milk Coffee", "Milk Coffee"])
    CoffeeProduct(f"Cappuccino",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.CAPPUCCINO_CUP,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/cappuccino_filling_tex")),
                  content=["Cappuccino"])
    CoffeeProduct(f"2 Cappuccini",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=10,
                  allows_double=True,
                  container_type=CoffeeProduct.CAPPUCCINO_CUP,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/cappuccino_filling_tex")),
                  content=["Cappuccino", "Cappuccino"])
    CoffeeProduct(f"Latte Macchiato",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.BIG_GLASS,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/latte_macchiato_filling_tex")),
                  content=["Latte Macchiato"])
    CoffeeProduct(f"Cafe Latte",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.BIG_GLASS,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/latte_macchiato_filling_tex")),
                  content=["Cafe Latte"])
    CoffeeProduct(f"Tea",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=18,
                  allows_double=False,
                  container_type=CoffeeProduct.TEA_POT,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/tea_filling_tex")),
                  content=["Tea"])
    CoffeeProduct(f"Hot Chocolate",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.BIG_GLASS,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/chocolate_filling_tex")),
                  content=["Hot Chocolate"])
    CoffeeProduct(f"Cold Chocolate",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.BIG_GLASS,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/chocolate_filling_tex")),
                  content=["Cold Chocolate"])
    CoffeeProduct(f"Children Chocolate",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=6,
                  allows_double=False,
                  container_type=CoffeeProduct.SMALL_GLASS,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/chocolate_filling_tex")),
                  content=["Children Chocolate"])
    CoffeeProduct(f"Milk for Chai, Ovo",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.BIG_GLASS,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/milk_filling_tex")),
                  content=["Milk for Chai, Ovo"])
    CoffeeProduct(f"Warm Milk",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.BIG_GLASS,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/milk_filling_tex")),
                  content=["Warm Milk"])
    CoffeeProduct(f"Cold Milk",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.BIG_GLASS,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/milk_filling_tex")),
                  content=["Cold Milk"])
    CoffeeProduct(f"Babyccino",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=6,
                  allows_double=False,
                  container_type=CoffeeProduct.SMALL_GLASS,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/milk_foam_filling_tex")),
                  content=["Babyccino"])
    CoffeeProduct(f"Americano",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.CAPPUCCINO_CUP,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/coffee_filling_tex")),
                  content=["Americano"])
    CoffeeProduct(f"Doppio Macchiato",
                  GuiTexture(loader.load_texture("product_icon_test"),
                             [0, 0],
                             [1, 1]),
                  brew_length=8,
                  allows_double=False,
                  container_type=CoffeeProduct.COFFEE_CUP,
                  loader=loader,
                  texture=ModelTexture(loader.load_texture("pngs/cups/latte_macchiato_filling_tex")),
                  content=["Doppio Macchiato"])

    products = CoffeePage.get_products(CoffeePage.get_instances()[1])

    # small_coffee_game_object = prefabs.coffee_cup([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader)
    # big_coffee_game_object = prefabs.cappuccino_cup([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader)
    # tea_pot_game_object = prefabs.tea([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader)
    # small_glass_game_object = prefabs.small_glass([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader)
    # big_glass_game_object = prefabs.big_glass([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader)
    # espresso_cup_game_object = prefabs.espresso_cup([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader)
    # entities.extend([small_coffee_game_object, big_coffee_game_object, tea_pot_game_object, small_glass_game_object,
    #                 big_glass_game_object, espresso_cup_game_object])

    coffee_machine_model = obj_loader.load_obj_model("objs/machinery/coffee_machine", loader)
    coffee_machine_texture = ModelTexture(loader.load_texture("pngs/machinery/coffee_machine_tex"))
    coffee_machine_texture.set_shine_damper(10)
    coffee_machine_texture.set_reflectivity(0.1)
    static_coffee_machine_model = TexturedModel(coffee_machine_model, coffee_machine_texture)
    static_coffee_machine_collider = TexturedModel(
        obj_loader.load_obj_model("objs/machinery/coffee_machine_collider", loader),
        ModelTexture(loader.load_texture("")))

    coffee_machine_screen_model = obj_loader.load_obj_model("objs/machinery/coffee_machine_screen", loader)
    coffee_machine_screen_texture = ModelTexture(loader.load_texture("pngs/machinery/white"))
    coffee_machine_screen_texture.set_shine_damper(10)
    coffee_machine_screen_texture.set_reflectivity(0.5)
    static_coffee_machine_screen_model = TexturedModel(coffee_machine_screen_model, coffee_machine_screen_texture)

    machine = Entity(static_coffee_machine_model,[50, 10.5, 60], 0, 10, 0, 0.7)
    coffee_machine_collider = Entity(static_coffee_machine_collider, [50, 10.5, 60], 0, 10, 0, 1)
    coffee_machine_screen = Entity(static_coffee_machine_screen_model, [50, 10.5, 60], 0, 10, 0, 0.7)
    coffee_machine_game_object = GameObject(machine, coffee_machine_screen, int_name=CoffeeMachineOS.get_name(),
                                            collider=coffee_machine_collider)

    entities.append(coffee_machine_game_object)
    entities.append(prefabs.mixer([50, 10.5, 60], [0, 10, 0], 0.5, loader, obj_loader))
    entities.append(prefabs.mixer_vessel([50, 10.5, 60], [0, 10, 0], 0.5, loader, obj_loader))
    milk_foamer_vessel_model = obj_loader.load_obj_model("objs/machinery/milk_foamer_vessel", loader)
    milk_foamer_vessel_texture = ModelTexture(loader.load_texture("pngs/machinery/milk_foamer_vessel_tex"))
    milk_foamer_vessel_texture.set_reflectivity(0.75)
    static_milk_foamer_vessel_model = TexturedModel(milk_foamer_vessel_model, milk_foamer_vessel_texture)
    static_milk_foamer_vessel_collider = TexturedModel(
        obj_loader.load_obj_model("objs/machinery/milk_foamer_vessel_collider", loader),
        ModelTexture(loader.load_texture("")))

    milk_foamer_screen_model = obj_loader.load_obj_model("objs/machinery/milk_foamer_screen", loader)
    milk_foamer_screen_texture = ModelTexture(loader.load_texture("pngs/machinery/black"))
    static_milk_foamer_screen_model = TexturedModel(milk_foamer_screen_model, milk_foamer_screen_texture)

    milk_foamer_cup_model = obj_loader.load_obj_model("objs/machinery/milk_foamer_cup", loader)
    milk_foamer_cup_texture = ModelTexture(loader.load_texture("pngs/machinery/milk_foamer_cup_tex"))
    milk_foamer_cup_texture.set_reflectivity(0.75)
    static_milk_foamer_cup_model = TexturedModel(milk_foamer_cup_model, milk_foamer_cup_texture)
    static_milk_foamer_cup_collider = TexturedModel(
        obj_loader.load_obj_model("objs/machinery/milk_foamer_cup_collider", loader),
        ModelTexture(loader.load_texture("")))

    milk_foamer_rotator_model = obj_loader.load_obj_model("objs/machinery/milk_foamer_rotator", loader)
    milk_foamer_rotator_texture = ModelTexture(loader.load_texture("pngs/machinery/milk_foamer_rotator_tex"))
    static_milk_foamer_rotator_model = TexturedModel(milk_foamer_rotator_model, milk_foamer_rotator_texture)

    milk_foamer_lid_model = obj_loader.load_obj_model("objs/machinery/milk_foamer_lid", loader)
    milk_foamer_lid_texture = ModelTexture(loader.load_texture("pngs/machinery/milk_foamer_lid_tex"))
    milk_foamer_lid_texture.set_reflectivity(0.75)
    static_milk_foamer_lid_model = TexturedModel(milk_foamer_lid_model, milk_foamer_lid_texture)
    static_milk_foamer_lid_collider = TexturedModel(
        obj_loader.load_obj_model("objs/machinery/milk_foamer_lid_collider", loader),
        ModelTexture(loader.load_texture("")))

    milk_foamer_vessel = Entity(static_milk_foamer_vessel_model, [50, 10.5, 60], *[0, 10, 0], 1)
    milk_foamer_vessel_collider = Entity(static_milk_foamer_vessel_collider, [50, 10.5, 60], *[0, 10, 0], 1)
    milk_foamer_screen = Entity(static_milk_foamer_screen_model, [50, 10.5, 60], *[0, 10, 0], 1)
    milk_foamer_cup = Entity(static_milk_foamer_cup_model, [50, 10.5, 60], *[0, 10, 0], 1)
    milk_foamer_cup_collider = Entity(static_milk_foamer_cup_collider, [50, 10.5, 60], *[0, 10, 0], 1)
    milk_foamer_rotator = Entity(static_milk_foamer_rotator_model, [50, 10.5, 60], *[0, 10, 0], 1)
    milk_foamer_lid = Entity(static_milk_foamer_lid_model, [50, 10.5, 60], *[0, 10, 0], 1)
    milk_foamer_lid_collider = Entity(static_milk_foamer_lid_collider, [50, 10.5, 60], *[0, 10, 0], 1)

    milk_foamer_game_object = GameObject(milk_foamer_vessel, child_0=milk_foamer_lid, child_1=milk_foamer_cup,
                                         collider=milk_foamer_vessel_collider,
                                         int_name="MILK_FOAMER_VESSEL")
    entities.append(milk_foamer_game_object)
    entities.append(prefabs.plate([50, 10.5, 60], [0, 10, 0], 0.5, loader, obj_loader))
    entities.append(prefabs.oat_milk([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader))
    entities.append(prefabs.lactose_free_milk([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader))
    entities.append(prefabs.chai_bottle([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader))
    entities.append(prefabs.orange_juice([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader))
    entities.append(prefabs.topfit_juice([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader))
    entities.append(prefabs.prosecco_bottle([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader))
    entities.append(prefabs.prosecco_glass([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader))
    entities.append(prefabs.sprite([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader))
    entities.append(prefabs.beer([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader))
    textures = [ModelTexture(loader.load_texture("pngs/cups/coke_filling_tex")),
                ModelTexture(loader.load_texture("pngs/cups/schorle_filling_tex")),
                ModelTexture(loader.load_texture("pngs/cups/water_filling_tex")),
                ModelTexture(loader.load_texture("pngs/cups/water_filling_tex")),
                ModelTexture(loader.load_texture("pngs/cups/beer_filling_tex"))]
    tap = Tap(obj_loader, loader, [50, 10.5, 60], [0, 10, 0], 0.7, textures).get_game_objects()
    entities.append(prefabs.caotina([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader))
    entities.append(prefabs.ovomaltine([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader))
    entities.append(prefabs.chocolatl([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader))


    for product in products:
        container = product.get_container_type()
        if container == CoffeeProduct.ESPRESSO_CUP:
            e1 = prefabs.espresso_cup([50, 10.5, 60], [0, 10, 0], 2, loader, obj_loader)
            entities.append(e1)
        if container == CoffeeProduct.COFFEE_CUP:
            e1 = prefabs.coffee_cup([50, 10.5, 60], [0, 10, 0], 2, loader, obj_loader)
            entities.append(e1)
        if container == CoffeeProduct.CAPPUCCINO_CUP:
            e1 = prefabs.cappuccino_cup([50, 10.5, 60], [0, 10, 0], 2, loader, obj_loader)
            entities.append(e1)
        if container == CoffeeProduct.SMALL_GLASS:
            e1 = prefabs.small_glass([50, 10.5, 60], [0, 10, 0], 2, loader, obj_loader)
            entities.append(e1)
        if container == CoffeeProduct.BIG_GLASS:
            e1 = prefabs.big_glass([50, 10.5, 60], [0, 10, 0], 2, loader, obj_loader)
            for i in range(3): e1.get_attachment().fill(product.get_texture())
            entities.append(e1)
        if container == CoffeeProduct.TEA_POT:
            e1 = prefabs.tea([50, 10.5, 60], [0, 10, 0], 2, loader, obj_loader)
            entities.append(e1)

    prefabs.egg_sandwich([50, 10.5, 60], [0, 10, 0], 0.5, loader, obj_loader, entities, collider_entities)
    prefabs.earl_grey([50, 10.5, 60], [0, 190, 0], 1, loader, obj_loader, entities, collider_entities)

    collider_entities.extend(entities.copy())
    print("finished loading assets")
    # ~~~~~~~~~~~~LIGHTS~~~~~~~~~~~~~~~~
    sun = Light([-100000, 150000, 100000], [1, 1, 1])
    lights = [sun]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    i = 0
    while glutGetWindow() != 0:
        # game logic
        Time.set_current_time(Time.time_current_time())
        Time.set_delta_time()  # automatically calculates delta time
        Time.set_last_frame_time(Time.time_current_time())

        fps = 1 / Time.get_delta_time()

        player.move([])
        camera.move()

        if KeyboardInput.on_key_down(b'r'):
            i += 1

        master_renderer.render_shadow_map([entities[i % len(entities)]], sun)

        master_renderer.render_scene([entities[i % len(entities)]], [], [], lights, camera, display)

        glutSwapBuffers()  # needs to be called AFTER finished drawing
        glutMainLoopEvent()  # used to run openGL manually in a loop instead of glutMainLoop()


if __name__ == "__main__":
    main()
