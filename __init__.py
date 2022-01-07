from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for
import shelve
import hashlib as hl
from datetime import date
from Customer import Customer
from Admin import Admin
from User import User
from addtocart import Addtocart
from Auction import Auction
from Forms import CreateAdminForm, CreateLoginForm, CreateCustomerForm, CreatePaymentForm, CreateProductForm, CreateAddCartForm, CreateAuctionForm


# create product function
from createProduct import load_product

app = Flask(__name__)


# Initilising Inventory
# inventory_dict = {}
# db = shelve.open("inventory", "c")
#
# try:
#     if "Inventory" in db:
#         inventory_dict = db["Inventory"]
#     else:
#         db["Inventory"] = inventory_dict
#
# except:
#     print("Error in retrieving Inventory from inventory.db")
#
# for x in range(4):
#     inventory = Product("Arkose 20L Modular Bacpack", "Everyday backpack + small camera insert", 140, 50, "Camera", 0)
#     inventory_dict[x] = inventory
#     db["Inventory"] = inventory_dict
#
# for x in inventory_dict:
#     print(inventory_dict[x])
# db.close()


# Customer Side
@app.route("/")
def home():
    # return render_template("adminAuction.html")
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def log_in():
    create_log_in_form = CreateLoginForm(request.form)
    if request.method == 'POST' and create_log_in_form.validate():
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        hashed_password = hl.pbkdf2_hmac('sha256', str(create_log_in_form.login_password.data).encode(), b'salt',100000).hex()
        for user in users_dict:
            if users_dict[user].get_email() == create_log_in_form.login_email.data and users_dict[user].get_password() == hashed_password:
                if isinstance(users_dict[user], Customer):
                    return redirect(url_for('home'))
                elif isinstance(users_dict[user], Admin):
                    return redirect((url_for('admin')))
        db.close()
    return render_template("loginpage.html", form=create_log_in_form)


@app.route("/register", methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        if create_customer_form.register_password.data == create_customer_form.confirm_password.data:
            customer_dict = {}
            db = shelve.open('user.db', 'c')
            try:
                customer_dict = db['Users']
            except:
                print("Error in retrieving Users from user.db")

            new_customer = Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                    create_customer_form.birthdate.data, create_customer_form.email.data,
                                    create_customer_form.register_password.data)
            customer_dict[new_customer.get_customer_id()] = new_customer
            print(new_customer.get_password())
            db['Users'] = customer_dict
            db.close()
            return redirect(url_for('home'))
        else:
            print("Password does not match!")
    return render_template("register.html", form=create_customer_form)


@app.route("/cart")
def cart():
    cartList = []
    cart_dict = {}
    db = shelve.open("addtocart", "c")
    try:
        if "Add_to_cart" in db:
            cart_dict = db["Add_to_cart"]
        else:
            db["Add_to_cart"] = cart_dict
    except:
        print("Error in retrieving Inventory from addtocart.db")

    for x in cart_dict:
        cartList.append(cart_dict[x])

    db.close()

    # print(cartList)

    if len(cartList) > 0:
        return render_template("cart.html", cart_list = cartList)
    else:
        return render_template("cart_empty.html")


@app.route('/deleteCart/<id>', methods=['POST'])
def delete_item(id):
    cartList = []
    cart_dict = {}
    db = shelve.open('addtocart', 'c')
    cart_dict = db['Add_to_cart']

    cart_dict.pop(id)

    for x in cart_dict:
        cartList.append(cart_dict[x])

    db['Add_to_cart'] = cart_dict
    db.close()

    if len(cartList) > 0:
        return redirect(url_for("cart"))
    else:
        return render_template("cart_empty.html")


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    create_payment_form = CreatePaymentForm(request.form)
    # if request.method == 'POST' and create_payment_form.validate():
    #     pass

    return render_template("checkout.html", form=create_payment_form)


@app.route("/mainshop", methods=['GET', 'POST'])
def mainshop():
    return render_template("mainshop.html")


@app.route("/bag1", methods=['GET', 'POST'])
def bag1():
    addtocartform = CreateAddCartForm(request.form)
    if request.method == "POST":
        addtocart_dict = {}
        db = shelve.open("addtocart", "c")

        try:
            if "Add_to_cart" in db:
                addtocart_dict = db["Add_to_cart"]
            else:
                db["Add_to_cart"] = addtocart_dict
        except:
            print("Error in retrieving Inventory from addtocart.db")

        addtocart = Addtocart(
            addtocartform.name.data,
            addtocartform.description.data,
            int(addtocartform.price.data),
            int(addtocartform.quantity.data),
            addtocartform.category.data,
            int(addtocartform.discount.data)
        )

        addtocart_dict[addtocart.get_id()] = addtocart
        print(addtocart_dict[addtocart.get_id()])
        db["Add_to_cart"] = addtocart_dict

    return render_template("bag1.html", form=addtocartform)


