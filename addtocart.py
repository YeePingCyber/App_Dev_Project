from Product import Product
from uuid import uuid4


class Addtocart(Product):
    def __init__(self, name, description, price, quantity, category, discount):
        super().__init__(name, price, quantity, category, discount, description)
        self.__id = str(uuid4())

    def get_id(self):
        return self.__id

    def __str__(self):
        return f"{self.get_id()}"