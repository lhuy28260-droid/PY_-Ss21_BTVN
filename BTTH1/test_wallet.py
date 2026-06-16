import unittest

from wallet import (
    Wallet,
    InvalidAmountError,
    InsufficientBalanceError
)


class TestWallet(unittest.TestCase):

    def test_deposit_success(self):

        wallet = Wallet()

        wallet.deposit(50000)

        self.assertEqual(
            wallet.balance,
            50000
        )

    def test_transfer_insufficient_balance(self):

        wallet = Wallet()

        wallet.deposit(100000)

        with self.assertRaises(
            InsufficientBalanceError
        ):
            wallet.transfer(200000)

    def test_invalid_amount(self):

        wallet = Wallet()

        with self.assertRaises(
            InvalidAmountError
        ):
            wallet.deposit(-50000)


if __name__ == "__main__":
    unittest.main()