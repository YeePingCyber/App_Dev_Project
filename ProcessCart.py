from uuid import uuid4


class ShippingProcess:
    def __init__(self, email, country, first_name, last_name, address, postal_code, city, phone):
        self.__email = email
        self.__country = country
        self.__first_name = first_name
        self.__last_name = last_name
        self.__address = address
        self.__postal_code = postal_code
        self.__city = city
        self.__phone = phone
        self.__shippingid = str(uuid4())

    def get_shippingid(self):
        return self.__shippingid

    def get_email(self):
        return self.__email

    def get_country(self):
        return self.__country

    def get_firstname(self):
        return self.__first_name

    def get_lastname(self):
        return self.__last_name

    def get_address(self):
        return self.__address

    def get_postal(self):
        return self.__postal_code

    def get_city(self):
        return self.__city

    def get_phone(self):
        return self.__phone


class PaymentProcess:
    def __init__(self, card_num, name_card, expire, ccv):
        self.__card_num = card_num
        self.__name_card = name_card
        self.__expire = expire
        self.__ccv = ccv
        self.__paymentid = str(uuid4())

    def get_paymentid(self):
        return self.__paymentid

    def get_cardnum(self):
        return self.__card_num

    def get_namecard(self):
        return self.__name_card

    def get_expire(self):
        return self.__expire

    def get_ccv(self):
        return self.__ccv


class Sales(ShippingProcess, PaymentProcess):
    def __init__(self, email, country, first_name, last_name, address, postal_code, city, phone, card_num, name_card,expire, ccv, cart):
        ShippingProcess.__init__(self, email, country, first_name, last_name, address, postal_code, city, phone)
        PaymentProcess.__init__(self, card_num, name_card, expire, ccv)
        self.__cart = cart


    def get_cart(self):
        return self.__cart



    def __str__(self):
        return f"{self.get_cart(), self.get_shippingid(), self.get_paymentid(), self.get_email(), self.get_firstname(), self.get_lastname(), self.get_address(), self.get_postal(), self.get_city(), self.get_phone(), self.get_cardnum(), self.get_namecard(), self.get_expire(), self.get_ccv()}"
