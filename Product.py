from Goods import Goods
import uuid


class Product(Goods):
    def __init__(self, name, description, price, quantity, category, discount):
        super().__init__(name, description, price, quantity)
        self.product_id = self.generate_product_id()
        self.__discount = discount
        self.__discounted_price = price - price * self.__discount
        self.__category = category
        self.__sold_units = 0

    def set_category(self, category):
        self.__category = category

    def set_discount(self, discount):
        self.__discount = discount

    def increase_sold_units(self, sold):
        self.__sold_units += sold
        self.decrease_quantity(sold)

    def get_category(self):
        return self.__category

    def get_discount(self):
        return self.__discount

    def get_sold_units(self):
        return self.__sold_units

    def get_product_id(self):
        return self.product_id

    def calculate_new_price(self):
        self.__discounted_price = self.get_price() - self.get_price() * self.__discount

    def get_discounted_price(self):
        return self.__discounted_price

    def generate_product_id(self):
        return "".join(str(uuid.uuid4())[::2].split("-"))

    def __str__(self):
        return f"{self.get_product_id(), self.get_name(), self.get_description(), self.get_price(), self.get_quantity(), self.get_category(), self.get_discount()}"