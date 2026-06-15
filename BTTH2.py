import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('highlands_pos.log', encoding='utf-8', mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)

class ItemNotFoundError(Exception):
    pass

class InvalidQuantityError(Exception):
    pass

DRINK_MENU = {
    "P1": {"name": "Phin Sữa Đá", "price": 35000},
    "F1": {"name": "Freeze Trà Xanh", "price": 55000},
    "T1": {"name": "Trà Sen Vàng", "price": 45000}
}

current_order = []

def display_menu(menu):
    print(" --- THỰC ĐƠN HIGHLANDS COFFEE --- ")
    for code, details in menu.items():
        print(f"[{code}] - {details.get('name', 'Unknown')} - {details.get('price', 0):,} VNĐ")
    
def add_to_cart(menu, cart):
    print(" --- THÊM MÓN VÀO GIỎ --- ")
    try:
        drink_code = input("Nhập mã đồ uống: ").strip().upper()
        if drink_code not in menu:
            raise ItemNotFoundError(drink_code) 
            
        raw_qty = input("Nhập số lượng: ").strip()
        quantity = int(raw_qty) 
        
        if quantity <= 0:
            raise InvalidQuantityError(quantity) 
            
        item_name = menu[drink_code]["name"]
        item_price = menu[drink_code]["price"]
        
        cart.append({
            "code": drink_code,
            "name": item_name,
            "price": item_price,
            "quantity": quantity
        })
        
        logging.info(f"Added {quantity} of {drink_code} to order")
        print(f"Đã thêm {quantity} x {item_name} vào giỏ hàng.")
        
    except ItemNotFoundError as e:
        print("Mã đồ uống không hợp lệ, vui lòng kiểm tra lại thực đơn!")
        logging.warning(f"ItemNotFoundError - Code: {e.args[0]}")
    except ValueError:
        print("Vui lòng nhập số lượng là một số nguyên!")
        logging.error("ValueError - Invalid quantity input")
    except InvalidQuantityError as e:
        print("Số lượng phải lớn hơn 0!")
        logging.warning(f"InvalidQuantityError - Quantity: {e.args[0]}")


def calculate_total(cart):
    """Hàm lõi (Core Logic) tách biệt hoàn toàn để phục vụ Unit Test"""
    return sum(item["price"] * item["quantity"] for item in cart)


def view_cart_and_total(cart):
    if not cart:
        print("Giỏ hàng trống, vui lòng chọn món (Chức năng 2).")
        return
        
    print(" --- GIỎ HÀNG HIỆN TẠI --- ")
    print(f"{'Mã SP':<6} | {'Tên đồ uống':<20} | {'Đơn giá':<10} | {'Số lượng':<9} | Thành tiền")
    print("-" * 70)
    
    for item in cart:
        item_total = item["price"] * item["quantity"]
        print(f"{item['code']:<6} | {item['name']:<20} | {item['price']:<10,} | {item['quantity']:<9} | {item_total:,} VNĐ")
        
    print("-" * 70)
    
    # Tái sử dụng hàm lõi
    total_amount = calculate_total(cart)
    print(f"Tổng tiền cần thanh toán: {total_amount:,} VNĐ")


def checkout(cart):
    print("\n--- THANH TOÁN ---")
    if not cart:
        print("Giỏ hàng trống, vui lòng chọn món (Chức năng 2).")
        return
        
    total_amount = calculate_total(cart)
    print(f"Tổng tiền cần thanh toán: {total_amount:,} VNĐ")
    
    confirm = input(f"Xác nhận thanh toán {total_amount:,} VNĐ? (y/n): ").strip().lower()
    
    if confirm == 'y':
        print("Thanh toán thành công.")
        logging.info("Checkout successful")
        cart.clear()
        print("Giỏ hàng đã được làm trống.")
    elif confirm == 'n':
        print("Đã hủy thao tác thanh toán. Quay lại menu chính.")
    else:
        print("Lựa chọn không hợp lệ. Thanh toán đã bị hủy.")


def main():
    while True:
        print("\n========== HIGHLANDS MINI POS ==========")
        print("1. Xem thực đơn")
        print("2. Thêm món vào giỏ")
        print("3. Xem giỏ hàng & Tính tổng tiền")
        print("4. Thanh toán & Xóa giỏ hàng")
        print("5. Thoát ca làm việc")
        print("========================================")
        
        choice = input("Chọn chức năng (1-5): ").strip()
        
        if choice == '1':
            display_menu(DRINK_MENU)
        elif choice == '2':
            add_to_cart(DRINK_MENU, current_order)
        elif choice == '3':
            view_cart_and_total(current_order)
        elif choice == '4':
            checkout(current_order)
        elif choice == '5':
            # Chức năng 5: Ghi log thoát ca chuẩn xác
            logging.info("Cashier logged out. System shutdown.")
            print("Đã thoát ca làm việc. Hẹn gặp lại!")
            break  
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại số từ 1-5!")

if __name__ == "__main__":
    main()