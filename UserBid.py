import uuid


class UserBid:
    def __init__(self, bidAmount, bidUser):
        self.__bidAmount = bidAmount
        self.__bidId = self.generate_bid_id()
        self.__bidUser = bidUser

    def set_bidAmount(self, bidAmount):
        self.__bidAmount = bidAmount

    def get_bidAmount(self):
        return self.__bidAmount

    def set_bidUser(self, bidUser):
        self.__bidUser = bidUser

    def get_bidUser(self):
        return self.__bidUser

    def generate_bid_id(self):
        return "User" + "".join(str(uuid.uuid4())[::2].split("-"))

    def get_bidId(self):
        return self.__bidId

    def __str__(self):
        s = "bid_amount for name {}, id {} == {}".format(self.get_bidUser(), self.__bidId, self.get_bidAmount())
        return s
