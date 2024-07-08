from src.entities.entity import Entity
from src.game_mechanics.coffee_container import CoffeeContainer
from src.game_mechanics.coffee_machine_os import CoffeeMachineOS, CoffeeMachineOSLactoseFree
from src.game_mechanics.food import Food
from src.game_mechanics.food_spawn import FoodSpawn
from src.game_mechanics.fridge import Fridge
from src.game_mechanics.fridge_object import FridgeObject
from src.game_mechanics.game_object import GameObject
from src.game_mechanics.ingredient import Ingredient
from src.game_mechanics.milk_foamer import MilkFoamer
from src.game_mechanics.mixer import Mixer
from src.game_mechanics.mixer_vessel import MixerVessel
from src.models.textured_model import TexturedModel
from src.obj_converter.obj_loader import OBJLoader
from src.post_processing.fbo import FBO
from src.render_engine.loader import Loader
from src.textures.model_texture import ModelTexture


def coffee_machine(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                   gui_renderer, object_picker) -> GameObject:
    coffee_machine_model = obj_loader.load_obj_model("coffee_machine", loader)
    coffee_machine_texture = ModelTexture(loader.load_texture("coffee_machine_texture"))
    coffee_machine_texture.set_shine_damper(10)
    coffee_machine_texture.set_reflectivity(0.5)
    static_coffee_machine_model = TexturedModel(coffee_machine_model, coffee_machine_texture)
    static_coffee_machine_collider = TexturedModel(obj_loader.load_obj_model("coffee_machine_collider", loader),
                                                   ModelTexture(loader.load_texture("")))

    coffee_machine_screen_model = obj_loader.load_obj_model("coffee_machine_screen", loader)
    coffee_machine_screen_texture = ModelTexture(loader.load_texture("white"))
    coffee_machine_screen_texture.set_shine_damper(10)
    coffee_machine_screen_texture.set_reflectivity(0.5)
    static_coffee_machine_screen_model = TexturedModel(coffee_machine_screen_model, coffee_machine_screen_texture)

    machine = Entity(static_coffee_machine_model, pos, *rot, size)
    coffee_machine_collider = Entity(static_coffee_machine_collider, pos, *rot, size)
    coffee_machine_screen = Entity(static_coffee_machine_screen_model, pos, *rot, size)
    coffee_machine_game_object = GameObject(machine, coffee_machine_screen, int_name=CoffeeMachineOS.get_name(),
                                            collider=coffee_machine_collider)
    coffee_machine_game_object.set_pickup_able(False)
    coffee_machine_game_object.set_prompt("Press the 'F' Key to interact.")

    coffee_fbo = FBO(1920, 1080, multi_target=False, depth_buffer_type=FBO.DEPTH_TEXTURE)
    coffee_os = CoffeeMachineOS(coffee_machine_screen, loader, obj_loader, coffee_fbo, gui_renderer, object_picker)
    coffee_machine_game_object.set_attachment(coffee_os)

    return coffee_machine_game_object


def lactose_free_coffee_machine(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                                gui_renderer, object_picker) -> GameObject:
    coffee_machine_model = obj_loader.load_obj_model("coffee_machine", loader)
    coffee_machine_texture = ModelTexture(loader.load_texture("coffee_machine_texture"))
    coffee_machine_texture.set_shine_damper(10)
    coffee_machine_texture.set_reflectivity(0.5)
    static_coffee_machine_model = TexturedModel(coffee_machine_model, coffee_machine_texture)
    static_coffee_machine_collider = TexturedModel(obj_loader.load_obj_model("coffee_machine_collider", loader),
                                                   ModelTexture(loader.load_texture("")))

    coffee_machine_screen_model = obj_loader.load_obj_model("coffee_machine_screen", loader)
    coffee_machine_screen_texture = ModelTexture(loader.load_texture("white"))
    coffee_machine_screen_texture.set_shine_damper(10)
    coffee_machine_screen_texture.set_reflectivity(0.5)
    static_coffee_machine_screen_model = TexturedModel(coffee_machine_screen_model, coffee_machine_screen_texture)

    coffee_machine_lactose_free = Entity(static_coffee_machine_model, pos, *rot, size)
    coffee_machine_lactose_free_collider = Entity(static_coffee_machine_collider, pos, *rot, size)
    coffee_machine_lactose_free_screen = Entity(static_coffee_machine_screen_model, pos, *rot, size)
    coffee_machine_lactose_free_game_object = GameObject(coffee_machine_lactose_free,
                                                         coffee_machine_lactose_free_screen,
                                                         int_name=CoffeeMachineOSLactoseFree.get_name(),
                                                         collider=coffee_machine_lactose_free_collider)
    coffee_machine_lactose_free_game_object.set_pickup_able(False)
    coffee_machine_lactose_free_game_object.set_prompt("Press the 'F' Key to interact.")

    lactose_free_coffee_fbo = FBO(1920, 1080, multi_target=False, depth_buffer_type=FBO.DEPTH_TEXTURE)
    coffee_os_lactose_free = CoffeeMachineOSLactoseFree(coffee_machine_lactose_free_screen, loader, obj_loader,
                                                        lactose_free_coffee_fbo, gui_renderer, object_picker)
    coffee_machine_lactose_free_game_object.set_attachment(coffee_os_lactose_free)

    return coffee_machine_lactose_free_game_object


