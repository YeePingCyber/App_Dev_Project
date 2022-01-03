from Goods import Goods


class Product(Goods):
    def __init__(self, name, description, price, quantity, category, discount):
        super().__init__(name, description, price, quantity)
        self.__discounted_price = price - price * self.__discount
        self.__category = category
        self.__discount = discount
        self.__sold_units = 0
        # I'll do the product ID later on

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

    def calculate_new_price(self):
        self.__discounted_price = self.get_price() - self.get_price() * self.__discount

    def get_discounted_price(self):
        return self.__discounted_price
