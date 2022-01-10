class UserBid:
    def __init__(self, bidAmount):
        self.__bidAmount = bidAmount

    def set_bidAmount(self, bidAmount):
        self.__bidAmount = bidAmount

    def get_bidAmount(self):
        return self.__bidAmount