def fridge(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
           gui_renderer, object_picker) -> GameObject:
    fridge_case_model = obj_loader.load_obj_model("fridge_case", loader)
    fridge_case_texture = ModelTexture(loader.load_texture("counter"))
    fridge_case_texture.set_shine_damper(10)
    fridge_case_texture.set_reflectivity(0.5)
    static_fridge_case_model = TexturedModel(fridge_case_model, fridge_case_texture)
    static_fridge_case_collider = TexturedModel(obj_loader.load_obj_model("case_collider", loader),
                                                ModelTexture(loader.load_texture("")))

    fridge_top_drawer_model = obj_loader.load_obj_model("fridge_top_drawer", loader)
    fridge_top_drawer_texture = ModelTexture(loader.load_texture("drawer"))
    fridge_top_drawer_texture.set_shine_damper(10)
    fridge_top_drawer_texture.set_reflectivity(0.5)
    static_fridge_top_drawer_model = TexturedModel(fridge_top_drawer_model, fridge_top_drawer_texture)
    static_fridge_top_drawer_collider = TexturedModel(obj_loader.load_obj_model("top_drawer_collider", loader),
                                                      ModelTexture(loader.load_texture("")))

    fridge_bottom_drawer_model = obj_loader.load_obj_model("fridge_bottom_drawer", loader)
    fridge_bottom_drawer_texture = ModelTexture(loader.load_texture("drawer"))
    fridge_bottom_drawer_texture.set_shine_damper(10)
    fridge_bottom_drawer_texture.set_reflectivity(0.5)
    static_fridge_bottom_drawer_model = TexturedModel(fridge_bottom_drawer_model, fridge_bottom_drawer_texture)
    static_fridge_bottom_drawer_collider = TexturedModel(obj_loader.load_obj_model("bottom_drawer_collider", loader),
                                                         ModelTexture(loader.load_texture("")))

    fridge_case = Entity(static_fridge_case_model, pos, *rot, size)
    fridge_case_collider = Entity(static_fridge_case_collider, pos, *rot, size)
    fridge_top_drawer = Entity(static_fridge_top_drawer_model, pos, *rot, size)
    fridge_top_drawer_collider = Entity(static_fridge_top_drawer_collider, pos, *rot, size)
    fridge_bottom_drawer = Entity(static_fridge_bottom_drawer_model, pos, *rot, size)
    fridge_bottom_drawer_collider = Entity(static_fridge_bottom_drawer_collider, pos, *rot, size)

    fridge_game_object = GameObject(fridge_case, child_0=fridge_top_drawer, child_1=fridge_bottom_drawer,
                                    collider=fridge_case_collider)
    fridge_game_object.set_pickup_able(False)
    fridge_game_object.get_child_0().set_collider(fridge_top_drawer_collider)
    fridge_game_object.get_child_1().set_collider(fridge_bottom_drawer_collider)
    fridge_game_object.get_child_0().set_int_name("TOP_DRAWER")
    fridge_game_object.get_child_1().set_int_name("BOTTOM_DRAWER")
    fridge_game_object.get_child_0().set_prompt("Press 'E' or 'Q' to open. Press the 'F' Key to interact.")
    fridge_game_object.get_child_1().set_prompt("Press 'E' or 'Q' to open. Press the 'F' Key to interact.")

    fri = Fridge(fridge_game_object.get_child_0(), fridge_game_object.get_child_1(), object_picker, loader,
                 gui_renderer)
    fridge_game_object.get_child_0().set_attachment(fri)
    fridge_game_object.get_child_1().set_attachment(fri)

    return fridge_game_object


def milk_foamer(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                gui_renderer, object_picker) -> GameObject:
    milk_foamer_vessel_model = obj_loader.load_obj_model("milk_foamer_vessel", loader)
    milk_foamer_vessel_texture = ModelTexture(loader.load_texture("milk_foamer_vessel_tex"))
    milk_foamer_vessel_texture.set_reflectivity(0.75)
    static_milk_foamer_vessel_model = TexturedModel(milk_foamer_vessel_model, milk_foamer_vessel_texture)
    static_milk_foamer_vessel_collider = TexturedModel(obj_loader.load_obj_model("milk_foamer_vessel_collider", loader),
                                                       ModelTexture(loader.load_texture("")))

    milk_foamer_screen_model = obj_loader.load_obj_model("milk_foamer_screen", loader)
    milk_foamer_screen_texture = ModelTexture(loader.load_texture("black"))
    static_milk_foamer_screen_model = TexturedModel(milk_foamer_screen_model, milk_foamer_screen_texture)

    milk_foamer_cup_model = obj_loader.load_obj_model("milk_foamer_cup", loader)
    milk_foamer_cup_texture = ModelTexture(loader.load_texture("milk_foamer_cup_tex"))
    milk_foamer_cup_texture.set_reflectivity(0.75)
    static_milk_foamer_cup_model = TexturedModel(milk_foamer_cup_model, milk_foamer_cup_texture)
    static_milk_foamer_cup_collider = TexturedModel(obj_loader.load_obj_model("milk_foamer_cup_collider", loader),
                                                    ModelTexture(loader.load_texture("")))

    milk_foamer_rotator_model = obj_loader.load_obj_model("milk_foamer_rotator", loader)
    milk_foamer_rotator_texture = ModelTexture(loader.load_texture("milk_foamer_rotator_tex"))
    static_milk_foamer_rotator_model = TexturedModel(milk_foamer_rotator_model, milk_foamer_rotator_texture)

    milk_foamer_lid_model = obj_loader.load_obj_model("milk_foamer_lid", loader)
    milk_foamer_lid_texture = ModelTexture(loader.load_texture("milk_foamer_lid_tex"))
    milk_foamer_lid_texture.set_reflectivity(0.75)
    static_milk_foamer_lid_model = TexturedModel(milk_foamer_lid_model, milk_foamer_lid_texture)
    static_milk_foamer_lid_collider = TexturedModel(obj_loader.load_obj_model("milk_foamer_lid_collider", loader),
                                                    ModelTexture(loader.load_texture("")))

    milk_foamer_vessel = Entity(static_milk_foamer_vessel_model, pos, *rot, size)
    milk_foamer_vessel_collider = Entity(static_milk_foamer_vessel_collider, pos, *rot, size)
    milk_foamer_screen = Entity(static_milk_foamer_screen_model, pos, *rot, size)
    milk_foamer_cup = Entity(static_milk_foamer_cup_model, pos, *rot, size)
    milk_foamer_cup_collider = Entity(static_milk_foamer_cup_collider, pos, *rot, size)
    milk_foamer_rotator = Entity(static_milk_foamer_rotator_model, pos, *rot, size)
    milk_foamer_lid = Entity(static_milk_foamer_lid_model, pos, *rot, size)
    milk_foamer_lid_collider = Entity(static_milk_foamer_lid_collider, pos, *rot, size)

    milk_foamer_game_object = GameObject(milk_foamer_vessel, child_0=milk_foamer_lid, child_1=milk_foamer_cup,
                                         collider=milk_foamer_vessel_collider,
                                         int_name="MILK_FOAMER_VESSEL")
    milk_foamer_game_object.set_pickup_able(False)
    milk_foamer_game_object.set_prompt("Press 'F' to interact")
    milk_foamer_game_object.get_child_0().set_collider(milk_foamer_lid_collider)
    milk_foamer_game_object.get_child_0().set_int_name("MILK_FOAMER_LID")
    milk_foamer_game_object.get_child_1().set_collider(milk_foamer_cup_collider)
    milk_foamer_game_object.get_child_1().set_int_name("MILK_FOAMER_CUP")
    milk_foamer_game_object.get_child_1().set_child_0(milk_foamer_rotator)

    milk_fbo = FBO(1920, 1080, multi_target=False, depth_buffer_type=FBO.DEPTH_TEXTURE)
    milk_foamer_os = MilkFoamer(milk_foamer_game_object, milk_foamer_screen, loader, obj_loader, milk_fbo, gui_renderer,
                                object_picker)
    milk_foamer_game_object.set_attachment(milk_foamer_os)
    milk_foamer_game_object.get_child_0().set_attachment(milk_foamer_os)
    milk_foamer_game_object.get_child_1().set_attachment(milk_foamer_os)

    return milk_foamer_game_object


