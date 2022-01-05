from Customer import Customer
from Product import Product


class UserCart(Customer):
    count = 0

    def __init__(self, fname, lname, email, password, birth_date):
        super().__init__(fname, lname, email, password, birth_date)
        self.__class__.count += 1

# print(UserCart("teo", "szeyan", "sz3yan@gmail.com", "sy", "12/01/2003"))
