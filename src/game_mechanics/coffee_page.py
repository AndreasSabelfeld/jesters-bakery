

class CoffeePage:
    __instances = []

    def __init__(self, product=None):
        self.__products = []
        if product:
            self.__products.append(product)
        CoffeePage.__instances.append(self)

    @classmethod
    def add_product(cls, product):
        if not cls.__instances:
            CoffeePage()
        if len(cls.__instances[-1].__products) < 16:
            cls.__instances[-1].__products.append(product)
        else:
            CoffeePage(product)

    @classmethod
    def get_instances(cls) -> list:
        return cls.__instances.copy()

    def get_products(self) -> list:
        return self.__products


class CoffeePageLactoseFree:
    __instances = []

    def __init__(self, product=None):
        self.__products = []
        if product:
            self.__products.append(product)
        CoffeePageLactoseFree.__instances.append(self)

    @classmethod
    def add_product(cls, product):
        if not cls.__instances:
            CoffeePageLactoseFree()
        if len(cls.__instances[-1].__products) < 16:
            cls.__instances[-1].__products.append(product)
        else:
            CoffeePageLactoseFree(product)

    @classmethod
    def get_instances(cls) -> list:
        return cls.__instances.copy()

    def get_products(self) -> list:
        return self.__products
