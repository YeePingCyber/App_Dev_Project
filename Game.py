import random

class PlayerStatus:
    def __init__(self, customerID, playableDate):
        self.__customerID = customerID
        self.__totalPoints = 0
        self.__playableDate = playableDate

    def set_customer_id(self, customerID):
        self.__customerID = customerID

    def set_total_points(self, totalPoints):
        self.__totalPoints = totalPoints

    def set_playable_date(self, playableDate):
        self.__playableDate = playableDate

    def get_customer_id(self):
        return self.__customerID

    def get_total_points(self):
        return self.__totalPoints

    def get_playable_date(self):
        return self.__playableDate


# Function for a list of different amount of points
def generate_points():
    points_and_multiplier = {0:"x5", 1:"x4", 2:"x3", 3:"x2", 4:"500", 5:"400", 6:"300", 7:"200", 8:"100"}

    point_list = []

    while len(point_list) < 3:
        random_dict_key = random.randint(0, 8)
        p_and_m_dict = {random_dict_key:points_and_multiplier[random_dict_key]}
        if p_and_m_dict in point_list:
            continue
        else:
            point_list.append(p_and_m_dict)

    return point_list

h = generate_points()
print(h)
print(list(h[0].keys())[0])
print(list(h[0].values())[0])

# list(point_list[0].keys())