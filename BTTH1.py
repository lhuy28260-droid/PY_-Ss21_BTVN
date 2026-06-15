import logging


# CẤU HÌNH HỆ THỐNG GHI NHẬT KÝ (LOGGING)

logging.basicConfig(
    filename='momo_transactions.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# TỰ ĐỊNH NGHĨA CÁC LỚP NGOẠI LỆ (CUSTOM EXCEPTIONS)
class InvalidAmountError(Exception):
    """Ngoại lệ ném ra khi số tiền giao dịch <= 0"""
    pass

class InsufficientBalanceError(Exception):
    """Ngoại lệ ném ra khi số dư ví không đủ để chuyển tiền"""
    pass


# THIẾT LẬP CẤU TRÚC DỮ LIỆU VÍ
my_wallet = {
    "balance": 0.0
}

def deposit_money(wallet):
    """Chức năng 1: Nạp tiền vào ví (Sử dụng Custom Exception)"""
    while True:
        try:
            raw_amount = input("Nhập số tiền cần nạp: ").strip()
            amount = float(raw_amount)
            
            if amount <= 0:
                raise InvalidAmountError(amount)    
            break    

        except ValueError:
            print("Vui lòng nhập số tiền hợp lệ.")
            logging.error("ValueError: Invalid numeric input for deposit.")
        except InvalidAmountError as e:
            err_amount = e.args[0]
            print("Số tiền nạp phải lớn hơn 0. Vui lòng nhập lại.")
            logging.error(f"InvalidAmountError: Attempted to process {int(err_amount)} VND.")
            
    wallet["balance"] += amount
    current_balance = wallet["balance"]
    
    print(f"Nạp tiền thành công: +{amount:,.0f} VND")
    print(f"Số dư hiện tại: {current_balance:,.0f} VND")
    
    logging.info(f"Deposit successful: +{int(amount)} VND. Current Balance: {int(current_balance)}")


def transfer_money(wallet):
    """Chức năng 2: Chuyển tiền (Sử dụng Custom Exception)"""
    
    while True:
        phone = input("Nhập số điện thoại người nhận: ").strip()
        if len(phone) == 10 and phone.isdigit():
            break
        else:
            print("Lỗi: Số điện thoại không hợp lệ (phải gồm đúng 10 chữ số). Vui lòng nhập lại.")
            logging.warning("Failed transfer attempt - Invalid phone format")
            
    try:
        raw_amount = input("Nhập số tiền cần chuyển: ").strip()
        amount = float(raw_amount)
        
        if amount <= 0:
            raise InvalidAmountError(amount)
            
        if amount > wallet["balance"]:
            raise InsufficientBalanceError(amount, wallet["balance"])
            
    except ValueError:
        print("Lỗi: Vui lòng nhập số tiền hợp lệ.")
        logging.error("ValueError: Invalid numeric input for transfer.")
        return
    except InvalidAmountError as e:
        err_amount = e.args[0]
        print("Lỗi: Số tiền giao dịch phải lớn hơn 0.")
        logging.error(f"InvalidAmountError: Attempted to process {int(err_amount)} VND.")
        return
    except InsufficientBalanceError as e:
        err_amount, current_bal = e.args
        print("Giao dịch thất bại: Số dư của bạn không đủ.")
        print(f"Số dư hiện tại: {int(current_bal):,} VND")
        logging.error(f"InsufficientBalanceError: Attempted to transfer {int(err_amount)} VND with balance {int(current_bal)} VND.")
        return
        
    if amount >= 10000000:
        logging.warning(f"High value transaction detected: {int(amount)} VND to {phone}")
        
    # Thực hiện trừ tiền
    wallet["balance"] -= amount
    current_balance = wallet["balance"]
    
    print(f"Chuyển tiền thành công tới số điện thoại {phone}.")
    print(f"Số tiền đã chuyển: {amount:,.0f} VND")
    print(f"Số dư còn lại: {current_balance:,.0f} VND")
    
    logging.info(f"Transfer successful: -{int(amount)} VND to {phone}. Current Balance: {int(current_balance)}")


def check_balance(wallet):
    """Chức năng 3: Xem số dư hiện tại"""
    print("\n--- SỐ DƯ VÍ MOMO ---")
    current_balance = wallet["balance"]
    
    print(f"Số dư hiện tại: {current_balance:,.0f} VND")
    logging.info(f"Balance checked. Current Balance: {int(current_balance)}")


def main():
    logging.info("Hệ thống Ví MoMo Giả Lập đã khởi động.")
    
    while True:
        print("========== VÍ MOMO GIẢ LẬP ==========")
        print("1. Nạp tiền vào ví")
        print("2. Chuyển tiền")
        print("3. Xem số dư hiện tại")
        print("4. Thoát chương trình")
        print("=======================================")
        
        choice = input("Chọn chức năng (1-4): ").strip()
        
        if choice == '1':
            deposit_money(my_wallet)
        elif choice == '2':
            transfer_money(my_wallet)
        elif choice == '3':
            check_balance(my_wallet) 
        elif choice == '4':
            print("Cảm ơn bạn đã sử dụng dịch vụ")
            logging.info("System shutdown")
            break  
        else:
            logging.warning("Invalid menu choice selected.")
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại số từ 1-4!")

if __name__ == "__main__":
    main()