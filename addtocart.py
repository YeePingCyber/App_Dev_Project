from Product import Product
from uuid import uuid4


class Addtocart(Product):
    cart_quantity = 0
    def __init__(self, name, description, price, quantity, category, discount, top):
        super().__init__(name, description, price, quantity, category, discount, top)
        self.__id = str(uuid4())
        self.__class__.cart_quantity += 1

    def get_id(self):
        return self.__id

    def __str__(self):
        return f"{self.get_id()}"