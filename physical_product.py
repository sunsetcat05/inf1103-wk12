from Products import Product


class PhysicalProduct(Product):
    def display_information(self) -> None:
        print("Type: Physical product")
        super().display_information()

    def get_fulfilment_info(self) -> str:
        return "Packed and shipped to the customer's address."