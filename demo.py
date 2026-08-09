"""Small demo showing usage of the Amazon UML models."""
from Amazon import Customer, Admin, Product, Payment, Shipping


def run_demo():
    # Admin adds products
    admin = Admin(username="admin", password="secret", admin_name="SiteAdmin")
    p1 = admin.add_product("Widget", "A useful widget", 9.99)
    p2 = admin.add_product("Gadget", "A shiny gadget", 19.99)
    print("Products:", Product.list_products())

    # Customer registers and uses cart
    cust = Customer(username="jdoe", password="pwd", customer_name="John Doe", email="j@x.com")
    cust.cart.add_to_cart(p1, 2)
    cust.cart.add_to_cart(p2, 1)
    order = cust.cart.place_order()
    print("Placed order:", order.order_id, "total=", order.total_price)

    # Make payment
    pay = Payment(payment_type="CreditCard")
    pay.make_payment(order)
    print("Payment status:", order.payment.payment_status)

    # Ship order
    ship = Shipping(shipping_address="123 Main St")
    ship.ship_order(order)
    print("Order status:", order.order_status)


if __name__ == "__main__":
    run_demo()
