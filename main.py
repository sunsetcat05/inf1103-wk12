from discount_strategy import BulkDiscount, PercentageDiscount, StudentDiscount
from input_helpers import get_positive_float
from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from product_loader import load_products
from supplier import Supplier


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def main() -> None:
    supplier = Supplier("SUP01", "Acme Supplies", "sales@acme.example")
    inventory = Inventory()

    print("--- Loading products from products.csv ---")
    load_products("products.csv", inventory, supplier)

    print("\n--- Inventory (polymorphism through Product) ---")
    for product in inventory.products:
        show_product_details(product)

    print("\n--- Factory and validation errors ---")
    try:
        ProductFactory.create("service", "S002", "Setup", 30.0, 1, supplier)
    except ValueError as error:
        print(f"Could not create product: {error}")
    try:
        ProductFactory.create("physical", "P999", "Free Pen", 0, 1, supplier)
    except ValueError as error:
        print(f"Could not create product: {error}")

    print("\n--- Create a product using validated user input ---")
    price = get_positive_float("Enter a price for a new desk (try 125): ")
    desk = ProductFactory.create("physical", "P100", "Standing Desk", price, 4, supplier)
    inventory.add_product(desk)
    show_product_details(desk)

    print("\n--- Strategy pattern: order discounts ---")
    order = Order("O1")
    order.add_order_line(desk, 2)
    print(f"No discount:         {order.calculate_total():.2f}")

    order.set_discount(BulkDiscount(200, 20))
    print(f"Bulk (200 -> 20 off): {order.calculate_total():.2f}")

    order.set_discount(PercentageDiscount(10))
    print(f"Percentage (10%):    {order.calculate_total():.2f}")

    order.set_discount(StudentDiscount())
    print(f"Student (5%):        {order.calculate_total():.2f}")

    print()
    order.display_information()


if __name__ == "__main__":
    main()