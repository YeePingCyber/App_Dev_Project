from Product import Product


def load_product():
    product_list = dict()

    # name: str, description: str, price: double, quantity: int, category: str, discount: int
    p1 = Product("Bag 1", "This is an expensive bag", 200.00, 10, "Female", 0)
    product_list[p1.get_product_id()] = p1

    p2 = Product("Bag 2", "This is an expensive bag", 150.00, 10, "Female", 0)
    product_list[p2.get_product_id()] = p2

    p3 = Product("Bag 3", "This is an expensive bag", 50.00, 10, "Female", 0)
    product_list[p3.get_product_id()] = p3

    p4 = Product("Bag 4", "This is an expensive bag", 240.00, 10, "Male", 0)
    product_list[p4.get_product_id()] = p4

    p5 = Product("Bag 5", "This is an expensive bag", 130.00, 10, "Male", 0)
    product_list[p5.get_product_id()] = p5

    p6 = Product("Bag 6", "This is an expensive bag", 70.00, 10, "Male", 0)
    product_list[p6.get_product_id()] = p6

    return product_list
