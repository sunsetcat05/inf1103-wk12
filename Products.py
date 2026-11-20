from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier):
        self.product_id: str = product_id
        self.name: str = name
        self.price = price                      # validated by the setter below
        self.stock_quantity = stock_quantity    # validated by the setter below
        self.supplier: Supplier = supplier      # association: a reference, not ownership

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Price must be greater than zero.")
        self._price = value

    @property
    def stock_quantity(self) -> int:
        return self._stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value: int) -> None:
        if value < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock_quantity = value

    def update_stock(self, quantity: int) -> None:
        """Add quantity to the stock (use a negative number to remove stock)."""
        self.stock_quantity = self.stock_quantity + quantity

    def display_information(self) -> None:
        print(f"[{self.product_id}] {self.name} - ${self.price:.2f} - Stock: {self.stock_quantity}")
        print(f"  Supplier: {self.supplier.name} ({self.supplier.contact_email})")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass