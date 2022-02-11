from User import User
from random import randint
from time import time


class Customer(User):
    def __init__(self, fname, lname, birth_date, email, password):
        super().__init__(fname, lname, email, password)
        self.__birthdate = birth_date
        self.__customer_id = randint(1, 10000)
        # When i sort out the time of creation i will get to this
        # for now ill do random integers-Dylan
        self.__contact_number = None
        self.__points = 0
        self.__address = None

    def set_birthdate(self, date):
        self.__birthdate = date

    def set_contact_number(self, number):
        self.__contact_number = number

    def set_address(self, address):
        self.__address = address

    def set_points(self, points):
        self.__points = points

    def get_birth_date(self):
        return self.__birthdate

    def get_contact_number(self):
        return self.__contact_number

    def get_address(self):
        return self.__address

    def get_points(self):
        return self.__points

    def get_customer_id(self):
        return self.__customer_id

    # How do you guys want to calculate points?
    def calculate_points(self, cost):
        self.__points = round(cost/5)
