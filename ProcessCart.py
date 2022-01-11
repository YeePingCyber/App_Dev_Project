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

    def get_id(self):
        return self.__shippingid

    def get_email(self):
        return self.__email

    def get_firstname(self):
        return self.__first_name

    def get_lastname(self):
        return self.__last_name

    def get_address(self):
        return self.__address

    def get_postal(self):
        return self.__postal_code

    def get_phone(self):
        return self.__phone


class PaymentProcess:
    def __init__(self, card_num, name_card, expire, ccv):
        self.__card_num = card_num
        self.__name_card = name_card
        self.__expire = expire
        self.__ccv = ccv
        self.__paymentid = str(uuid4())

    def get_card(self):
        return self.__card_num


class Output(ShippingProcess, PaymentProcess):
    def __init__(self, email, country, first_name, last_name, address, postal_code, city, phone, card_num, name_card, expire, ccv):
        ShippingProcess.__init__(self, email, country, first_name, last_name, address, postal_code, city, phone)
        PaymentProcess.__init__(self, card_num, name_card, expire, ccv)
