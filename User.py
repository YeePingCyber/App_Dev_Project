# Version 0.1
import hashlib as hl

class User:
    def __init__(self, fname, lname, email, password):
        self.__firstname = fname
        self.__lastname = lname
        self.__email = email
        self.__password = self.hashing_pwsd(password)
        self.__picture = None

    def set_picture(self, picture):
        self.__picture = picture

    def get_picture(self):
        return self.__picture
    def set_first_name(self, fname):
        self.__firstname = fname

    def set_last_name(self, lname):
        self.__lastname = lname

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = self.hashing_pwsd(password)

    def get_first_name(self):
        return self.__firstname

    def get_last_name(self):
        return self.__lastname

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def hashing_pwsd(self, pwsd):
        return hl.pbkdf2_hmac('sha256', str(pwsd).encode(), b'salt', 100000).hex()
