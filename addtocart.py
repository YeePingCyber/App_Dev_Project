from Product import Product
from uuid import uuid4


class Addtocart(Product):
    def __init__(self, name, description, price, quantity, category, discount, top):
        super().__init__(name, price, quantity, category, discount, description, top)
        self.__id = str(uuid4())
        self.__picture = None

    def get_picture(self):
        return self.__picture

    def set_picture(self, picture):
        self.__picture = picture

    def get_id(self):
        return self.__id

    def __str__(self):
        return f"{self.get_id(), self.get_name(), self.get_picture()}"