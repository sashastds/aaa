"""
tests modules functionality in pizza package
"""

from functools import reduce
from itertools import chain
from operator import add
from collections import Counter, defaultdict
import io
import pytest

from menu import MENU, SIZES_AVAILABLE, Pizza, Margherita, Pepperoni, Hawaiian, Speciale

from actions import validate_order, process_order, handle_order, summarize_order
from actions import check_stash, take_from_stash
from actions import bake, deliver, pickup, checkout
from actions import OrderException


def test_all_hashes_differ():
    types = [
        pizza_type(size) for pizza_type in MENU.values() for size in SIZES_AVAILABLE
    ]
    assert len(set(types)) == len(types)


@pytest.mark.parametrize(
    "pizza_type, size, amount, etalon_answer",
    [
        pytest.param("margherita", "L", "1", True, id="all ok"),
        pytest.param("margherita", "XXX", "1", False, id="bad size"),
        pytest.param("sasha", "L", "1", False, id="bad name"),
        pytest.param("MargheritA", "L", "1", True, id="not a bad name"),
        pytest.param("margherita", "L", "0", False, id="bad amount"),
        pytest.param("margherita", "L", "-1", False, id="bad amount"),
        pytest.param("margherita", "L", "8.3", False, id="bad amount"),
    ],
)
def test_validate_order(pizza_type, size, amount, etalon_answer):
    assert validate_order(pizza_type, size, amount) == etalon_answer


@pytest.mark.parametrize(
    "pizza, size",
    [
        pytest.param(("margherita",), ("XXXXL"), id="bad size"),
        pytest.param(("notexistingpizza",), ("XL"), id="bad type"),
        pytest.param(("margherita*3",), ("XXXXL"), id="bad size, ok amount spec"),
        pytest.param(("margherita*3*3",), ("XL"), id="bad amount spec"),
    ],
)
def test_process_order_can_raise_orderexception(pizza, size):
    with pytest.raises(OrderException):
        process_order(pizza, size)


@pytest.mark.parametrize(
    "pizza, size, expected",
    [
        pytest.param(
            ("margherita*3", "margherita"), ("XL",), {"margherita": {"XL": 4}}
        ),
        pytest.param(
            ("margherita", "margherita"), ("XL", "L"), {"margherita": {"XL": 1, "L": 1}}
        ),
        pytest.param(
            ("margherita", "pepperoni", "margherita"),
            ("XL", "L"),
            {"margherita": {"XL": 1, "L": 1}, "pepperoni": {"L": 1}},
        ),
        pytest.param(
            ("pepperoni*2", "margherita", "pepperoni*3"),
            ("XL",),
            {"pepperoni": {"XL": 5}, "margherita": {"XL": 1}},
        ),
    ],
)
def test_process_order_works_correctly(pizza, size, expected):
    actual = process_order(pizza, size)
    assert dict(expected) == dict(actual)


@pytest.mark.parametrize(
    "size, etalon_answer",
    [
        pytest.param("L", "Pizza L", id="L"),
        pytest.param("XL", "Pizza XL", id="XL"),
    ],
)
def test_simple_print(size, etalon_answer):
    assert f"{Pizza(size)}" == etalon_answer


@pytest.mark.parametrize(
    "pizza_type, size, etalon_answer",
    [
        pytest.param(
            Margherita,
            "L",
            "Margherita: Mozzarella - Tomato sauce - Basil - Oregano",
            id="Margherita",
        ),
        pytest.param(
            Pepperoni,
            "XL",
            "Pepperoni : Mozzarella - Tomato sauce - Pepperoni - Pepper",
            id="Pepperoni",
        ),
    ],
)
def test_pretty_print(pizza_type, size, etalon_answer):
    assert pizza_type(size).pretty == etalon_answer


@pytest.mark.parametrize(
    "pizza_type",
    [
        pytest.param(Speciale, id="Speciale"),
        pytest.param(Hawaiian, id="Hawaiian"),
        pytest.param(Margherita, id="Margherita"),
        pytest.param(Pepperoni, id="Pepperoni"),
    ],
)
def test_pizza_equality(pizza_type):
    assert pizza_type("XL") == pizza_type("XL")


@pytest.mark.parametrize(
    "pizza_type",
    [
        pytest.param(Speciale, id="Speciale"),
        pytest.param(Hawaiian, id="Hawaiian"),
        pytest.param(Margherita, id="Margherita"),
        pytest.param(Pepperoni, id="Pepperoni"),
    ],
)
def test_pizza_inequality_sizes(pizza_type):
    assert pizza_type("L") != pizza_type("XL")


@pytest.mark.parametrize(
    "size",
    [
        pytest.param("L", id="L"),
        pytest.param("XL", id="XL"),
    ],
)
def test_pizza_inequality(size):
    assert Margherita(size) != Pepperoni(size)


def test_can_create_dict_from_pizza_instance():
    expected = {
        "dough": 100,
        "mozzarella": 60,
        "tomato sauce": 60,
    }
    assert dict(Pizza("L")) == expected


