import time
import random
from itertools import chain, repeat
from collections import defaultdict, Counter
from typing import Callable, Dict, List, Set, Tuple

from menu import Pizza, MENU, SIZES_AVAILABLE, DEFAULT_SIZE


class OrderException(Exception):
    pass


def log(message_template: str = "{} секунд", display_name: bool = False) -> Callable:
    """
    a decorator allowing to pass 'message_template'
    in which run-time from inner decorator will be substituted
    """

    def timing_wrapper(func: Callable) -> Callable:
        """
        a decorator allowing time which takes a function to run
        measures time in seconds and outputs passed time into stdout
        """

        def inner_wrapper(*args, **kwargs):
            start_time = time.monotonic()
            result = func(*args, **kwargs)
            end_time = time.monotonic()
            passed_time = end_time - start_time
            message_formatted = message_template.format(round(passed_time, 2))
            if display_name:
                print(f"{func.__name__} - {message_formatted}")
            else:
                print(message_formatted)
            return result

        return inner_wrapper

    return timing_wrapper


def validate_order(pizza_type, size=DEFAULT_SIZE, amount=1):
    """
    returns 'True' if order is correct and 'False' otherwise
    """
    try:
        amount = int(amount)
    except ValueError:
        return False
    if (
        (pizza_type.strip().lower() not in MENU)
        or (amount <= 0)
        or (size.upper() not in SIZES_AVAILABLE)
    ):
        return False
    else:
        return True


def process_order(pizza: Tuple[str], size: Tuple[str]):
    """
    takes order from arguments
    parses and validates it
    when something is incorrect raises an 'OrderException'
    """

    ordered = defaultdict(lambda: defaultdict(int))

    for p, s in zip(pizza, chain(size, repeat(size[-1]))):
        order_ok = True
        splitted = p.split("*")
        if len(splitted) == 2:
            pizza_type, amount = splitted
        elif len(splitted) == 1:
            pizza_type, amount = splitted[0], 1
        else:
            order_ok = False
        order_ok = order_ok and validate_order(pizza_type, s, amount)
        if not order_ok:
            raise OrderException(
                f'unknown order format - pizza type / size: "{p}" / "{s}", please order again'
            )
        else:
            ordered[pizza_type.lower()][s.upper()] += int(amount)
    return ordered


def take_from_stash(ingredients: Dict[str, int], stash: Dict[str, int]):
    """
    takes specified amount of ingredients from stash
    """
    for k, v in ingredients.items():
        stash[k] -= v


def check_stash(pizza_type: str, size: str, stash: Dict[str, int]):
    """
    checks if there's enough ingredients in the stash
    for a given pizza type and size
    if every ingredient is enough - takes them all from stash
    and returns the pizza instance
    otherwise does not take anything and returns None
    """
    pizza = MENU[pizza_type](size)
    ingredients = dict(pizza)

    enough = True
    for k, v in ingredients.items():
        if stash.get(k, 0) - v < 0:
            enough = False
            print(f"there is not enough ingredients for another {pizza}")
            break
    if enough:
        take_from_stash(ingredients, stash)
        return pizza
    else:
        return None


def handle_order(ordered: Dict[str, Dict[str, int]], stash: Dict[str, int]):
    """
    takes dict of pizza types with sizes and amounts
    and tries to get ingredients from stash for every pizza
    if there is enough - bakes it
    keeps pizzas in client's order - first tries the one which were met earlier
    returns Counter with baked pizzas of every type-size
    """

    baking_order = []

    for pizza_type in ordered:
        for size in ordered[pizza_type]:
            N = ordered[pizza_type][size]
            pizza_queue = (check_stash(pizza_type, size, stash) for _ in range(N))
            baking_order.extend(list(filter(lambda x: x, pizza_queue)))
    ready_order = Counter(bake(pizza) for pizza in baking_order)

    return ready_order


def summarize_order(ready_order: Dict[Pizza, int]):
    """
    print order that was really baked
    takes ready_order as Counter and displays it
    returns total price
    """
    price = 0
    if ready_order:
        print(f"\nYour pizza is waiting:\n")
        for pizza, amount in ready_order.items():
            print(f"{pizza}: {amount}, {pizza.price * amount}₽")
            price += pizza.price * amount
        print(f"\nTotal price: {price}₽")
    return price


@log(display_name=True)
def bake(pizza: Pizza):
    """
    bakes the pizza instance
    """
    time.sleep(0.1)
    pizza.baked = True
    return pizza


@log("Ожидание оплаты: {}с!")
def checkout(price: int):
    """
    simulates checkout, but without actually saving money
    as it intended to work only a single run
    """
    paid = False
    while not paid:
        input_ = input(f"Please, pay for your order: {price}₽\n")
        try:
            paid_sum = int(input_)
            if paid_sum > price:
                print("Thanks for the tips!")
                paid = True
            elif paid_sum < price:
                print(
                    f"Please, provide valid amount not less than total price: {price}₽"
                )
            else:
                paid = True
        except ValueError:
            print(
                f"Please, provide valid amount not less than total price: {price}₽"
            )
    time.sleep(0.5)
    print("Thanks for choosing us!")


@log("🛵 Доставили за {}с!")
def deliver(ready_order: Dict[Pizza, int]):
    """
    simulates delivery
    """
    time.sleep(random.randint(0, 3))
    price = summarize_order(ready_order)
    checkout(price)


@log("🏠 Забрали за {}с!")
def pickup(ready_order: Dict[Pizza, int]):
    """
    simulates pickup
    """
    time.sleep(random.randint(1, 4))
    price = summarize_order(ready_order)
    checkout(price)
