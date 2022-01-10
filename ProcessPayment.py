from Product import Product


class ProcessPayment(Product):
    def __init__(self, name, description, price, quantity, category, discount, top):
        super().__init__(name, description, price, quantity, category, discount, top)