from collections import Counter

SIZES_AVAILABLE = ["L", "XL"]
DEFAULT_SIZE = "L"


class Pizza:
    """
    implements base pizza class
    """

    def __init__(self, size=DEFAULT_SIZE):
        """
        initiate instance of pizza class
        """
        self.size = size
        self._basic_ingredients = Counter(
            {
                "dough": 100,
                "mozzarella": 60,
                "tomato sauce": 60,
            }
        )
        self.ingredients = self._scale_ingredients(self._basic_ingredients)
        self.baked = False
        self.price = self._scale_price(350)

    def _get_scaling_factor(self):
        """
        helps scale amount of ingredients needed and/or price due to size
        """
        if self.size == DEFAULT_SIZE:
            return 1
        else:
            return 2

    def _scale_ingredients(self, ingredients):
        """
        scales amount of ingredients needed due to size
        """
        factor = self._get_scaling_factor()
        return Counter({k: v * factor for k, v in ingredients.items()})

    def _scale_price(self, price):
        """
        scales price due to size
        """
        return price * self._get_scaling_factor()

    @property
    def pretty(self):
        """
        returns pretty pizza description with ingredients to display in a menu
        """
        return f"{type(self).__name__:<10}: {' - '.join(k.capitalize() for k in self.ingredients if k != 'dough')}"

    def __str__(self):
        """
        returns short pizza representation as class name and size
        """
        return self.__repr__()

    def __repr__(self):
        """
        returns short pizza representation as class name and size
        """
        return f"{type(self).__name__} {self.size}"

    def __iter__(self):
        """
        overloaded method to get dict representation of an instance as a recipe
        """
        for key, value in self.ingredients.items():
            yield key, value

    def __eq__(self, other):
        """
        allows to compare two different pizza instances
        """
        return type(other) == type(self) and dict(self) == dict(other)

    def __hash__(self):
        """
        implements hashing for simple usage in Counters or sets
        """
        return hash(
            "".join(f"{k}{v}" for k, v in self.ingredients.items()) + f"{self.price}"
        )


class Margherita(Pizza):
    """
    your simple yet delicious pizza
    """

    def __init__(self, size: str = DEFAULT_SIZE):
        """
        initiate instance
        """
        super().__init__(size)
        self.ingredients += self._scale_ingredients({"basil": 10, "oregano": 10})
        self.price = self._scale_price(200)


class Pepperoni(Pizza):
    """
    want something spicy?
    """

    def __init__(self, size: str = DEFAULT_SIZE):
        """
        initiate instance
        """
        super().__init__(size)
        self.ingredients += self._scale_ingredients({"pepperoni": 50, "pepper": 20})
        self.price = self._scale_price(250)


class Hawaiian(Pizza):
    """
    aloha, brother
    """

    def __init__(self, size: str = DEFAULT_SIZE):
        """
        initiate instance
        """
        super().__init__(size)
        self.ingredients += self._scale_ingredients({"chicken": 50, "pineapples": 40})
        self.price = self._scale_price(300)


class Speciale(Pizza):
    """
    irresistable for any gourmet
    """

    def __init__(self, size: str = DEFAULT_SIZE):
        """
        initiate instance
        """
        super().__init__(size)
        self.ingredients += self._scale_ingredients(
            {"chicken": 50, "bacon": 30, "sweet onions": 10}
        )
        self.price = self._scale_price(350)


MENU = {
    "margherita": Margherita,
    "pepperoni": Pepperoni,
    "hawaiian": Hawaiian,
    "speciale": Speciale,
}
