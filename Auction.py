from Goods import Goods
import uuid


class Auction(Goods):
    def __init__(self, name, description, price, minimumAmount, startDate, endDate):
        super().__init__(name, description, price, quantity=1)
        self.__auction_id = self.generate_auction_id()
        self.__minimumAmount = minimumAmount
        self.__startDate = startDate
        self.__endDate = endDate
        self.__total = price

    def set_minimum_amount(self, minimumAmount):
        self.__minimumAmount = minimumAmount

    def set_start_date(self, startDate):
        self.__startDate = startDate

    def set_end_date(self, endDate):
        self.__endDate = endDate

    def get_auction_id(self):
        return self.__auction_id

    def get_minimum_amount(self):
        return self.__minimumAmount

    def get_start_date(self):
        return self.__startDate

    def get_end_date(self):
        return self.__endDate

    def calculate_total(self):
        self.__total += self.__minimumAmount

    def generate_auction_id(self):
        return "AU" + "".join(str(uuid.uuid4())[::2].split("-"))
