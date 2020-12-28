import click
from collections import Counter

from actions import process_order, handle_order, deliver, pickup
from actions import OrderException
from menu import MENU, SIZES_AVAILABLE, DEFAULT_SIZE


INITIAL_AMOUNT = 100

STASH = Counter(
    {
        "dough": INITIAL_AMOUNT * 100,
        "mozzarella": INITIAL_AMOUNT * 100,
        "tomato sauce": INITIAL_AMOUNT * 100,
        "pepperoni": INITIAL_AMOUNT * 50,
        "pepper": INITIAL_AMOUNT * 50,
        "chicken": INITIAL_AMOUNT * 80,
        "pineapples": INITIAL_AMOUNT * 50,
        "bacon": INITIAL_AMOUNT * 10,
        "sweet onions": INITIAL_AMOUNT,
        "basil": INITIAL_AMOUNT,
        "oregano": INITIAL_AMOUNT,
    }
)


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--delivery",
    default=False,
    is_flag=True,
    help="specify if you want your order to be delivered",
)
@click.option(
    "-s",
    "--size",
    multiple=True,
    default=DEFAULT_SIZE,
    metavar="",
    help="""
    specify sizes in order of corresponding pizzas apperances
    default size is 'L', available: 'L', 'XL'
    when amount of pizzas more than sizes specified, the last size used for the rest
    sizes always shifted to the left, such as,
    e.g. 'pepperoni hawaiian -s L speciale -s XL'
    means pepperoni in 'L' and two others in 'XL'
    """,
)
@click.argument("pizza", nargs=-1, required=True)
def order(pizza: str, size: str, delivery: bool):
    """
    takes order of one or more pizza(s)
    if you want to take several pizzas of the same type
    provide order as 'pizza_type*amount' without spaces, e.g. 'pepperoni*3'
    """
    try:
        ordered = process_order(pizza, size)
    except OrderException as exception:
        print(exception)
        print("see order --help for more info")
        return
    ready_order = handle_order(ordered, STASH)
    if delivery:
        deliver(ready_order)
    else:
        pickup(ready_order)


@cli.command()
def menu():
    """
    lists all pizzas you could order
    available sizes are 'L' and 'XL' for all pizza types
    """
    print("\nMenu:\n")
    for pizza_name in MENU:
        pizza = MENU[pizza_name](size=DEFAULT_SIZE)
        print(f"{pizza.pretty} : {pizza.price}")
    print(f"\nall prices above are set for {DEFAULT_SIZE} size, double it for 'XL'")


if __name__ == "__main__":
    cli()