def mixer(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    mixer_model = obj_loader.load_obj_model("mixer", loader)
    mixer_texture = ModelTexture(loader.load_texture(""))
    mixer_texture.set_reflectivity(0.75)
    static_mixer_model = TexturedModel(mixer_model, mixer_texture)
    static_mixer_collider = TexturedModel(obj_loader.load_obj_model("mixer_collider", loader),
                                          ModelTexture(loader.load_texture("")))

    mix = Entity(static_mixer_model, pos, *rot, size)
    mixer_collider = Entity(static_mixer_collider, pos, *rot, size)
    mixer_game_object = GameObject(mix, collider=mixer_collider, int_name="MIXER")
    mixer_game_object.set_pickup_able(False)

    mixer_os = Mixer(mixer_game_object)
    mixer_game_object.set_attachment(mixer_os)

    return mixer_game_object


def mixer_vessel(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    mixer_vessel_model = obj_loader.load_obj_model("mixer_vessel", loader)
    mixer_vessel_texture = ModelTexture(loader.load_texture(""))
    mixer_vessel_texture.set_reflectivity(0.75)
    static_mixer_vessel_model = TexturedModel(mixer_vessel_model, mixer_vessel_texture)
    static_mixer_vessel_collider = TexturedModel(obj_loader.load_obj_model("mixer_vessel_collider", loader),
                                                 ModelTexture(loader.load_texture("")))

    mix_vessel = Entity(static_mixer_vessel_model, pos, *rot, size)
    mixer_vessel_collider = Entity(static_mixer_vessel_collider, pos, *rot, size)
    mixer_vessel_game_object = GameObject(mix_vessel, collider=mixer_vessel_collider, int_name="MIXER_VESSEL")

    mixer_vessel_os = MixerVessel(mixer_vessel_game_object, obj_loader, loader)
    mixer_vessel_game_object.set_attachment(mixer_vessel_os)
    mixer_vessel_game_object.set_info(mixer_vessel_os.get_content())

    return mixer_vessel_game_object


def espresso_cup(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    small_coffee_texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    small_coffee_texture.set_shine_damper(10)
    small_coffee_texture.set_reflectivity(0.5)

    espresso_model = obj_loader.load_obj_model("espresso_cup", loader)
    static_espresso_model = TexturedModel(espresso_model, small_coffee_texture)
    static_espresso_collider = TexturedModel(obj_loader.load_obj_model("espresso_cup_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    esp_cup = Entity(static_espresso_model, pos, *rot, size)
    espresso_cup_collider = Entity(static_espresso_collider, pos, *rot, size)
    espresso_cup_game_object = GameObject(esp_cup, int_name="COFFEE", collider=espresso_cup_collider)
    espresso_cup_game_object.set_attachment(CoffeeContainer(CoffeeContainer.ESPRESSO_CUP, espresso_cup_game_object))
    espresso_cup_game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return espresso_cup_game_object


def coffee_cup(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    small_coffee_model = obj_loader.load_obj_model("small_coffee_cup", loader)
    small_coffee_texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    small_coffee_texture.set_shine_damper(10)
    small_coffee_texture.set_reflectivity(0.5)
    static_small_coffee_model = TexturedModel(small_coffee_model, small_coffee_texture)
    static_small_coffee_collider = TexturedModel(obj_loader.load_obj_model("small_coffee_cup_collider", loader),
                                                 ModelTexture(loader.load_texture("")))

    small_coffee = Entity(static_small_coffee_model, pos, *rot, size)
    small_coffee_collider = Entity(static_small_coffee_collider, pos, *rot, size)
    small_coffee_game_object = GameObject(small_coffee, int_name="COFFEE", collider=small_coffee_collider)
    small_coffee_game_object.set_attachment(CoffeeContainer(CoffeeContainer.COFFEE_CUP, small_coffee_game_object))
    small_coffee_game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return small_coffee_game_object


def cappuccino_cup(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    small_coffee_texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    small_coffee_texture.set_shine_damper(10)
    small_coffee_texture.set_reflectivity(0.5)

    big_coffee_model = obj_loader.load_obj_model("big_coffee_cup", loader)
    static_big_coffee_model = TexturedModel(big_coffee_model, small_coffee_texture)
    static_big_coffee_collider = TexturedModel(obj_loader.load_obj_model("big_coffee_cup_collider", loader),
                                               ModelTexture(loader.load_texture("")))

    big_coffee = Entity(static_big_coffee_model, pos, *rot, size)
    big_coffee_collider = Entity(static_big_coffee_collider, pos, *rot, size)
    big_coffee_game_object = GameObject(big_coffee, int_name="COFFEE", collider=big_coffee_collider)
    big_coffee_game_object.set_attachment(CoffeeContainer(CoffeeContainer.CAPPUCCINO_CUP, big_coffee_game_object))
    big_coffee_game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return big_coffee_game_object


def big_glass(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    small_coffee_texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    small_coffee_texture.set_shine_damper(10)
    small_coffee_texture.set_reflectivity(0.5)

    big_glass_model = obj_loader.load_obj_model("big_glass", loader)
    static_big_glass_model = TexturedModel(big_glass_model, small_coffee_texture)
    static_big_glass_collider = TexturedModel(obj_loader.load_obj_model("big_glass_collider", loader),
                                              ModelTexture(loader.load_texture("")))

    big_gla = Entity(static_big_glass_model, pos, *rot, size)
    big_glass_collider = Entity(static_big_glass_collider, pos, *rot, size)
    big_glass_game_object = GameObject(big_gla, int_name="GLASS", collider=big_glass_collider)
    big_glass_game_object.set_attachment(CoffeeContainer(CoffeeContainer.BIG_GLASS, big_glass_game_object))
    big_glass_game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return big_glass_game_object


def small_glass(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    small_coffee_texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    small_coffee_texture.set_shine_damper(10)
    small_coffee_texture.set_reflectivity(0.5)

    small_glass_model = obj_loader.load_obj_model("small_glass", loader)
    static_small_glass_model = TexturedModel(small_glass_model, small_coffee_texture)
    static_small_glass_collider = TexturedModel(obj_loader.load_obj_model("small_glass_collider", loader),
                                                ModelTexture(loader.load_texture("")))

    small_gla = Entity(static_small_glass_model, pos, *rot, size)
    small_glass_collider = Entity(static_small_glass_collider, pos, *rot, size)
    small_glass_game_object = GameObject(small_gla, int_name="GLASS", collider=small_glass_collider)
    small_glass_game_object.set_attachment(CoffeeContainer(CoffeeContainer.SMALL_GLASS, small_glass_game_object))
    small_glass_game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return small_glass_game_object


def tea(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    small_coffee_texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    small_coffee_texture.set_shine_damper(10)
    small_coffee_texture.set_reflectivity(0.5)

    tea_pot_model = obj_loader.load_obj_model("tea_pot", loader)
    static_tea_pot_model = TexturedModel(tea_pot_model, small_coffee_texture)
    tea_pot_lid_model = obj_loader.load_obj_model("tea_pot_lid", loader)
    static_tea_pot_lid_model = TexturedModel(tea_pot_lid_model, small_coffee_texture)
    static_tea_pot_collider = TexturedModel(obj_loader.load_obj_model("tea_pot_collider", loader),
                                            ModelTexture(loader.load_texture("")))

    tea_pot = Entity(static_tea_pot_model, pos, *rot, size)
    tea_pot_lid = Entity(static_tea_pot_lid_model, pos, *rot, size)
    tea_pot_collider = Entity(static_tea_pot_collider, pos, *rot, size)
    tea_pot_game_object = GameObject(tea_pot, tea_pot_lid, int_name="TEA", collider=tea_pot_collider)
    tea_pot_game_object.set_attachment(CoffeeContainer(CoffeeContainer.TEA_POT, tea_pot_game_object))
    tea_pot_game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return tea_pot_game_object


def beer(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    beer_glass_texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    beer_glass_texture.set_shine_damper(10)
    beer_glass_texture.set_reflectivity(0.5)

    beer_model = obj_loader.load_obj_model("beer", loader)
    static_beer_model = TexturedModel(beer_model, beer_glass_texture)
    static_beer_collider = TexturedModel(obj_loader.load_obj_model("beer_collider", loader),
                                         ModelTexture(loader.load_texture("")))

    beer_glass = Entity(static_beer_model, pos, *rot, size)
    beer_collider = Entity(static_beer_collider, pos, *rot, size)
    beer_game_object = GameObject(beer_glass, int_name="GLASS", collider=beer_collider)
    beer_game_object.set_attachment(CoffeeContainer(CoffeeContainer.BEER, beer_game_object))
    beer_game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return beer_game_object


def prosecco_glass(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    prosecco_glass_texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    prosecco_glass_texture.set_shine_damper(10)
    prosecco_glass_texture.set_reflectivity(0.5)

    prosecco_model = obj_loader.load_obj_model("prosecco_glass", loader)
    static_prosecco_model = TexturedModel(prosecco_model, prosecco_glass_texture)
    static_prosecco_collider = TexturedModel(obj_loader.load_obj_model("prosecco_glass_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    prosecco_gla = Entity(static_prosecco_model, pos, *rot, size)
    prosecco_collider = Entity(static_prosecco_collider, pos, *rot, size)
    prosecco_game_object = GameObject(prosecco_gla, int_name="GLASS", collider=prosecco_collider)
    prosecco_game_object.set_attachment(CoffeeContainer(CoffeeContainer.PROSECCO, prosecco_game_object))
    prosecco_game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return prosecco_game_object


def prosecco_bottle(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    texture.set_shine_damper(10)
    texture.set_reflectivity(0.5)

    model = obj_loader.load_obj_model("prosecco", loader)
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("prosecco_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    filling_texture = ModelTexture(loader.load_texture("grass_block"))
    filling_texture.set_shine_damper(10)
    filling_texture.set_reflectivity(0.5)

    prosecco = Entity(static_model, pos, *rot, size)
    prosecco_collider = Entity(static_collider, pos, *rot, size)
    prosecco_game_object = GameObject(prosecco, int_name="FRIDGE", collider=prosecco_collider)
    prosecco_game_object.set_attachment(FridgeObject((1, 1), prosecco, filling_texture, "Prosecco"))
    prosecco_game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return prosecco_game_object


def chai_bottle(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    texture.set_shine_damper(10)
    texture.set_reflectivity(0.5)

    model = obj_loader.load_obj_model("chai", loader)
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("chai_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    filling_texture = ModelTexture(loader.load_texture("grass_block"))
    filling_texture.set_shine_damper(10)
    filling_texture.set_reflectivity(0.5)

    ent = Entity(static_model, pos, *rot, size)
    collider = Entity(static_collider, pos, *rot, size)
    game_object = GameObject(ent, int_name="FRIDGE", collider=collider)
    game_object.set_attachment(FridgeObject((1, 1), ent, filling_texture, "Chai"))
    game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return game_object


def coke_zero(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    texture.set_shine_damper(10)
    texture.set_reflectivity(0.5)

    model = obj_loader.load_obj_model("coke", loader)
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("coke_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    filling_texture = ModelTexture(loader.load_texture("grass_block"))
    filling_texture.set_shine_damper(10)
    filling_texture.set_reflectivity(0.5)

    ent = Entity(static_model, pos, *rot, size)
    collider = Entity(static_collider, pos, *rot, size)
    game_object = GameObject(ent, int_name="COKE", collider=collider)
    game_object.set_attachment(FridgeObject((1, 1), ent, filling_texture, "Coke Zero"))
    game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return game_object


def sprite(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    texture.set_shine_damper(10)
    texture.set_reflectivity(0.5)

    model = obj_loader.load_obj_model("sprite", loader)
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("sprite_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    filling_texture = ModelTexture(loader.load_texture("grass_block"))
    filling_texture.set_shine_damper(10)
    filling_texture.set_reflectivity(0.5)

    ent = Entity(static_model, pos, *rot, size)
    collider = Entity(static_collider, pos, *rot, size)
    game_object = GameObject(ent, int_name="SPRITE", collider=collider)
    game_object.set_attachment(FridgeObject((1, 1), ent, filling_texture, "Sprite"))
    game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return game_object


def orange_juice(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    texture.set_shine_damper(10)
    texture.set_reflectivity(0.5)

    model = obj_loader.load_obj_model("juice", loader)
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("juice_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    filling_texture = ModelTexture(loader.load_texture("grass_block"))
    filling_texture.set_shine_damper(10)
    filling_texture.set_reflectivity(0.5)

    ent = Entity(static_model, pos, *rot, size)
    collider = Entity(static_collider, pos, *rot, size)
    game_object = GameObject(ent, int_name="JUICE", collider=collider)
    game_object.set_attachment(FridgeObject((2, 1), ent, filling_texture, "Orange Juice"))
    game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return game_object


def topfit_juice(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    texture.set_shine_damper(10)
    texture.set_reflectivity(0.5)

    model = obj_loader.load_obj_model("juice", loader)
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("juice_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    filling_texture = ModelTexture(loader.load_texture("grass_block"))
    filling_texture.set_shine_damper(10)
    filling_texture.set_reflectivity(0.5)

    ent = Entity(static_model, pos, *rot, size)
    collider = Entity(static_collider, pos, *rot, size)
    game_object = GameObject(ent, int_name="JUICE", collider=collider)
    game_object.set_attachment(FridgeObject((2, 1), ent, filling_texture, "Topfit Juice"))
    game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return game_object


def milk_sac(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    milk_sac_texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    milk_sac_texture.set_shine_damper(10)
    milk_sac_texture.set_reflectivity(0.5)

    milk_sac_model = obj_loader.load_obj_model("milk_sac", loader)
    static_milk_sac_model = TexturedModel(milk_sac_model, milk_sac_texture)
    static_milk_sac_collider = TexturedModel(obj_loader.load_obj_model("milk_sac_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    filling_texture = ModelTexture(loader.load_texture("grass_block"))
    filling_texture.set_shine_damper(10)
    filling_texture.set_reflectivity(0.5)

    milk_sa = Entity(static_milk_sac_model, pos, *rot, size)
    milk_sac_collider = Entity(static_milk_sac_collider, pos, *rot, size)
    milk_sac_game_object = GameObject(milk_sa, int_name="FRIDGE", collider=milk_sac_collider)
    milk_sac_game_object.set_attachment(FridgeObject((3, 2), milk_sa, filling_texture, "Milk"))
    milk_sac_game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return milk_sac_game_object


def lactose_free_milk(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    milk_model = obj_loader.load_obj_model("milk", loader)
    milk_texture = ModelTexture(loader.load_texture("white"))
    milk_texture.set_shine_damper(10)
    milk_texture.set_reflectivity(0.5)
    static_milk_model = TexturedModel(milk_model, milk_texture)
    static_milk_collider = TexturedModel(obj_loader.load_obj_model("milk_collider", loader),
                                         ModelTexture(loader.load_texture("")))

    filling_texture = ModelTexture(loader.load_texture("white"))
    filling_texture.set_shine_damper(10)
    filling_texture.set_reflectivity(0.5)

    milk = Entity(static_milk_model, pos, *rot, size)
    milk_collider = Entity(static_milk_collider, pos, *rot, size)
    milk_game_object = GameObject(milk, int_name="MILK", collider=milk_collider)
    milk_game_object.set_attachment(FridgeObject((1, 1), milk, filling_texture, ["Milk", "Lactose Free"]))
    milk_game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return milk_game_object


def oat_milk(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    milk_model = obj_loader.load_obj_model("milk", loader)
    milk_texture = ModelTexture(loader.load_texture("white"))
    milk_texture.set_shine_damper(10)
    milk_texture.set_reflectivity(0.5)
    static_milk_model = TexturedModel(milk_model, milk_texture)
    static_milk_collider = TexturedModel(obj_loader.load_obj_model("milk_collider", loader),
                                         ModelTexture(loader.load_texture("")))

    filling_texture = ModelTexture(loader.load_texture("white"))
    filling_texture.set_shine_damper(10)
    filling_texture.set_reflectivity(0.5)

    milk = Entity(static_milk_model, pos, *rot, size)
    milk_collider = Entity(static_milk_collider, pos, *rot, size)
    milk_game_object = GameObject(milk, int_name="MILK", collider=milk_collider)
    milk_game_object.set_attachment(FridgeObject((1, 1), milk, filling_texture, "Oat Milk"))
    milk_game_object.set_prompt("Press 'E' or 'Q' to pick up.")

    return milk_game_object


def plate(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    plate_model = obj_loader.load_obj_model("plate", loader)
    plate_texture = ModelTexture(loader.load_texture("white"))
    static_plate_model = TexturedModel(plate_model, plate_texture)
    static_plate_collider = TexturedModel(obj_loader.load_obj_model("plate_collider", loader),
                                          ModelTexture(loader.load_texture("")))

    plat = Entity(static_plate_model, pos, *rot, size)
    plate_collider = Entity(static_plate_collider, pos, *rot, size)
    plate_game_object = GameObject(plat, int_name="PLATE", collider=plate_collider)

    return plate_game_object


def ham_sandwich(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                 entities: list, collider_entities: list) -> None:
    sandwich_model = obj_loader.load_obj_model("sandwich", loader)
    sandwich_texture = ModelTexture(loader.load_texture(""))
    static_sandwich_model = TexturedModel(sandwich_model, sandwich_texture)
    static_sandwich_collider = TexturedModel(obj_loader.load_obj_model("sandwich_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    sandwich = Food(static_sandwich_model, static_sandwich_collider, "Ham Sandwich")
    sandwich_spawn = FoodSpawn(sandwich, pos, rot, size, entities, collider_entities)


def salami_sandwich(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                    entities: list, collider_entities: list) -> None:
    sandwich_model = obj_loader.load_obj_model("sandwich", loader)
    sandwich_texture = ModelTexture(loader.load_texture(""))
    static_sandwich_model = TexturedModel(sandwich_model, sandwich_texture)
    static_sandwich_collider = TexturedModel(obj_loader.load_obj_model("sandwich_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    sandwich = Food(static_sandwich_model, static_sandwich_collider, "Salami Sandwich")
    sandwich_spawn = FoodSpawn(sandwich, pos, rot, size, entities, collider_entities)


def tuna_sandwich(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                  entities: list, collider_entities: list) -> None:
    sandwich_model = obj_loader.load_obj_model("sandwich", loader)
    sandwich_texture = ModelTexture(loader.load_texture(""))
    static_sandwich_model = TexturedModel(sandwich_model, sandwich_texture)
    static_sandwich_collider = TexturedModel(obj_loader.load_obj_model("sandwich_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    sandwich = Food(static_sandwich_model, static_sandwich_collider, "Tuna Sandwich")
    sandwich_spawn = FoodSpawn(sandwich, pos, rot, size, entities, collider_entities)


def mango_chutney_sandwich(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                           entities: list, collider_entities: list) -> None:
    sandwich_model = obj_loader.load_obj_model("sandwich", loader)
    sandwich_texture = ModelTexture(loader.load_texture(""))
    static_sandwich_model = TexturedModel(sandwich_model, sandwich_texture)
    static_sandwich_collider = TexturedModel(obj_loader.load_obj_model("sandwich_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    sandwich = Food(static_sandwich_model, static_sandwich_collider, "Mango Chutney Sandwich")
    sandwich_spawn = FoodSpawn(sandwich, pos, rot, size, entities, collider_entities)


def tomato_sandwich(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                    entities: list, collider_entities: list) -> None:
    sandwich_model = obj_loader.load_obj_model("sandwich", loader)
    sandwich_texture = ModelTexture(loader.load_texture(""))
    static_sandwich_model = TexturedModel(sandwich_model, sandwich_texture)
    static_sandwich_collider = TexturedModel(obj_loader.load_obj_model("sandwich_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    sandwich = Food(static_sandwich_model, static_sandwich_collider, "Tomato Sandwich")
    sandwich_spawn = FoodSpawn(sandwich, pos, rot, size, entities, collider_entities)


def sirserli(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
             entities: list, collider_entities: list) -> None:
    sirserli_model = obj_loader.load_obj_model("sirserli", loader)
    sirserli_texture = ModelTexture(loader.load_texture(""))
    static_sirserli_model = TexturedModel(sirserli_model, sirserli_texture)
    static_sirserli_collider = TexturedModel(obj_loader.load_obj_model("sirserli_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    sirserl = Food(static_sirserli_model, static_sirserli_collider, "Sirserli")
    sirserli_spawn = FoodSpawn(sirserl, pos, rot, size, entities, collider_entities)


def croissant(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
              entities: list, collider_entities: list) -> None:
    croissant_model = obj_loader.load_obj_model("croissant", loader)
    croissant_texture = ModelTexture(loader.load_texture(""))
    static_croissant_model = TexturedModel(croissant_model, croissant_texture)
    static_croissant_collider = TexturedModel(obj_loader.load_obj_model("croissant_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    croissan = Food(static_croissant_model, static_croissant_collider, "Croissant")
    croissant_spawn = FoodSpawn(croissan, pos, rot, size, entities, collider_entities)


def chocolate_croissant(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                        entities: list, collider_entities: list) -> None:
    croissant_model = obj_loader.load_obj_model("croissant", loader)
    croissant_texture = ModelTexture(loader.load_texture(""))
    static_croissant_model = TexturedModel(croissant_model, croissant_texture)
    static_croissant_collider = TexturedModel(obj_loader.load_obj_model("croissant_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    croissan = Food(static_croissant_model, static_croissant_collider, "Chocolate Croissant")
    croissant_spawn = FoodSpawn(croissan, pos, rot, size, entities, collider_entities)


def almond_croissant(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                     entities: list, collider_entities: list) -> None:
    croissant_model = obj_loader.load_obj_model("croissant", loader)
    croissant_texture = ModelTexture(loader.load_texture(""))
    static_croissant_model = TexturedModel(croissant_model, croissant_texture)
    static_croissant_collider = TexturedModel(obj_loader.load_obj_model("croissant_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    croissan = Food(static_croissant_model, static_croissant_collider, "Almond Croissant")
    croissant_spawn = FoodSpawn(croissan, pos, rot, size, entities, collider_entities)


def strawberry_tart(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                    entities: list, collider_entities: list) -> None:
    strawberry_tart_model = obj_loader.load_obj_model("erdbeertoertchen", loader)
    strawberry_tart_texture = ModelTexture(loader.load_texture(""))
    static_strawberry_tart_model = TexturedModel(strawberry_tart_model, strawberry_tart_texture)
    static_strawberry_tart_collider = TexturedModel(obj_loader.load_obj_model("erdbeertoertchen_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    tart = Food(static_strawberry_tart_model, static_strawberry_tart_collider, "Strawberry Tart")
    tart_spawn = FoodSpawn(tart, pos, rot, size, entities, collider_entities)


def cookie(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
           entities: list, collider_entities: list) -> None:
    cookie_model = obj_loader.load_obj_model("cookie", loader)
    cookie_texture = ModelTexture(loader.load_texture(""))
    static_cookie_model = TexturedModel(cookie_model, cookie_texture)
    static_cookie_collider = TexturedModel(obj_loader.load_obj_model("cookie_collider", loader),
                                           ModelTexture(loader.load_texture("")))

    cookie = Food(static_cookie_model, static_cookie_collider, "Cookie")
    cookie_spawn = FoodSpawn(cookie, pos, rot, size, entities, collider_entities)


def spitzbub(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
             entities: list, collider_entities: list) -> None:
    spitzbub_model = obj_loader.load_obj_model("spitzbub", loader)
    spitzbub_texture = ModelTexture(loader.load_texture(""))
    static_spitzbub_model = TexturedModel(spitzbub_model, spitzbub_texture)
    static_spitzbub_collider = TexturedModel(obj_loader.load_obj_model("spitzbub_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    spitzbub = Food(static_spitzbub_model, static_spitzbub_collider, "Spitzbub")
    spitzbub_spawn = FoodSpawn(spitzbub, pos, rot, size, entities, collider_entities)


def linzerli(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
             entities: list, collider_entities: list) -> None:
    linzerli_model = obj_loader.load_obj_model("linzerli", loader)
    linzerli_texture = ModelTexture(loader.load_texture(""))
    static_linzerli_model = TexturedModel(linzerli_model, linzerli_texture)
    static_linzerli_collider = TexturedModel(obj_loader.load_obj_model("linzerli_collider", loader),
                                             ModelTexture(loader.load_texture("")))

    linzerli = Food(static_linzerli_model, static_linzerli_collider, "Linzerli")
    linzerli_spawn = FoodSpawn(linzerli, pos, rot, size, entities, collider_entities)


def carac(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
          entities: list, collider_entities: list) -> None:
    model = obj_loader.load_obj_model("carac", loader)
    texture = ModelTexture(loader.load_texture(""))
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("carac_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    food = Food(static_model, static_collider, "Carac")
    food_spawn = FoodSpawn(food, pos, rot, size, entities, collider_entities)


def wurstwegge(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
               entities: list, collider_entities: list) -> None:
    model = obj_loader.load_obj_model("wurstwegge", loader)
    texture = ModelTexture(loader.load_texture(""))
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("wurstwegge_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    food = Food(static_model, static_collider, "Wurstwegge")
    food_spawn = FoodSpawn(food, pos, rot, size, entities, collider_entities)


def schinkengipfel(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                   entities: list, collider_entities: list) -> None:
    model = obj_loader.load_obj_model("schinkengipfel", loader)
    texture = ModelTexture(loader.load_texture(""))
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("schinkengipfel_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    food = Food(static_model, static_collider, "Schinkengipfel")
    food_spawn = FoodSpawn(food, pos, rot, size, entities, collider_entities)


def chocolate_cake(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                   entities: list, collider_entities: list) -> None:
    model = obj_loader.load_obj_model("cake", loader)
    texture = ModelTexture(loader.load_texture(""))
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("cake_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    food = Food(static_model, static_collider, "Chocolate Cake")
    food_spawn = FoodSpawn(food, pos, rot, size, entities, collider_entities)


def passionfruit_cake(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                   entities: list, collider_entities: list) -> None:
    model = obj_loader.load_obj_model("cake", loader)
    texture = ModelTexture(loader.load_texture(""))
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("cake_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    food = Food(static_model, static_collider, "Passionfruit Cake")
    food_spawn = FoodSpawn(food, pos, rot, size, entities, collider_entities)


def carrot_cake(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                   entities: list, collider_entities: list) -> None:
    model = obj_loader.load_obj_model("cake", loader)
    texture = ModelTexture(loader.load_texture(""))
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("cake_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    food = Food(static_model, static_collider, "Carrot Cake")
    food_spawn = FoodSpawn(food, pos, rot, size, entities, collider_entities)


def citron_cake(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                entities: list, collider_entities: list) -> None:
    model = obj_loader.load_obj_model("cake", loader)
    texture = ModelTexture(loader.load_texture(""))
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("cake_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    food = Food(static_model, static_collider, "Citron Cake")
    food_spawn = FoodSpawn(food, pos, rot, size, entities, collider_entities)


def ovomaltine(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    texture.set_shine_damper(10)
    texture.set_reflectivity(0.5)

    model = obj_loader.load_obj_model("ovomaltine", loader)
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("ovomaltine_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    ent = Entity(static_model, pos, *rot, size)
    collider = Entity(static_collider, pos, *rot, size)
    game_object = GameObject(ent, int_name="INGREDIENT", collider=collider)
    game_object.set_attachment(Ingredient("Ovomaltine"))
    game_object.set_prompt("Press 'E' or 'Q' to pick up.")
    game_object.set_info("Ovomaltine")

    return game_object


def caotina(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    texture.set_shine_damper(10)
    texture.set_reflectivity(0.5)

    model = obj_loader.load_obj_model("ovomaltine", loader)
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("ovomaltine_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    ent = Entity(static_model, pos, *rot, size)
    collider = Entity(static_collider, pos, *rot, size)
    game_object = GameObject(ent, int_name="INGREDIENT", collider=collider)
    game_object.set_attachment(Ingredient("Caotina"))
    game_object.set_prompt("Press 'E' or 'Q' to pick up.")
    game_object.set_info("Caotina")

    return game_object


def chocolatl(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    texture.set_shine_damper(10)
    texture.set_reflectivity(0.5)

    model = obj_loader.load_obj_model("ovomaltine", loader)
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("ovomaltine_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    ent = Entity(static_model, pos, *rot, size)
    collider = Entity(static_collider, pos, *rot, size)
    game_object = GameObject(ent, int_name="INGREDIENT", collider=collider)
    game_object.set_attachment(Ingredient("Chocolatl"))
    game_object.set_prompt("Press 'E' or 'Q' to pick up.")
    game_object.set_info("Chocolatl")

    return game_object


def finished_counter(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    counter_model = obj_loader.load_obj_model("serving_station", loader)
    counter_texture = ModelTexture(loader.load_texture(""))
    static_counter_model = TexturedModel(counter_model, counter_texture)
    static_counter_collider = TexturedModel(obj_loader.load_obj_model("serving_station_collider", loader),
                                            ModelTexture(loader.load_texture("")))

    counter = Entity(static_counter_model, pos, *rot, size)
    counter_collider = Entity(static_counter_collider, pos, *rot, size)
    counter_game_object = GameObject(counter, collider=counter_collider)
    counter_game_object.set_pickup_able(False)

    return counter_game_object


def finished_collider(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader) -> GameObject:
    static_finished_collider = TexturedModel(obj_loader.load_obj_model("serving_station_finished_collider", loader),
                                             ModelTexture(loader.load_texture("")))
    finished_col = Entity(static_finished_collider, pos, *rot, size)
    finished_game_object = GameObject(finished_col, int_name="FINISHED")
    return finished_game_object


def lemons(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
          entities: list, collider_entities: list) -> None:
    model = obj_loader.load_obj_model("lemon_vessel", loader)
    texture = ModelTexture(loader.load_texture(""))
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("lemon_vessel_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    food = Food(static_model, static_collider, "Lemon")

    alt_model = obj_loader.load_obj_model("lemon", loader)
    alt_texture = ModelTexture(loader.load_texture(""))
    alt_static_model = TexturedModel(alt_model, alt_texture)
    alt_static_collider = TexturedModel(obj_loader.load_obj_model("lemon_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    food.set_alt_model(alt_static_model)
    food.set_alt_collider(alt_static_collider)

    food_spawn = FoodSpawn(food, pos, rot, size, entities, collider_entities)


def ice_machine(pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                entities: list, collider_entities: list) -> GameObject:
    model = obj_loader.load_obj_model("ice_machine", loader)
    texture = ModelTexture(loader.load_texture("white"))
    static_model = TexturedModel(model, texture)
    static_collider = TexturedModel(obj_loader.load_obj_model("ice_machine_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    food = Food(static_model, static_collider, "Ice")

    alt_model = obj_loader.load_obj_model("ice_cubes", loader)
    alt_texture = ModelTexture(loader.load_texture(""))
    alt_static_model = TexturedModel(alt_model, alt_texture)
    alt_static_collider = TexturedModel(obj_loader.load_obj_model("ice_cubes_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    food.set_alt_model(alt_static_model)
    food.set_alt_collider(alt_static_collider)

    food_spawn = FoodSpawn(food, pos, rot, size, entities, collider_entities)

    door_texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    door_texture.set_shine_damper(10)
    door_texture.set_reflectivity(0.5)

    door_model = obj_loader.load_obj_model("ice_machine_door", loader)
    door_static_model = TexturedModel(door_model, door_texture)
    door_static_collider = TexturedModel(obj_loader.load_obj_model("ice_machine_door_collider", loader),
                                    ModelTexture(loader.load_texture("")))

    door_pos = [pos[0] + 4.5, pos[1] + 0.25, pos[2] + 3.5]

    ent = Entity(door_static_model, door_pos, *rot, size)
    collider = Entity(door_static_collider, door_pos, *rot, size)
    game_object = GameObject(ent, int_name="DOOR", collider=collider)
    game_object.set_prompt("Press 'E' or 'Q' to open/close.")

    return game_object



