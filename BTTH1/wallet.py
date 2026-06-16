import logging

logging.basicConfig(
    filename='momo_transactions.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)


class InvalidAmountError(Exception):
    """Ngoại lệ ném ra khi số tiền giao dịch <= 0"""
    pass


class InsufficientBalanceError(Exception):
    """Ngoại lệ ném ra khi số dư ví không đủ để chuyển tiền"""
    pass


class Wallet:

    def __init__(self):
        self.balance = 0.0

    def deposit(self, amount):

        if amount <= 0:
            raise InvalidAmountError(amount)

        self.balance += amount

        return self.balance

    def transfer(self, amount):

        if amount <= 0:
            raise InvalidAmountError(amount)

        if amount > self.balance:
            raise InsufficientBalanceError(
                amount,
                self.balance
            )

        self.balance -= amount

        return self.balance


my_wallet = Wallet()


def deposit_money(wallet):

    while True:

        try:

            raw_amount = input(
                "Nhập số tiền cần nạp: "
            ).strip()

            amount = float(raw_amount)

            current_balance = wallet.deposit(
                amount
            )

            print(
                f"Nạp tiền thành công: "
                f"+{amount:,.0f} VND"
            )

            print(
                f"Số dư hiện tại: "
                f"{current_balance:,.0f} VND"
            )

            logging.info(
                f"Deposit successful: "
                f"+{int(amount)} VND. "
                f"Current Balance: "
                f"{int(current_balance)}"
            )

            break

        except ValueError:

            print(
                "Vui lòng nhập số tiền hợp lệ."
            )

            logging.error(
                "ValueError: Invalid numeric input for deposit."
            )

        except InvalidAmountError as e:

            err_amount = e.args[0]

            print(
                "Số tiền nạp phải lớn hơn 0."
            )

            logging.error(
                f"InvalidAmountError: "
                f"Attempted to process "
                f"{int(err_amount)} VND."
            )


def transfer_money(wallet):

    while True:

        phone = input(
            "Nhập số điện thoại người nhận: "
        ).strip()

        if len(phone) == 10 and phone.isdigit():
            break

        print(
            "Lỗi: Số điện thoại không hợp lệ "
            "(phải gồm đúng 10 chữ số)."
        )

        logging.warning(
            "Failed transfer attempt - Invalid phone format"
        )

    try:

        raw_amount = input(
            "Nhập số tiền cần chuyển: "
        ).strip()

        amount = float(raw_amount)

        current_balance = wallet.transfer(
            amount
        )

    except ValueError:

        print(
            "Lỗi: Vui lòng nhập số tiền hợp lệ."
        )

        logging.error(
            "ValueError: Invalid numeric input for transfer."
        )

        return

    except InvalidAmountError as e:

        err_amount = e.args[0]

        print(
            "Lỗi: Số tiền giao dịch phải lớn hơn 0."
        )

        logging.error(
            f"InvalidAmountError: "
            f"Attempted to process "
            f"{int(err_amount)} VND."
        )

        return

    except InsufficientBalanceError as e:

        err_amount, current_bal = e.args

        print(
            "Giao dịch thất bại: "
            "Số dư của bạn không đủ."
        )

        print(
            f"Số dư hiện tại: "
            f"{current_bal:,.0f} VND"
        )

        logging.error(
            f"InsufficientBalanceError: "
            f"Attempted to transfer "
            f"{int(err_amount)} VND "
            f"with balance "
            f"{int(current_bal)} VND."
        )

        return

    if amount >= 10000000:

        logging.warning(
            f"High value transaction detected: "
            f"{int(amount)} VND to {phone}"
        )

    print(
        f"Chuyển tiền thành công tới "
        f"số điện thoại {phone}."
    )

    print(
        f"Số tiền đã chuyển: "
        f"{amount:,.0f} VND"
    )

    print(
        f"Số dư còn lại: "
        f"{current_balance:,.0f} VND"
    )

    logging.info(
        f"Transfer successful: "
        f"-{int(amount)} VND "
        f"to {phone}. "
        f"Current Balance: "
        f"{int(current_balance)}"
    )


def check_balance(wallet):

    print("\n--- SỐ DƯ VÍ MOMO ---")

    print(
        f"Số dư hiện tại: "
        f"{wallet.balance:,.0f} VND"
    )

    logging.info(
        f"Balance checked. "
        f"Current Balance: "
        f"{int(wallet.balance)}"
    )


def main():

    logging.info(
        "Hệ thống Ví MoMo Giả Lập đã khởi động."
    )

    while True:

        print("========== VÍ MOMO GIẢ LẬP ==========")
        print("1. Nạp tiền vào ví")
        print("2. Chuyển tiền")
        print("3. Xem số dư hiện tại")
        print("4. Thoát chương trình")
        print("=======================================")

        choice = input(
            "Chọn chức năng (1-4): "
        ).strip()

        if choice == "1":

            deposit_money(my_wallet)

        elif choice == "2":

            transfer_money(my_wallet)

        elif choice == "3":

            check_balance(my_wallet)

        elif choice == "4":

            print(
                "Cảm ơn bạn đã sử dụng dịch vụ"
            )

            logging.info(
                "System shutdown"
            )

            break

        else:

            logging.warning(
                "Invalid menu choice selected."
            )

            print(
                "Lựa chọn không hợp lệ. "
                "Vui lòng nhập lại số từ 1-4!"
            )


if __name__ == "__main__":
    main()