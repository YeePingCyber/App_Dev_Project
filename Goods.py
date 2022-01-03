class Goods:
    def __init__(self, name, description, price, quantity):
        self.__name = name
        self.__description = description
        self.__price = price
        self.__quantity = quantity

    def set_name(self, name):
        self.__name = name

    def set_description(self, desc):
        self.__description = desc

    def set_price(self, price):
        self.__price = price

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    def decrease_quantity(self, minus_amount):
        self.__quantity -= minus_amount

    def increase_quantity(self, increase_amount):
        self.__quantity += increase_amount