@app.route("/bag2", methods=['GET', 'POST'])
def bag2():
    addtocartform = CreateAddCartForm(request.form)
    if request.method == "POST":
        addtocart_dict = {}
        db = shelve.open("addtocart", "c")

        try:
            if "Add_to_cart" in db:
                addtocart_dict = db["Add_to_cart"]
            else:
                db["Add_to_cart"] = addtocart_dict
        except:
            print("Error in retrieving Inventory from addtocart.db")

        addtocart = Addtocart(
            addtocartform.name.data,
            addtocartform.description.data,
            int(addtocartform.price.data),
            int(addtocartform.quantity.data),
            addtocartform.category.data,
            int(addtocartform.discount.data)
        )

        addtocart_dict[addtocart.get_id()] = addtocart
        print(addtocart_dict[addtocart.get_id()])
        db["Add_to_cart"] = addtocart_dict

    return render_template("bag2.html", form=addtocartform)


# Admin Side
@app.route("/admin")
def admin():
    return render_template("adminDashboard.html")


@app.route("/adminAuction")
def adminAuction():
    try:
        db = shelve.open('auction', 'r')
        auction_dict = db["Auction"]
        db.close()
    except:
        auction_dict = {}

    today = date.today().strftime('%Y-%m-%d')
    upcoming = []
    ongoing = ""

    if auction_dict != {}:

        for keys, values in auction_dict.items():
            start = date.strftime(values.get_start_date(), '%Y-%m-%d')
            end = date.strftime(values.get_end_date(), '%Y-%m-%d')

            if start == today or today > start or start <= today and end <= today:
                ongoing = values
            elif start > today and end > today:
                upcoming.append(values)

    return render_template("adminAuction.html", ongoing=ongoing, upcoming=upcoming)



@app.route("/createAuction", methods=['GET', 'POST'])
def createAuction():
    create_auction = CreateAuctionForm(request.form)

    if request.method == "POST" and create_auction.validate():
        create_auction_dict = {}
        db = shelve.open("auction", "c")

        try:
            if "Auction" in db:
                create_auction_dict = db["Auction"]
            else:
                db["Auction"] = create_auction_dict
        except:
            print("Error in retrieving Inventory from auction.db")

        auction = Auction(create_auction.product_name.data, create_auction.description.data,
                          create_auction.base_amount.data, create_auction.minimum_amount.data,
                          create_auction.start_date.data, create_auction.end_date.data)

        create_auction_dict[auction.get_auction_id()] = auction
        db["Auction"] = create_auction_dict

        db.close()

        return redirect(url_for("adminAuction"))

    return render_template("createAuction.html", form=create_auction)


@app.route("/updateAuction/<id>/", methods=['GET', 'POST'])
def updateAuction(id):
    update_auction_form = CreateAuctionForm(request.form)
    if request.method == 'POST' and update_auction_form.validate():
        db = shelve.open("auction", 'w')
        auction_dict = db["Auction"]

        auction_dict.get(id).set_name(update_auction_form.product_name.data)
        auction_dict.get(id).set_description(update_auction_form.description.data)
        auction_dict.get(id).set_price(update_auction_form.base_amount.data)
        auction_dict.get(id).set_minimum_amount(update_auction_form.minimum_amount.data)
        auction_dict.get(id).set_start_date(update_auction_form.start_date.data)
        auction_dict.get(id).set_end_date(update_auction_form.end_date.data)

        db["Auction"] = auction_dict
        db.close()

        return redirect(url_for("adminAuction"))
    else:
        db = shelve.open("auction", 'r')
        auction_dict = db["Auction"]
        db.close()

        update_auction_form.product_name.data = auction_dict.get(id).get_name()
        update_auction_form.base_amount.data = auction_dict.get(id).get_price()
        update_auction_form.minimum_amount.data = auction_dict.get(id).get_minimum_amount()
        update_auction_form.start_date.data = auction_dict.get(id).get_start_date()
        update_auction_form.end_date.data = auction_dict.get(id).get_end_date()
        update_auction_form.description.data = auction_dict.get(id).get_description()

        return render_template("updateAuction.html", form=update_auction_form)


@app.route("/adminOrders")
def adminOrders():
    return render_template("adminOrders.html")


@app.route("/adminCustomerManagement")
def admin_customer_management():
    db = shelve.open('user.db','r')
    users_dict = db['Users']
    db.close()
    customer_list = []
    for user in users_dict:
        if isinstance(users_dict[user], Customer):
            customer = users_dict[user]
            customer_list.append(customer)

    return render_template("adminCustomerManagement.html", count = len(customer_list), customer_list=customer_list)


@app.route("/adminProductManagement")
def adminProductManagement():
    return render_template("adminProductManagement.html")


if __name__ == "__main__":
    app.run(debug=True)
