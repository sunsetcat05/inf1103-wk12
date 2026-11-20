import inspect
import unittest

from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount, StudentDiscount)
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


def make_order(discount=None) -> Order:
    """An order whose lines add up to 250."""
    supplier = Supplier("SUP01", "Acme Supplies", "sales@acme.example")
    product = ProductFactory.create("physical", "P001", "Desk", 125.0, 10, supplier)
    order = Order("O1", discount)
    order.add_order_line(product, 2)
    return order


class TestOrderDiscounts(unittest.TestCase):
    def test_default_is_no_discount(self):
        order = make_order()
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_bulk_discount_applies_at_threshold(self):
        self.assertAlmostEqual(make_order(BulkDiscount(200, 20)).calculate_total(), 230.0)

    def test_bulk_discount_not_applied_below_threshold(self):
        self.assertAlmostEqual(make_order(BulkDiscount(300, 20)).calculate_total(), 250.0)

    def test_percentage_discount(self):
        self.assertAlmostEqual(make_order(PercentageDiscount(10)).calculate_total(), 225.0)

    def test_student_discount(self):
        self.assertAlmostEqual(make_order(StudentDiscount()).calculate_total(), 237.5)

    def test_set_discount_changes_strategy(self):
        order = make_order(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_new_strategy_works_without_changing_order(self):
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2

        self.assertAlmostEqual(make_order(HalfPrice()).calculate_total(), 125.0)

    def test_order_has_no_discount_branching(self):
        source = inspect.getsource(Order.calculate_total)
        self.assertNotIn("if ", source)
        self.assertNotIn("elif", source)


if __name__ == "__main__":
    unittest.main()