import json
import keyword


class DefaultAttributer:
    def __getattribute__(self, attr):

        try:

            value = super().__getattribute__(attr)
        except AttributeError:

            value = None
        return value

    def __setattr__(self, attr, value):

        __dict__ = super().__getattribute__("__dict__")
        __dict__[attr] = value


class DefaultStructure(DefaultAttributer):
    def __init__(self, items_dict=None):

        if items_dict:

            for k, v in items_dict.items():

                self.__setattr__(k, v)


class JSONParser(DefaultAttributer):
    def __init__(self, record):

        if isinstance(record, str):

            record_dict = json.loads(record)
        elif isinstance(record, dict):

            record_dict = record
        else:

            raise ValueError(
                "JSONParser constructor takes only valid json-structured object, either as 'str' or 'dict'"
            )
        for k, v in record_dict.items():

            if k == "location":

                self.__setattr__(k, self._parse_location(v))
            else:

                self.__setattr__(k, v)
        if self.title is None:

            raise AttributeError("title was not provided in json")

    def _parse_address(self, address):

        """
        assuming all input strings have similar notation: "city-like, street-like, building-№-like"
        """

        city, street, building = address.split(", ")
        return DefaultStructure({"city": city, "street": street, "building": building})

    def _parse_location(self, location):

        return DefaultStructure(
            {
                k: (v if k != "address" else self._parse_address(v))
                for k, v in location.items()
            }
        )


class BaseAdvert(JSONParser):
    def __init__(self, record):

        super().__init__(record)
        self._validate_price(self.price)

    def __getattribute__(self, attr):

        value = super().__getattribute__(attr)

        if attr == "price" and value is None:

            value = 0
        return value

    def __setattr__(self, attr, value):

        if attr == "price":

            self._validate_price(value)
        elif keyword.iskeyword(attr):

            attr = f"{attr}_"
        __dict__ = super().__getattribute__("__dict__")
        __dict__[attr] = value

    def __repr__(self):

        return f"{self.title} | {self.price} ₽"

    def _validate_price(self, price):

        if price < 0:

            raise ValueError(f"price must be >= 0, current price is {price}")


class ColorizeMixin:
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._repr_color_code = 33  # yellow

    def __repr__(self):

        return f"\033[1;{self._repr_color_code};49m{super().__repr__()}"


class Advert(ColorizeMixin, BaseAdvert):
    def __init__(self, record):

        super().__init__(record)
