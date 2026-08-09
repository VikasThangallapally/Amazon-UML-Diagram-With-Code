"""Interactive CLI for the Amazon UML models.

Run `python cli.py` to start interactive mode.
Run `python cli.py --demo` to run a scripted demo.
"""
import sys
from Amazon import Admin, Customer, Product, Payment, Shipping


def print_products():
    prods = Product.list_products()
    if not prods:
        print("No products available")
        return
    for p in prods:
        print(f"{p.product_id}: {p.product_name} - {p.product_description} (${p.product_price})")


def interactive():
    # simple in-memory users
    admins = [Admin(username="admin", password="secret", admin_name="SiteAdmin")]
    customers = []
    current_customer = None

    while True:
        print("\nMenu:\n1) Admin login\n2) Customer register/login\n3) List products\n4) Add product (admin)\n5) Add to cart (customer)\n6) View cart\n7) Place order\n8) Pay for order\n9) Ship order (admin)\n0) Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        if choice == "1":
            user = input("Admin username: ")
            pwd = input("Password: ")
            admin = next((a for a in admins if a.username == user), None)
            if admin and admin.login(pwd):
                print("Admin logged in")
                # allow add/remove operations immediately
            else:
                print("Invalid admin")
        elif choice == "2":
            sub = input("(r)egister or (l)ogin? ").strip().lower()
            if sub == "r":
                uname = input("username: ")
                pwd = input("password: ")
                name = input("name: ")
                email = input("email: ")
                cust = Customer(username=uname, password=pwd, customer_name=name, email=email)
                customers.append(cust)
                current_customer = cust
                print("Registered and logged in as", name)
            else:
                uname = input("username: ")
                pwd = input("password: ")
                cust = next((c for c in customers if c.username == uname), None)
                if cust and cust.login(pwd):
                    current_customer = cust
                    print("Logged in as", cust.customer_name)
                else:
                    print("Invalid credentials or user not found")
        elif choice == "3":
            print_products()
        elif choice == "4":
            user = input("Admin username: ")
            pwd = input("Password: ")
            admin = Admin(username=user, password=pwd, admin_name=user)
            if admin.login(pwd):
                name = input("Product name: ")
                desc = input("Description: ")
                price = float(input("Price: "))
                p = admin.add_product(name, desc, price)
                print("Added product", p.product_id)
            else:
                print("Admin authentication failed")
        elif choice == "5":
            if current_customer is None:
                print("Login as customer first")
                continue
            print_products()
            pid = int(input("Product id to add: "))
            qty = int(input("Quantity: "))
            prod = Product.get_product(pid)
            if prod is None:
                print("No such product")
                continue
            current_customer.cart.add_to_cart(prod, qty)
            print("Added to cart")
        elif choice == "6":
            if current_customer is None:
                print("Login as customer first")
                continue
            if not current_customer.cart.items:
                print("Cart is empty")
                continue
            for pid, qty in current_customer.cart.items.items():
                p = Product.get_product(pid)
                print(f"{p.product_name} x{qty} = ${p.product_price * qty}")
        elif choice == "7":
            if current_customer is None:
                print("Login as customer first")
                continue
            order = current_customer.cart.place_order()
            if order:
                print("Order placed", order.order_id, "total=", order.total_price)
            else:
                print("Nothing to order")
        elif choice == "8":
            if current_customer is None or not current_customer.orders:
                print("No orders to pay")
                continue
            order = current_customer.orders[-1]
            paytype = input("Payment type: ")
            pay = Payment(payment_type=paytype)
            pay.make_payment(order)
            print("Payment status:", order.payment.payment_status)
        elif choice == "9":
            # shipping performed by admin
            user = input("Admin username: ")
            pwd = input("Password: ")
            admin = Admin(username=user, password=pwd, admin_name=user)
            if admin.login(pwd):
                # ship last order of the last customer for simplicity
                if not customers:
                    print("No customers/orders")
                    continue
                target = customers[-1]
                if not target.orders:
                    print("Target has no orders")
                    continue
                order = target.orders[-1]
                addr = input("Shipping address: ")
                ship = Shipping(shipping_address=addr)
                ship.ship_order(order)
                print("Shipped order", order.order_id)
            else:
                print("Admin auth failed")
        else:
            print("Unknown choice")


def demo():
    # replicate earlier demo but using the CLI flows
    admin = Admin(username="admin", password="secret", admin_name="SiteAdmin")
    p1 = admin.add_product("Widget", "A useful widget", 9.99)
    p2 = admin.add_product("Gadget", "A shiny gadget", 19.99)
    print("Products:", Product.list_products())

    cust = Customer(username="jdoe", password="pwd", customer_name="John Doe", email="j@x.com")
    cust.cart.add_to_cart(p1, 2)
    cust.cart.add_to_cart(p2, 1)
    order = cust.cart.place_order()
    print("Placed order:", order.order_id, "total=", order.total_price)

    pay = Payment(payment_type="CreditCard")
    pay.make_payment(order)
    print("Payment status:", order.payment.payment_status)

    ship = Shipping(shipping_address="123 Main St")
    ship.ship_order(order)
    print("Order status:", order.order_status)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo()
    else:
        interactive()
