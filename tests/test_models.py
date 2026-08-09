from Amazon import Product, Admin, Customer, Payment, Shipping


def test_product_and_order_flow():
    # clear any existing catalog
    for p in list(Product.list_products()):
        Product.remove_product(p.product_id)

    admin = Admin(username="a", password="p", admin_name="A")
    p1 = admin.add_product("X", "x", 5.0)
    p2 = admin.add_product("Y", "y", 2.5)

    cust = Customer(username="c", password="p", customer_name="C", email="c@example.com")
    cust.cart.add_to_cart(p1, 1)
    cust.cart.add_to_cart(p2, 2)
    order = cust.cart.place_order()
    assert order is not None
    assert order.total_price == 5.0 + 2 * 2.5

    pay = Payment(payment_type="Test")
    assert pay.make_payment(order)
    assert order.payment.payment_status == "Completed"

    ship = Shipping(shipping_address="Addr")
    assert ship.ship_order(order)
    assert order.order_status == "Shipped"
