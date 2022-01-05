from User import User


class Customer(User):
    def __init__(self, fname, lname, email, password, birth_date):
        super().__init__(fname, lname, email, password)
        self.__birthdate = birth_date
        self.__customer_id = None
        # When i sort out the time of creation i will get to this -Dylan
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
    def calculate_points(self):
        pass
        # return round(price/5)
        # OR
        # return round(price/10)

    def __str__(self):
        return f"{self.get_first_name()} ,{self.get_last_name()}, {self.get_email()}, {self.get_password()}, {self.get_birth_date()}"
