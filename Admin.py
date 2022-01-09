from User import User
from random import randint


class Admin(User):
    def __init__(self, fname, lname, email, password, employee_id):
        super().__init__(fname, lname, email, password)
        self.__admin_id = randint(1, 10000)
        self.__employee_id = employee_id

    def set_employee_id(self, id):
        self.__employee_id = id

    def set_admin_id(self, id):
        self.__admin_id = id

    def get_employee_id(self):
        return self.__employee_id

    def get_admin_id(self):
        return self.__admin_id

    # Discount code generation will be done ltr on -Dylan
