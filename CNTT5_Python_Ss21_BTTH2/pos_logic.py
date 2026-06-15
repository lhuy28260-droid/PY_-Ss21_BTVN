class ItemNotFoundError(Exception):
    pass


class InvalidQuantityError(Exception):
    pass


DRINK_MENU = {
    "P1": {"name": "Phin Sữa Đá", "price": 35000},
    "F1": {"name": "Freeze Trà Xanh", "price": 55000},
    "T1": {"name": "Trà Sen Vàng", "price": 45000}
}


def add_item(menu, cart, drink_code, quantity):

    if drink_code not in menu:
        raise ItemNotFoundError(drink_code)

    if quantity <= 0:
        raise InvalidQuantityError(quantity)

    cart.append({
        "code": drink_code,
        "name": menu[drink_code]["name"],
        "price": menu[drink_code]["price"],
        "quantity": quantity
    })


def calculate_total(cart):
    return sum(
        item["price"] * item["quantity"]
        for item in cart
    )