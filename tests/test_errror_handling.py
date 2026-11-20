import contextlib
import io
import os
import tempfile
import unittest
from unittest.mock import patch

from input_helpers import get_positive_float
from inventory import Inventory
from product_loader import load_products
from supplier import Supplier

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def run_and_capture(func, *args):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


class TestGetPositiveFloat(unittest.TestCase):
    def test_reprompts_until_valid(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            value, output = run_and_capture(get_positive_float, "Price: ")
        self.assertEqual(value, 12.5)
        self.assertIn("Please enter a valid number", output)
        self.assertIn("greater than zero", output)


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP01", "Acme Supplies", "sales@acme.example")

    def test_missing_file_is_handled(self):
        inventory = Inventory()
        _, output = run_and_capture(load_products, "does_not_exist.csv", inventory, self.supplier)
        self.assertIn("Products file not found", output)
        self.assertIn("Load attempt finished.", output)
        self.assertNotIn("products loaded", output)
        self.assertEqual(len(inventory.products), 0)

    def test_bad_rows_are_skipped_and_valid_rows_load(self):
        inventory = Inventory()
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", newline="") as f:
                f.write(CSV_TEXT)
            _, output = run_and_capture(load_products, path, inventory, self.supplier)

        self.assertEqual(len(inventory.products), 3)
        self.assertEqual(output.count("Skipping row"), 2)
        self.assertIn("3 products loaded.", output)
        self.assertTrue(output.strip().endswith("Load attempt finished."))


if __name__ == "__main__":
    unittest.main()