def test_price_doubles():
    assert Pizza("XL").price == Pizza("L").price * 2


def test_can_bake_pizza():
    assert bake(Pizza()).baked


@pytest.mark.parametrize(
    "amount_paid, message",
    [
        pytest.param("1000", "Thanks for choosing us!", id="exact"),
        pytest.param("1001", "Thanks for the tips!", id="tips"),
        pytest.param(
            "999\n1000",
            "Please, provide valid amount not less than total price",
            id="not enough",
        ),
        pytest.param(
            "nope\n1000",
            "Please, provide valid amount not less than total price",
            id="wrong",
        ),
    ],
)
def test_checkout(monkeypatch, capsys, amount_paid, message):
    monkeypatch.setattr("sys.stdin", io.StringIO(amount_paid))
    checkout(1000)
    out, _ = capsys.readouterr()
    assert message in out


def test_can_deliver_with_logs(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("0"))
    deliver(None)
    out, _ = capsys.readouterr()
    assert "Доставили" in out


def test_can_pickup_with_logs(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("0"))
    pickup(None)
    out, _ = capsys.readouterr()
    assert "Забрали" in out


@pytest.mark.parametrize(
    "ingredients, result",
    [
        pytest.param({"a": 10, "b": 5, "c": 1}, {"a": 0, "b": 0, "c": 0}, id="all"),
        pytest.param({"a": 5, "b": 0, "c": 1}, {"a": 5, "b": 5, "c": 0}, id="partly"),
        pytest.param({}, {"a": 10, "b": 5, "c": 1}, id="none"),
    ],
)
def test_can_take_from_stash(ingredients, result):
    stash = {"a": 10, "b": 5, "c": 1}
    take_from_stash(ingredients, stash)
    assert stash == result


@pytest.mark.parametrize(
    "pizza_type, size, expected",
    [
        pytest.param("margherita", "L", Margherita("L"), id="enough"),
        pytest.param("margherita", "XL", None, id="not enough"),
        pytest.param("speciale", "L", None, id="other ingredients"),
    ],
)
def test_can_check_stash_correctly(pizza_type, size, expected):
    margherita_l_size_stash = {
        "dough": 100,
        "mozzarella": 60,
        "tomato sauce": 60,
        "basil": 10,
        "oregano": 10,
    }
    result = check_stash(pizza_type, size, margherita_l_size_stash)
    assert expected == result


@pytest.fixture
def stash_m3_p2():
    margherita_l_size_stash = Counter(
        {"dough": 100, "mozzarella": 60, "tomato sauce": 60, "basil": 10, "oregano": 10}
    )
    pepperoni_l_size_stash = Counter(
        {
            "dough": 100,
            "mozzarella": 60,
            "tomato sauce": 60,
            "pepperoni": 50,
            "pepper": 20,
        }
    )
    n_margherita = 3
    n_pepperoni = 2
    stash = reduce(
        add,
        chain(
            (margherita_l_size_stash for _ in range(n_margherita)),
            (pepperoni_l_size_stash for _ in range(n_pepperoni)),
        ),
    )
    return stash


@pytest.fixture
def order_m3_p3_s1():
    n_margherita = 3
    n_pepperoni = 2
    order = {
        "margherita": {"L": n_margherita},
        "pepperoni": {"L": n_pepperoni + 1},
        "speciale": {"L": 1},
    }
    return order


def test_can_handle_order_correctly(stash_m3_p2, order_m3_p3_s1, capsys):
    n_margherita = 3
    n_pepperoni = 2
    result = handle_order(order_m3_p3_s1, stash_m3_p2)
    out, _ = capsys.readouterr()

    assert (
        result[Margherita("L")] == n_margherita
        and result[Pepperoni("L")] == n_pepperoni
        and result[Speciale("L")] == 0
        and "there is not enough ingredients for another Pepperoni L" in out
        and "there is not enough ingredients for another Speciale L" in out
    )


class DefaultDictWithGet(defaultdict):
    """
    allows to experience actually expected behavior
    when 'safe' method for usual dict .get(key, value) applied to defaultdict
    will return not 'value' but the value with which defaultdict was instantiated
    in defaultdict's implementation this is not the case
    """

    def get(self, key, default):
        """
        ignores default value and uses intrinsic magic by __getitem__
        """
        return self[key]


@pytest.fixture
def stash_unlimited():
    stash = DefaultDictWithGet(lambda: 10000000)
    return stash


def test_can_summarize_order_correctly(order_m3_p3_s1, stash_unlimited):
    pizza_types = {Margherita: 3, Pepperoni: 3, Speciale: 1}
    order = handle_order(order_m3_p3_s1, stash_unlimited)
    price = summarize_order(order)
    expected_price = reduce(
        add, (pizza().price for pizza in pizza_types for _ in range(pizza_types[pizza]))
    )
    assert expected_price == price
