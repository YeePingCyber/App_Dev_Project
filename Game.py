import random

class PlayerStatus:
    def __init__(self, customerID, today, nextDay):
        self.__customerID = customerID
        self.__totalPoints = 0
        self.__today = today
        self.__nextDay = nextDay
        self.__discount_code = ""

    def set_customer_id(self, customerID):
        self.__customerID = customerID

    def set_today(self, today):
        self.__today = today

    def set_total_zero(self):
        self.__totalPoints = 0

    def set_next_day(self, nextDay):
        self.__nextDay = nextDay

    def get_customer_id(self):
        return self.__customerID

    def get_total_points(self):
        return self.__totalPoints

    def get_today(self):
        return self.__today

    def get_next_day(self):
        return self.__nextDay

    def calculate_total_points(self, points=0, multiplier=0):
        if points == 0:
            self.__totalPoints *= multiplier
        else:
            self.__totalPoints += points

    def generate_discount_code(self, position):
        discount_code_dict = {0: "TPFreeBag2022", 1: "TP70%Discount2022", 2: "TP50%Discount2022", 3: "TP30%Discount2022",
                              4: "TP10%Discount2022", 5: "TP5%Discount2022"}

        if (position > 5) and (position <= 9):
            position = 5

        self.__discount_code = discount_code_dict[position]

    def get_discount_code(self):
        return self.__discount_code


# Function for a list of different amount of points
def generate_points():
    points_and_multiplier = {0:"x5", 1:"x4", 2:"x3", 3:"x2", 4:"50", 5:"40", 6:"30", 7:"20", 8:"10"}

    point_list = []

    while len(point_list) < 3:
        random_dict_key = random.randint(0, 8)
        p_and_m_dict = {random_dict_key:points_and_multiplier[random_dict_key]}
        if p_and_m_dict in point_list:
            continue
        else:
            point_list.append(p_and_m_dict)

    return point_list

# h = generate_points()
# print(h)
# print(list(h[0].keys())[0])
# print(list(h[0].values())[0])

# list(point_list[0].keys())