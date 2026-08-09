from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, ClassVar
import itertools


# Simple ID generators
_id_counter = itertools.count(1)
def _next_id() -> int:
    return next(_id_counter)


@dataclass
class User:
    username: str
    password: str
    logged_in: bool = field(default=False, init=False)

    def login(self, password: str) -> bool:
        if password == self.password:
            self.logged_in = True
            return True
        return False

    def logout(self) -> None:
        self.logged_in = False


@dataclass
class Customer(User):
    customer_name: str
    email: str
    customer_id: int = field(default_factory=_next_id)
    cart: "Cart" = field(default=None)
    orders: List["Order"] = field(default_factory=list)

    def __post_init__(self):
        if self.cart is None:
            self.cart = Cart(owner=self)

    def register(self) -> None:
        # placeholder for registration logic
        pass

    def update_profile(self, name: Optional[str] = None, email: Optional[str] = None) -> None:
        if name:
            self.customer_name = name
        if email:
            self.email = email


@dataclass
class Admin(User):
    admin_id: int = field(default_factory=_next_id)
    admin_name: str = "admin"

    def add_product(self, name: str, description: str, price: float) -> "Product":
        return Product.add_product(name=name, description=description, price=price)

    def remove_product(self, product_id: int) -> bool:
        return Product.remove_product(product_id)


@dataclass
class Product:
    product_name: str
    product_description: str
    product_price: float
    product_id: int = field(default_factory=_next_id)

    _catalog: ClassVar[Dict[int, "Product"]] = {}

    @classmethod
    def add_product(cls, name: str, description: str, price: float) -> "Product":
        p = Product(product_name=name, product_description=description, product_price=price)
        cls._catalog[p.product_id] = p
        return p

    @classmethod
    def remove_product(cls, product_id: int) -> bool:
        return cls._catalog.pop(product_id, None) is not None

    @classmethod
    def get_product(cls, product_id: int) -> Optional["Product"]:
        return cls._catalog.get(product_id)

    @classmethod
    def list_products(cls) -> List["Product"]:
        return list(cls._catalog.values())


@dataclass
class Cart:
    owner: Customer
    cart_id: int = field(default_factory=_next_id)
    items: Dict[int, int] = field(default_factory=dict)  # product_id -> quantity

    def add_to_cart(self, product: Product, quantity: int = 1) -> None:
        if product.product_id in self.items:
            self.items[product.product_id] += quantity
        else:
            self.items[product.product_id] = quantity

    def remove_from_cart(self, product: Product, quantity: int = 1) -> None:
        pid = product.product_id
        if pid not in self.items:
            return
        self.items[pid] -= quantity
        if self.items[pid] <= 0:
            del self.items[pid]

    def clear(self) -> None:
        self.items.clear()

    def place_order(self) -> Optional["Order"]:
        if not self.items:
            return None
        items_snapshot: List[Tuple[Product, int]] = []
        total = 0.0
        for pid, qty in self.items.items():
            prod = Product.get_product(pid)
            if prod is None:
                continue
            items_snapshot.append((prod, qty))
            total += prod.product_price * qty
        order = Order(items=items_snapshot, total_price=total, customer=self.owner)
        self.owner.orders.append(order)
        self.clear()
        return order


@dataclass
class Order:
    items: List[Tuple[Product, int]]
    total_price: float
    customer: Customer
    order_id: int = field(default_factory=_next_id)
    order_date: datetime = field(default_factory=datetime.utcnow)
    order_status: str = field(default="Placed")
    payment: Optional["Payment"] = None
    shipping: Optional["Shipping"] = None

    def place_order(self) -> None:
        self.order_status = "Placed"

    def set_payment(self, payment: "Payment") -> None:
        self.payment = payment

    def set_shipping(self, shipping: "Shipping") -> None:
        self.shipping = shipping


@dataclass
class Payment:
    payment_type: str
    payment_status: str = field(default="Pending")
    payment_id: int = field(default_factory=_next_id)

    def make_payment(self, order: Order) -> bool:
        # in a real system we'd integrate with a gateway. Here we simulate success.
        self.payment_status = "Completed"
        order.set_payment(self)
        return True


@dataclass
class Shipping:
    shipping_address: str
    shipping_status: str = field(default="Pending")
    shipping_id: int = field(default_factory=_next_id)

    def ship_order(self, order: Order) -> bool:
        # simulate shipping process
        self.shipping_status = "Shipped"
        order.set_shipping(self)
        order.order_status = "Shipped"
        return True
