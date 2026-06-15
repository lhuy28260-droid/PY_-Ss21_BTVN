import unittest

from pos_logic import (
    calculate_total,
    add_item,
    DRINK_MENU,
    ItemNotFoundError,
    InvalidQuantityError
)


class TestHighlands(unittest.TestCase):

    def test_calculate_total(self):

        cart = [
            {
                "price": 35000,
                "quantity": 2
            },
            {
                "price": 45000,
                "quantity": 1
            }
        ]

        self.assertEqual(
            calculate_total(cart),
            115000
        )

    def test_invalid_code(self):

        cart = []

        with self.assertRaises(
            ItemNotFoundError
        ):
            add_item(
                DRINK_MENU,
                cart,
                "ABC",
                1
            )

    def test_invalid_quantity(self):

        cart = []

        with self.assertRaises(
            InvalidQuantityError
        ):
            add_item(
                DRINK_MENU,
                cart,
                "P1",
                -1
            )


if __name__ == "__main__":
    unittest.main()