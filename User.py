# Version 0.1
class User:
    def __init__(self, fname, lname, email, password):
        self.__firstname = fname
        self.__lastname = lname
        self.__email = email
        self.__password = password

# Ill try to do epoch timing for time of creation later on - Dylan
# Hashing and password security we do later on - Dylan

    def set_first_name(self, fname):
        self.__firstname = fname

    def set_last_name(self, lname):
        self.__lastname = lname

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def get_first_name(self):
        return self.__firstname

    def get_last_name(self):
        return self.__lastname

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password
