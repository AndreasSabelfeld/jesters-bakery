

class CoffeePage:
    __instances = []

    def __init__(self, product=None):
        """
        Initializes a new CoffeePage instance. If a product is provided, it is added
        to the list of products for this page.

        :param product: The product to add to this page, if provided.
        """
        self.__products = []
        if product:
            self.__products.append(product)
        CoffeePage.__instances.append(self)

    @classmethod
    def add_product(cls, product) -> None:
        """
        Adds a product to the last instance of CoffeePage. If the last instance
        already has 16 products, a new instance is created.

        :param product: The product to be added.
        """
        if not cls.__instances:
            CoffeePage()
        if len(cls.__instances[-1].__products) < 16:
            cls.__instances[-1].__products.append(product)
        else:
            CoffeePage(product)

    @classmethod
    def get_instances(cls) -> list:
        """
        Returns a copy of the list of CoffeePage instances.

        :return: A copy of the list containing all instances of CoffeePage.
        """
        return cls.__instances.copy()

    def get_products(self) -> list:
        """
        Returns the list of products for this CoffeePage instance.

        :return: The list of products.
        """
        return self.__products


class CoffeePageLactoseFree:
    __instances = []

    def __init__(self, product=None):
        """
        Initializes a new CoffeePageLactoseFree instance. If a product is provided,
        it is added to the list of products for this page.

        :param product: The product to add to this page, if provided.
        """
        self.__products = []
        if product:
            self.__products.append(product)
        CoffeePageLactoseFree.__instances.append(self)

    @classmethod
    def add_product(cls, product) -> None:
        """
        Adds a product to the last instance of CoffeePageLactoseFree. If the last instance
        already has 16 products, a new instance is created.

        :param product: The product to be added.
        """
        if not cls.__instances:
            CoffeePageLactoseFree()
        if len(cls.__instances[-1].__products) < 16:
            cls.__instances[-1].__products.append(product)
        else:
            CoffeePageLactoseFree(product)

    @classmethod
    def get_instances(cls) -> list:
        """
        Returns a copy of the list of CoffeePageLactoseFree instances.

        :return: A copy of the list containing all instances of CoffeePageLactoseFree.
        """
        return cls.__instances.copy()

    def get_products(self) -> list:
        """
        Returns the list of products for this CoffeePageLactoseFree instance.

        :return: The list of products.
        """
        return self.__products
