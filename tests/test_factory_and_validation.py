import unittest

from digital_product import DigitalProduct
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier


class TestProductFactory(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP01", "Acme Supplies", "sales@acme.example")

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, self.supplier)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, self.supplier)
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_type_raises_clear_value_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Install", 30.0, 5, self.supplier)
        self.assertIn("Unknown product type", str(context.exception))
        self.assertIn("service", str(context.exception))


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP01", "Acme Supplies", "sales@acme.example")

    def test_price_must_be_greater_than_zero(self):
        for bad_price in (0, -1):
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P1", "Lamp", bad_price, 10, self.supplier)

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Lamp", 25.0, -1, self.supplier)

    def test_zero_stock_is_allowed(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 0, self.supplier)
        self.assertEqual(product.stock_quantity, 0)

    def test_stock_cannot_be_set_negative_later(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            product.stock_quantity = -3
        with self.assertRaises(ValueError):
            product.update_stock(-10)

    def test_digital_product_enforces_same_rules(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "Editor", -5.0, 10, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "Editor", 5.0, -10, self.supplier)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 5, self.supplier)
        for bad_quantity in (0, -2):
            with self.assertRaises(ValueError):
                OrderLine(product, bad_quantity)


if __name__ == "__main__":
    unittest.main()