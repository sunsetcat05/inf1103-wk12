from product import Product


class DigitalProduct(Product):
    def display_information(self) -> None:
        print("Type: Digital product")
        super().display_information()

    def get_fulfilment_info(self) -> str:
        return "Delivered instantly as a download link."