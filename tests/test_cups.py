from OpenGL.GLUT import *

from src.font_rendering.text_master import TextMaster
from src.game_mechanics.coffee_container import CoffeeContainer
from src.game_mechanics.coffee_product import CoffeeProduct
from src.guis.gui_texture import GuiTexture
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

    # ~~~~~~~~~~~~LOADERS~~~~~~~~~~~~~~
    loader = Loader()
    obj_loader = OBJLoader()
    normal_mapped_obj_loader = NormalMappedOBJLoader()
    CoffeeContainer.add_loaders(loader, obj_loader)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~PLAYER~~~~~~~~~~~~~~
    bunny_model = obj_loader.load_obj_model("bunny", loader)
    static_bunny_model = TexturedModel(bunny_model, ModelTexture(loader.load_texture("white")))

    player = FirstPersonPlayer(static_bunny_model, [50, 0, 62], 0, 0, 0, 3)
    player.set_player_size(12)
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

    for product in products:
        container = product.get_container_type()
        if container == CoffeeProduct.ESPRESSO_CUP:
            e1 = prefabs.espresso_cup([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader)
            for i in range(3): e1.get_attachment().fill(product.get_texture())
            entities.append(e1)
        if container == CoffeeProduct.COFFEE_CUP:
            e1 = prefabs.coffee_cup([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader)
            for i in range(3): e1.get_attachment().fill(product.get_texture())
            entities.append(e1)
        if container == CoffeeProduct.CAPPUCCINO_CUP:
            e1 = prefabs.cappuccino_cup([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader)
            for i in range(3): e1.get_attachment().fill(product.get_texture())
            entities.append(e1)
        if container == CoffeeProduct.SMALL_GLASS:
            e1 = prefabs.small_glass([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader)
            for i in range(3): e1.get_attachment().fill(product.get_texture())
            entities.append(e1)
        if container == CoffeeProduct.BIG_GLASS:
            e1 = prefabs.big_glass([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader)
            for i in range(3): e1.get_attachment().fill(product.get_texture())
            entities.append(e1)
        if container == CoffeeProduct.TEA_POT:
            e1 = prefabs.tea([50, 10.5, 60], [0, 10, 0], 1, loader, obj_loader)
            for i in range(3): e1.get_attachment().fill(product.get_texture())
            entities.append(e1)

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
