from discount_strategy import DiscountStrategy, NoDiscount
from order_line import OrderLine
from Products import Product


class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []      # composition: the Order creates its own lines
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> None:
        self.order_lines = [line for line in self.order_lines
                            if line.product.product_id != product_id]

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_information(self) -> None:
        print(f"Order {self.order_id}")
        for line in self.order_lines:
            print(f"  {line.product.name} x {line.quantity} = ${line.calculate_subtotal():.2f}")
        print(f"  Total after discount: ${self.calculate_total():.2f}")