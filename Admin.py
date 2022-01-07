from User import User


class Admin(User):
    def __init__(self, fname, lname, email, password, employee_id):
        super().__init__(fname, lname, email, password)
        self.__admin_id = int(employee_id)

    def set_admin_id(self, id):
        self.__admin_id = id

    def get_admin_id(self):
        return self.__admin_id

    # Discount code generation will be done ltr on -Dylan
