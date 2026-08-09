from .models import (
	User,
	Customer,
	Admin,
	Product,
	Cart,
	Order,
	Payment,
	Shipping,
)

__all__ = [
	"User",
	"Customer",
	"Admin",
	"Product",
	"Cart",
	"Order",
	"Payment",
	"Shipping",
]

def main() -> None:
	print("Amazon UML models available: import from Amazon.models")


if __name__ == "__main__":
	main()
