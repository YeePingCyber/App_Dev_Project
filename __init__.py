from flask import Flask, render_template, flash
from flask import Flask, render_template, request, redirect, url_for, session
import shelve
import random
import hashlib as hl
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from Customer import Customer
from Admin import Admin
from User import User
from Product import Product
from addtocart import Addtocart
from Auction import Auction
from ProcessCart import PaymentProcess, ShippingProcess, Sales
from UserBid import UserBid
from Game import PlayerStatus, generate_points
from Forms import CreateAdminForm, CreateLoginForm, CreateCustomerForm, CreateShipmentForm, CreatePaymentForm, CreateProductForm, CreateAddCartForm, CreateAuctionForm, UpdateAdminForm, CreateBidForm, CreateForgetPassForm, UpdateCustomerForm, CreateProductView
from werkzeug.datastructures import CombinedMultiDict
import os
# from PIL import Image

app = Flask(__name__)
app.secret_key = "abc"


def save_picture(form_picture, id):
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_name = str(id) + str(f_ext)
    picture_path = os.path.join(app.root_path, "static", picture_name)
    form_picture.save(picture_path)
    print("saved")
    return picture_name


# Customer Side
@app.route("/")
def home():
    db = shelve.open("database/inventory.db", 'w')
    products_dict = db["Products"]
    db.close()

    db = shelve.open("database/trees.db", "c")
    trees = db["Trees"]

    return render_template("home.html", top4=products_dict, trees=trees)


@app.route("/login", methods=['GET', 'POST'])
def log_in():
    error = ""
    create_log_in_form = CreateLoginForm(request.form)
    if "customer_session" in session:
        return redirect(url_for('customer_logged_in'))
    else:
        if request.method == 'POST' and create_log_in_form.validate():
            db = shelve.open('database/user.db', 'r')
            users_dict = db['Users']
            hashed_password = hl.pbkdf2_hmac('sha256', str(create_log_in_form.login_password.data).encode(), b'salt',
                                             100000).hex()
            for user in users_dict:
                if users_dict[user].get_email().upper() == create_log_in_form.login_email.data.upper() and users_dict[user].get_password() == hashed_password:
                    if isinstance(users_dict[user], Customer):

                        # Session for customer
                        session["customer_session"] = users_dict[user].get_customer_id()
                        print(session["customer_session"])

                        # Delete Customer session
                        # session.pop("customer_session")
                        # print(session["customer_session"])

                        return redirect(url_for('customer_logged_in'))
                    elif isinstance(users_dict[user], Admin):

                        # Session for admin
                        session["admin_session"] = users_dict[user].get_admin_id()

                        # Delete Admin session
                        # session.pop("admin_session")
                        # print(session["customer_session"])

                        return redirect((url_for('admin')))
                elif users_dict[user].get_email() != create_log_in_form.login_email.data or users_dict[
                    user].get_password() != hashed_password:
                    error = "Invalid email or password"
            db.close()

        db = shelve.open("database/trees.db", "c")
        trees = db["Trees"]
        db.close()

        return render_template("loginpage.html", form=create_log_in_form, error=error, trees=trees)


@app.route("/logout", methods=['GET'])
def log_out():
    session.pop("customer_session", None)
    return redirect(url_for('log_in'))


@app.route("/user", methods=['GET', 'POST'])
def customer_logged_in():
    code = 0
    pw_code = 0
    error = ""
    picture_status = 0
    update_customer_form = UpdateCustomerForm(CombinedMultiDict((request.files, request.form)))
    if "customer_session" in session:
        customer = session["customer_session"]
        db = shelve.open('database/user.db', 'w')
        users_dict = db['Users']
        customer_user = users_dict.get(customer)
        path = "../static/images/profile_pics/"+str(customer_user.get_picture())
        # print(path)
        if customer_user.get_picture() is not None:
            picture_status = 1

        if request.method == "POST" and update_customer_form.validate():
            for user in users_dict:
                if isinstance(users_dict[user], Customer):
                    if update_customer_form.email.data.upper() == users_dict[user].get_email().upper() and customer != \
                            users_dict[user].get_customer_id():
                        code = 1
                        break
                if isinstance(users_dict[user], Admin):
                    if update_customer_form.email.data.upper() == users_dict[user].get_email().upper() and customer != \
                            users_dict[user].get_admin_id():
                        code = 1
                        break
            hashed_password = hl.pbkdf2_hmac('sha256', str(update_customer_form.current_password.data).encode(),
                                             b'salt', 100000).hex()
            if "profile_pic" in request.files:
                pic = update_customer_form.profile_pic.data
                fn = pic.filename.split(".")
                ext = fn[len(fn)-1]
                if ext == "jpg" or ext == "png":
                    pic_name = str(customer_user.get_customer_id()) + "." + str(ext)
                    try:
                        customer_user.set_picture(pic_name)
                        pic.save(os.path.join("static/images/profile_pics/", pic_name))
                        print("saved")
                    except:
                        print("upload failed")
            if "profile_picture" not in request.files:
                print("not saved")
            if update_customer_form.current_password.data == "" and code == 0:
                customer_user.set_first_name(update_customer_form.first_name.data)
                customer_user.set_last_name(update_customer_form.last_name.data)
                customer_user.set_email(update_customer_form.email.data)
                customer_user.set_birthdate(update_customer_form.birthdate.data)
                db['Users'] = users_dict
                db.close()
                return redirect(url_for('home'))
            elif update_customer_form.current_password.data != "" and code == 0 and hashed_password == customer_user.get_password():
                if hashed_password == customer_user.get_password():
                    customer_user.set_first_name(update_customer_form.first_name.data)
                    customer_user.set_last_name(update_customer_form.last_name.data)
                    customer_user.set_email(update_customer_form.email.data)
                    customer_user.set_birthdate(update_customer_form.birthdate.data)
                    customer_user.set_password(update_customer_form.new_password.data)
                    db['Users'] = users_dict
                    db.close()
                    return redirect(url_for('home'))
            else:
                pw_code = 1
                error = "Wrong password entered"
        else:
            update_customer_form.first_name.data = customer_user.get_first_name()
            update_customer_form.last_name.data = customer_user.get_last_name()
            update_customer_form.email.data = customer_user.get_email()
            update_customer_form.birthdate.data = customer_user.get_birth_date()

        db = shelve.open("database/trees.db", "c")
        trees = db["Trees"]
        db.close()

        return render_template("customer_logged_in.html", form=update_customer_form, error=error, code=code,
                               pw_code=pw_code, trees=trees, picture_status=picture_status, customer=customer_user, path=path)
    else:
        return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def create_customer():
    errortwo = ""
    code = 0
    create_customer_form = CreateCustomerForm(CombinedMultiDict((request.files, request.form)))
    db = shelve.open("database/trees.db", "c")
    trees = db["Trees"]
    db.close()

    if request.method == 'POST' and create_customer_form.validate():
        user_dict = {}
        db = shelve.open('database/user.db', 'r')
        user_dict = db['Users']
        for user in user_dict:
            print(user)
            if create_customer_form.email.data.upper() == user_dict[user].get_email().upper():
                errortwo = "There is an existing email registered"
                code = 1
                break
        if create_customer_form.register_password.data == create_customer_form.confirm_password.data and code == 0:
            customer_dict = {}
            db = shelve.open('database/user.db', 'c')
            try:
                customer_dict = db['Users']
            except:
                print("Error in retrieving Users from user.db")
            new_customer = Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                    create_customer_form.birthdate.data, create_customer_form.email.data,
                                    create_customer_form.register_password.data)
            customer_dict[new_customer.get_customer_id()] = new_customer

            if "profile_pic" in request.files:
                pic = create_customer_form.profile_pic.data
                fn = pic.filename.split(".")
                ext = fn[len(fn)-1]
                if ext == "jpg" or ext == "png":
                    pic_name = str(new_customer.get_customer_id()) + "." + str(ext)
                    try:
                        new_customer.set_picture(pic_name)
                        pic.save(os.path.join("static/images/profile_pics/", pic_name))
                        print("saved")
                    except:
                        print("upload failed")
            else:
                print("not saved")

            db['Users'] = customer_dict
            db.close()
            return redirect(url_for('log_in'))
        else:
            print("Password does not match!")

    return render_template("register.html", form=create_customer_form, erorrtwo=errortwo, code=code, trees = trees)


@app.route("/cart")
def cart():
    db = shelve.open("database/trees.db", "c")
    trees = db["Trees"]
    db.close()

    db = shelve.open("database/inventory.db", 'w')
    products_dict = db["Products"]
    db.close()

    listofDict = []
    listofKeys = []
    for i in range(1, len(products_dict) + 1):
        listofKeys.append(str(i))
        i = dict()
        listofDict.append(i)

    if "customer_session" in session:
        customer = session["customer_session"]
        db = shelve.open("database/user.db", "w")
        users_dict = db["Users"]
        customer_user = users_dict.get(customer)

        cart_dict = dict(zip(listofKeys, listofDict))

        cartList = []
        for j in range(1, len(products_dict) + 1):
            j = list()
            cartList.append(j)

        db = shelve.open("database/addtocart", "c")
        try:
            if "Add_to_cart" in db:
                temp = db["Add_to_cart"]

                if len(products_dict) == len(temp):
                    cart_dict = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dict = dict(zip(new_listofKeys, new_listofDict))

                    cart_dict.update(temp)

            else:
                db["Add_to_cart"] = cart_dict
        except:
            print("Error in retrieving Inventory from addtocart.db")

        for i, j in zip(cart_dict, products_dict):
            for y in cart_dict[i]:
                cart_dict[i][y].set_price(products_dict[j].get_price())
        db.close()

        for i in cart_dict:
            for y in cart_dict[i]:
                cartList[int(i) - 1].append(cart_dict[i][y])

        if any(len(cart_dict[y]) > 0 for y in cart_dict):
            subtotal = 0
            for total in range(0, len(cartList)):
                for x in cartList[total]:
                    subtotal += x.get_price()

            return render_template("cart.html", cartList=cartList, subtotal=subtotal, trees=tree)
        else:
            return render_template("cart_empty.html", trees=trees)

    else:
        temp = {}
        cart_dictnosession = dict(zip(listofKeys, listofDict))

        cartListnosession = []
        for j in range(1, len(products_dict) + 1):
            j = list()
            cartListnosession.append(j)

        db = shelve.open("database/addtocartnosession", "c")
        try:
            if "Add_to_cartnosession" in db:
                temp = db["Add_to_cartnosession"]
                print(len(products_dict), "in invenetory", len(temp), "in database")

                if len(products_dict) == len(temp):
                    cart_dictnosession = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dictnosession = dict(zip(new_listofKeys, new_listofDict))

                    cart_dictnosession.update(temp)

            else:
                db["Add_to_cartnosession"] = cart_dictnosession
        except:
            print("Error in retrieving Inventory from addtocart.db")
        db.close()

        for i, j in zip(cart_dictnosession, products_dict):
            for y in cart_dictnosession[i]:
                cart_dictnosession[i][y].set_price(products_dict[j].get_price())

        for i in cart_dictnosession:
            for y in cart_dictnosession[i]:
                cartListnosession[int(i) - 1].append(cart_dictnosession[i][y])

        print(cart_dictnosession)

        if any(len(cart_dictnosession[y]) > 0 for y in cart_dictnosession):
            subtotal = 0
            for total in range(0, len(cartListnosession)):
                for x in cartListnosession[total]:
                    subtotal += x.get_price()

            return render_template("cart.html", cartList=cartListnosession, subtotal=subtotal, trees=trees)

        else:
            return render_template("cart_empty.html", trees=trees)


@app.route('/updateAddCart/<int:id>', methods=['POST'])
def updateAddCart(id):
    db = shelve.open("database/inventory.db", 'w')
    products_dict = db["Products"]
    db.close()

    listofDict = []
    listofKeys = []
    for i in range(1, len(products_dict) + 1):
        listofKeys.append(str(i))
        i = dict()
        listofDict.append(i)

    if "customer_session" in session:
        customer = session["customer_session"]
        db = shelve.open("database/user.db", "w")
        users_dict = db["Users"]
        customer_user = users_dict.get(customer)

        cart_dict = dict(zip(listofKeys, listofDict))

        cartList = []
        for j in range(1, len(products_dict) + 1):
            j = list()
            cartList.append(j)

        db = shelve.open("database/addtocart", "c")
        try:
            if "Add_to_cart" in db:
                temp = db["Add_to_cart"]

                if len(products_dict) == len(temp):
                    cart_dict = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dict = dict(zip(new_listofKeys, new_listofDict))

                    cart_dict.update(temp)

            else:
                db["Add_to_cart"] = cart_dict
        except:
            print("Error in retrieving Inventory from addtocart.db")

        for i in cart_dict:
            for y in cart_dict[i]:
                cartList[int(i) - 1].append(cart_dict[i][y])

        if request.method == "POST":
            addtocart = Addtocart(cartList[id][0].get_name(), cartList[id][0].get_description(),
                                  cartList[id][0].get_price(), 1, cartList[id][0].get_category(),
                                  cartList[id][0].get_discount(), cartList[id][0].get_top())

            for x in cart_dict:
                if id == int(x) - 1:
                    cart_dict[x][addtocart.get_id()] = addtocart

            db["Add_to_cart"] = cart_dict
            db.close()

        return redirect(url_for("cart"))

    else:
        cart_dictnosession = dict(zip(listofKeys, listofDict))

        cartListnosession = []
        for j in range(1, len(products_dict) + 1):
            j = list()
            cartListnosession.append(j)

        db = shelve.open("database/addtocartnosession", "c")

        try:
            if "Add_to_cartnosession" in db:
                temp = db["Add_to_cartnosession"]

                if len(products_dict) == len(temp):
                    cart_dictnosession = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dictnosession = dict(zip(new_listofKeys, new_listofDict))

                    cart_dictnosession.update(temp)
            else:
                db["Add_to_cartnosession"] = cart_dictnosession
        except:
            print("Error in retrieving Inventory from addtocart.db")

        for i in cart_dictnosession:
            for y in cart_dictnosession[i]:
                cartListnosession[int(i) - 1].append(cart_dictnosession[i][y])

        if request.method == "POST":
            addtocartnosession = Addtocart(cartListnosession[id][0].get_name(), cartListnosession[id][0].get_description(),
                                  cartListnosession[id][0].get_price(), 1, cartListnosession[id][0].get_category(),
                                  cartListnosession[id][0].get_discount(), cartListnosession[id][0].get_top())
            for x in cart_dictnosession:
                if id == int(x) - 1:
                    cart_dictnosession[x][addtocartnosession.get_id()] = addtocartnosession

            db["Add_to_cartnosession"] = cart_dictnosession
            db.close()

        return redirect(url_for("cart"))


@app.route('/updateSubCart/<int:id>', methods=['POST'])
def updateSubCart(id):
    db = shelve.open("database/inventory.db", 'w')
    products_dict = db["Products"]
    db.close()

    listofDict = []
    listofKeys = []
    for i in range(1, len(products_dict) + 1):
        listofKeys.append(str(i))
        i = dict()
        listofDict.append(i)

    if "customer_session" in session:
        customer = session["customer_session"]
        db = shelve.open("database/user.db", "w")
        users_dict = db["Users"]
        customer_user = users_dict.get(customer)

        cart_dict = dict(zip(listofKeys, listofDict))
        db = shelve.open("database/addtocart", "c")
        try:
            if "Add_to_cart" in db:
                temp = db["Add_to_cart"]

                if len(products_dict) == len(temp):
                    cart_dict = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dict = dict(zip(new_listofKeys, new_listofDict))

                    cart_dict.update(temp)

            else:
                db["Add_to_cart"] = cart_dict
        except:
            print("Error in retrieving Inventory from addtocart.db")

        if request.method == "POST":
            cart_dict[str(id + 1)].popitem()

        db["Add_to_cart"] = cart_dict
        db.close()

        return redirect(url_for("cart"))

    else:
        cart_dictnosession = dict(zip(listofKeys, listofDict))
        db = shelve.open("database/addtocartnosession", "c")
        try:
            if "Add_to_cartnosession" in db:
                temp = db["Add_to_cartnosession"]

                if len(products_dict) == len(temp):
                    cart_dictnosession = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dictnosession = dict(zip(new_listofKeys, new_listofDict))

                    cart_dictnosession.update(temp)
            else:
                db["Add_to_cartnosession"] = cart_dictnosession
        except:
            print("Error in retrieving Inventory from addtocart.db")

        if request.method == "POST":
           cart_dictnosession[str(id + 1)].popitem()

        db["Add_to_cartnosession"] = cart_dictnosession
        db.close()

        return redirect(url_for("cart"))


@app.route('/deleteCart/<int:id>', methods=['POST'])
def delete_item(id):
    db = shelve.open("database/trees.db", "c")
    trees = db["Trees"]
    db.close()

    db = shelve.open("database/inventory.db", 'w')
    products_dict = db["Products"]
    db.close()

    listofDict = []
    listofKeys = []
    for i in range(1, len(products_dict) + 1):
        listofKeys.append(str(i))
        i = dict()
        listofDict.append(i)

    if "customer_session" in session:
        customer = session["customer_session"]
        db = shelve.open("database/user.db", "w")
        users_dict = db["Users"]
        customer_user = users_dict.get(customer)

        cart_dict = dict(zip(listofKeys, listofDict))
        db = shelve.open("database/addtocart", "c")
        try:
            if "Add_to_cart" in db:
                temp = db["Add_to_cart"]

                if len(products_dict) == len(temp):
                    cart_dict = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dict = dict(zip(new_listofKeys, new_listofDict))

                    cart_dict.update(temp)

            else:
                db["Add_to_cart"] = cart_dict
        except:
            print("Error in retrieving Inventory from addtocart.db")

        cart_dict[str(id + 1)].clear()

        db['Add_to_cart'] = cart_dict
        db.close()

        if any(len(cart_dict[y]) > 0 for y in cart_dict):
            return redirect(url_for("cart"))

        else:
            return render_template("cart_empty.html", trees=trees)

    else:
        cart_dictnosession = dict(zip(listofKeys, listofDict))
        db = shelve.open("database/addtocartnosession", "c")
        try:
            if "Add_to_cartnosession" in db:
                temp = db["Add_to_cartnosession"]

                if len(products_dict) == len(temp):
                    cart_dictnosession = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dictnosession = dict(zip(new_listofKeys, new_listofDict))

                    cart_dictnosession.update(temp)
            else:
                db["Add_to_cartnosession"] = cart_dictnosession
        except:
            print("Error in retrieving Inventory from addtocart.db")

        cart_dictnosession[str(id + 1)].clear()

        db['Add_to_cartnosession'] = cart_dictnosession
        db.close()

        if any(len(cart_dictnosession[y]) > 0 for y in cart_dictnosession):
            return redirect(url_for("cart"))

        else:
            return render_template("cart_empty.html", trees=trees)


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    db = shelve.open("database/trees.db", "c")
    trees = db["Trees"]
    db.close()

    db = shelve.open("database/inventory.db", 'w')
    products_dict = db["Products"]
    db.close()

    listofDict = []
    listofKeys = []
    for i in range(1, len(products_dict) + 1):
        listofKeys.append(str(i))
        i = dict()
        listofDict.append(i)

    if "customer_session" in session:
        customer = session["customer_session"]
        db = shelve.open("database/user.db", "w")
        users_dict = db["Users"]
        customer_user = users_dict.get(customer)

        cart_dict = dict(zip(listofKeys, listofDict))

        cartList = []
        for j in range(1, len(products_dict) + 1):
            j = list()
            cartList.append(j)

        db = shelve.open("database/addtocart", "c")
        try:
            if "Add_to_cart" in db:
                temp = db["Add_to_cart"]

                if len(products_dict) == len(temp):
                    cart_dict = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dict = dict(zip(new_listofKeys, new_listofDict))

                    cart_dict.update(temp)

            else:
                db["Add_to_cart"] = cart_dict
        except:
            print("Error in retrieving Inventory from addtocart.db")

        for i in cart_dict:
            for y in cart_dict[i]:
                cartList[int(i) - 1].append(cart_dict[i][y])

        subtotal = 0
        for total in range(0, len(cartList)):
            for x in cartList[total]:
                subtotal += x.get_price()

        grandtotal = subtotal + 4

        db.close()
        shipping_dict = {}
        create_shipment_form = CreateShipmentForm(request.form)
        if request.method == 'POST' and create_shipment_form.validate():
            db = shelve.open("database/shipping", "c")
            try:
                if "Shipping" in db:
                    shipping_dict = db["Shipping"]
                else:
                    db["Shipping"] = shipping_dict
            except:
                print("Error in retrieving Inventory from shipping.db")
            shipping = ShippingProcess(create_shipment_form.email.data, create_shipment_form.country.data,
                                       create_shipment_form.first_name.data, create_shipment_form.last_name.data,
                                       create_shipment_form.address.data, create_shipment_form.postal_code.data,
                                       create_shipment_form.city.data, create_shipment_form.phone.data)
            shipping_dict[0] = shipping
            db["Shipping"] = shipping_dict

            return redirect(url_for("payment"))

        return render_template("checkout.html", form=create_shipment_form, cartList=cartList, subtotal=subtotal, grandtotal=grandtotal, trees=trees)

    else:
        cart_dictnosession = dict(zip(listofKeys, listofDict))

        cartListnosession = []
        for j in range(1, len(products_dict) + 1):
            j = list()
            cartListnosession.append(j)

        db = shelve.open("database/addtocartnosession", "c")
        try:
            if "Add_to_cartnosession" in db:
                temp = db["Add_to_cartnosession"]

                if len(products_dict) == len(temp):
                    cart_dictnosession = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dictnosession = dict(zip(new_listofKeys, new_listofDict))

                    cart_dictnosession.update(temp)
            else:
                db["Add_to_cartnosession"] = cart_dictnosession
        except:
            print("Error in retrieving Inventory from addtocart.db")

        for i in cart_dictnosession:
            for y in cart_dictnosession[i]:
                cartListnosession[int(i) - 1].append(cart_dictnosession[i][y])

        subtotal = 0
        for total in range(0, len(cartListnosession)):
            for x in cartListnosession[total]:
                subtotal += x.get_price()

        grandtotal = subtotal + 4

        db.close()
        shipping_dict = {}
        create_shipment_form = CreateShipmentForm(request.form)
        if request.method == 'POST' and create_shipment_form.validate():
            db = shelve.open("database/shipping", "c")
            try:
                if "Shipping" in db:
                    shipping_dict = db["Shipping"]
                else:
                    db["Shipping"] = shipping_dict
            except:
                print("Error in retrieving Inventory from shipping.db")
            shipping = ShippingProcess(create_shipment_form.email.data, create_shipment_form.country.data,
                                       create_shipment_form.first_name.data, create_shipment_form.last_name.data,
                                       create_shipment_form.address.data, create_shipment_form.postal_code.data,
                                       create_shipment_form.city.data, create_shipment_form.phone.data)
            shipping_dict[0] = shipping
            db["Shipping"] = shipping_dict

            return redirect(url_for("payment"))

        return render_template("checkout.html", form=create_shipment_form, cartList=cartListnosession, subtotal=subtotal,grandtotal=grandtotal, trees=trees)


@app.route("/checkout/payment", methods=['GET', 'POST'])
def payment():
    db = shelve.open("database/trees.db", "c")
    trees = db["Trees"]
    db.close()

    db = shelve.open("database/inventory.db", 'w')
    products_dict = db["Products"]
    db.close()

    listofDict = []
    listofKeys = []
    for i in range(1, len(products_dict) + 1):
        listofKeys.append(str(i))
        i = dict()
        listofDict.append(i)

    if "customer_session" in session:
        customer = session["customer_session"]
        db = shelve.open("database/user.db", "w")
        users_dict = db["Users"]
        customer_user = users_dict.get(customer)

        cart_dict = dict(zip(listofKeys, listofDict))

        cartList = []
        for j in range(1, len(products_dict) + 1):
            j = list()
            cartList.append(j)

        db = shelve.open("database/addtocart", "c")
        try:
            if "Add_to_cart" in db:
                temp = db["Add_to_cart"]

                if len(products_dict) == len(temp):
                    cart_dict = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dict = dict(zip(new_listofKeys, new_listofDict))

                    cart_dict.update(temp)

            else:
                db["Add_to_cart"] = cart_dict
        except:
            print("Error in retrieving Inventory from addtocart.db")

        for i in cart_dict:
            for y in cart_dict[i]:
                cartList[int(i) - 1].append(cart_dict[i][y])

        subtotal = 0
        for total in range(0, len(cartList)):
            for x in cartList[total]:
                subtotal += x.get_price()

        grandtotal = subtotal + 4

        shipping_dict = {}
        db = shelve.open("database/shipping", "c")
        try:
            if "Shipping" in db:
                shipping_dict = db["Shipping"]
            else:
                db["Shipping"] = shipping_dict
        except:
            print("Error in retrieving Inventory from shipping.db")

        payment_dict = {}
        create_payment_form = CreatePaymentForm(request.form)
        if request.method == 'POST' and create_payment_form.validate():
            db = shelve.open("database/payment", "c")
            try:
                if "payment" in db:
                    payment_dict = db["payment"]
                else:
                    db["payment"] = payment_dict
            except:
                print("Error in retrieving Sales from payment.db")

            payment = PaymentProcess(create_payment_form.card_num.data, create_payment_form.name_card.data,
                                     create_payment_form.expire.data, create_payment_form.ccv.data)
            payment_dict[0] = payment
            db["payment"] = payment_dict
            db.close()

            return redirect(url_for("paymentdone"))

        return render_template("payment.html", form=create_payment_form, cartList=cartList, subtotal=subtotal, grandtotal=grandtotal, ship=shipping_dict, payment=payment_dict, trees=trees)

    else:
        cart_dictnosession = dict(zip(listofKeys, listofDict))

        cartListnosession = []
        for j in range(1, len(products_dict) + 1):
            j = list()
            cartListnosession.append(j)

        db = shelve.open("database/addtocartnosession", "c")
        try:
            if "Add_to_cartnosession" in db:
                temp = db["Add_to_cartnosession"]

                if len(products_dict) == len(temp):
                    cart_dictnosession = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dictnosession = dict(zip(new_listofKeys, new_listofDict))

                    cart_dictnosession.update(temp)
            else:
                db["Add_to_cartnosession"] =  cart_dictnosession
        except:
            print("Error in retrieving Inventory from addtocart.db")

        for i in cart_dictnosession:
            for y in cart_dictnosession[i]:
                cartListnosession[int(i) - 1].append(cart_dictnosession[i][y])

        subtotal = 0
        for total in range(0, len(cartListnosession)):
            for x in cartListnosession[total]:
                subtotal += x.get_price()

        grandtotal = subtotal + 4

        shipping_dict = {}
        db = shelve.open("database/shipping", "c")
        try:
            if "Shipping" in db:
                shipping_dict = db["Shipping"]
            else:
                db["Shipping"] = shipping_dict
        except:
            print("Error in retrieving Inventory from shipping.db")

        payment_dict = {}
        create_payment_form = CreatePaymentForm(request.form)
        if request.method == 'POST' and create_payment_form.validate():
            db = shelve.open("database/payment", "c")
            try:
                if "payment" in db:
                    payment_dict = db["payment"]
                else:
                    db["payment"] = payment_dict
            except:
                print("Error in retrieving Sales from payment.db")

            payment = PaymentProcess(create_payment_form.card_num.data, create_payment_form.name_card.data,
                                     create_payment_form.expire.data, create_payment_form.ccv.data)
            payment_dict[0] = payment
            db["payment"] = payment_dict
            db.close()

            return redirect(url_for("paymentdone"))
        db.close()

        return render_template("payment.html", form=create_payment_form, cartList=cartListnosession, subtotal=subtotal, grandtotal=grandtotal, ship=shipping_dict, payment=payment_dict, trees=trees)


@app.route("/checkout/paymentdone")
def paymentdone():
    db = shelve.open("database/trees.db", "c")
    trees = db["Trees"]
    db.close()

    db = shelve.open("database/inventory.db", 'w')
    products_dict = db["Products"]
    db.close()

    listofDict = []
    listofKeys = []
    for i in range(1, len(products_dict) + 1):
        listofKeys.append(str(i))
        i = dict()
        listofDict.append(i)

    if "customer_session" in session:
        # do not delete this customer I use it for calculating the credit points
        customer = session["customer_session"]
        db1 = shelve.open("database/user.db", "w")
        users_dict = db1["Users"]
        customer_user = users_dict.get(customer)

        cart_dict = dict(zip(listofKeys, listofDict))

        cartList = []
        for j in range(1, len(products_dict) + 1):
            j = list()
            cartList.append(j)

        db = shelve.open("database/addtocart", "c")
        try:
            if "Add_to_cart" in db:
                temp = db["Add_to_cart"]

                if len(products_dict) == len(temp):
                    cart_dict = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dict = dict(zip(new_listofKeys, new_listofDict))

                    cart_dict.update(temp)

            else:
                db["Add_to_cart"] = cart_dict
        except:
            print("Error in retrieving Inventory from addtocart.db")

        for i in cart_dict:
            for y in cart_dict[i]:
                cartList[int(i) - 1].append(cart_dict[i][y])

        subtotal = 0
        for total in range(0, len(cartList)):
            for x in cartList[total]:
                subtotal += x.get_price()

        grandtotal = subtotal + 4

        shipping_dict = {}
        db = shelve.open("database/shipping", "c")
        try:
            if "Shipping" in db:
                shipping_dict = db["Shipping"]
            else:
                db["Shipping"] = shipping_dict
        except:
            print("Error in retrieving Inventory from shipping.db")

        payment_dict = {}
        db = shelve.open("database/payment", "c")
        try:
            if "payment" in db:
                payment_dict = db["payment"]
            else:
                db["payment"] = payment_dict
        except:
            print("Error in retrieving Sales from payment.db")

        sales_dict = {}
        db = shelve.open("database/sales", "c")
        try:
            if "sales" in db:
                sales_dict = db["sales"]
            else:
                db["sales"] = sales_dict
        except:
            print("Error in retrieving Sales from sales.db")

        combinedShippingnPayment = Sales(shipping_dict[0].get_email(), shipping_dict[0].get_country(),
                                         shipping_dict[0].get_firstname(), shipping_dict[0].get_lastname(),
                                         shipping_dict[0].get_address(), shipping_dict[0].get_postal(),
                                         shipping_dict[0].get_city(), shipping_dict[0].get_phone(),
                                         payment_dict[0].get_cardnum(), payment_dict[0].get_namecard(),
                                         payment_dict[0].get_expire(), payment_dict[0].get_ccv(),
                                         cart_dict)

        sales_dict[payment_dict[0].get_paymentid()] = combinedShippingnPayment
        db["sales"] = sales_dict

        # Calculating credit points
        customer_user.calculate_points(grandtotal)
        users_dict[customer] = customer_user
        db1["Users"] = users_dict
        db1.close()

        return render_template("paymentdone.html", subtotal=subtotal, grandtotal=grandtotal, ship=shipping_dict, payment=payment_dict, sales=sales_dict, cartList=cartList, trees=trees)

    else:
        cart_dictnosession = dict(zip(listofKeys, listofDict))

        cartListnosession = []
        for j in range(1, len(products_dict) + 1):
            j = list()
            cartListnosession.append(j)

        db = shelve.open("database/addtocartnosession", "c")
        try:
            if "Add_to_cartnosession" in db:
                temp = db["Add_to_cartnosession"]

                if len(products_dict) == len(temp):
                    cart_dictnosession = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dictnosession = dict(zip(new_listofKeys, new_listofDict))

                    cart_dictnosession.update(temp)
            else:
                db["Add_to_cartnosession"] = cart_dictnosession
        except:
            print("Error in retrieving Inventory from addtocart.db")

        for i in cart_dictnosession:
            for y in cart_dictnosession[i]:
                cartListnosession[int(i) - 1].append(cart_dictnosession[i][y])

        subtotal = 0
        for total in range(0, len(cartListnosession)):
            for x in cartListnosession[total]:
                subtotal += x.get_price()

        grandtotal = subtotal + 4

        shipping_dict = {}
        db = shelve.open("database/shipping", "c")
        try:
            if "Shipping" in db:
                shipping_dict = db["Shipping"]
            else:
                db["Shipping"] = shipping_dict
        except:
            print("Error in retrieving Inventory from shipping.db")

        payment_dict = {}
        db = shelve.open("database/payment", "c")
        try:
            if "payment" in db:
                payment_dict = db["payment"]
            else:
                db["payment"] = payment_dict
        except:
            print("Error in retrieving Sales from payment.db")

        sales_dict = {}
        db = shelve.open("database/sales", "c")
        try:
            if "sales" in db:
                sales_dict = db["sales"]
            else:
                db["sales"] = sales_dict
        except:
            print("Error in retrieving Sales from sales.db")

        combinedShippingnPayment = Sales(shipping_dict[0].get_email(), shipping_dict[0].get_country(),
                                         shipping_dict[0].get_firstname(), shipping_dict[0].get_lastname(),
                                         shipping_dict[0].get_address(), shipping_dict[0].get_postal(),
                                         shipping_dict[0].get_city(), shipping_dict[0].get_phone(),
                                         payment_dict[0].get_cardnum(), payment_dict[0].get_namecard(),
                                         payment_dict[0].get_expire(), payment_dict[0].get_ccv(),
                                         cart_dictnosession)

        sales_dict[payment_dict[0].get_paymentid()] = combinedShippingnPayment
        db["sales"] = sales_dict
        db.close()

        return render_template("paymentdone.html", subtotal=subtotal, grandtotal=grandtotal, ship=shipping_dict, payment=payment_dict, sales=sales_dict, cartList=cartListnosession, trees=trees)


@app.route("/checkout/paymentdone/clear", methods=['POST'])
def done_clear():
    db = shelve.open("database/inventory.db", 'w')
    products_dict = db["Products"]
    db.close()

    listofDict = []
    listofKeys = []
    for i in range(1, len(products_dict) + 1):
        listofKeys.append(str(i))
        i = dict()
        listofDict.append(i)

    if "customer_session" in session:
        customer = session["customer_session"]
        db = shelve.open("database/user.db", "w")
        users_dict = db["Users"]
        customer_user = users_dict.get(customer)

        cart_dict = dict(zip(listofKeys, listofDict))

        db1 = shelve.open("database/addtocart", "c")
        try:
            if "Add_to_cart" in db:
                temp = db["Add_to_cart"]

                if len(products_dict) == len(temp):
                    cart_dict = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dict = dict(zip(new_listofKeys, new_listofDict))

                    cart_dict.update(temp)

            else:
                db["Add_to_cart"] = cart_dict
        except:
            print("Error in retrieving Inventory from addtocart.db")

        shipping_dict = {}
        db2 = shelve.open("database/shipping", "c")
        try:
            if "Shipping" in db2:
                shipping_dict = db2["Shipping"]
            else:
                db2["Shipping"] = shipping_dict
        except:
            print("Error in retrieving Inventory from shipping.db")

        payment_dict = {}
        db3 = shelve.open("database/payment", "c")
        try:
            if "payment" in db3:
                payment_dict = db3["payment"]
            else:
                db3["payment"] = payment_dict
        except:
            print("Error in retrieving Sales from payment.db")

        nlistofDict = []
        nlistofKeys = []
        for i in range(1, len(products_dict) + 1):
            nlistofKeys.append(str(i))
            i = dict()
            nlistofDict.append(i)
        cart_dict = dict(zip(nlistofKeys, nlistofDict))

        db1['Add_to_cart'] = cart_dict
        shipping_dict[0] = None
        db2["Shipping"] = shipping_dict
        payment_dict[0] = None
        db3["payment"] = payment_dict

        return redirect(url_for("home"))

    else:
        cart_dictnosession = dict(zip(listofKeys, listofDict))

        db1 = shelve.open("database/addtocartnosession", "c")
        try:
            if "Add_to_cartnosession" in db1:
                temp = db["Add_to_cartnosession"]

                if len(products_dict) == len(temp):
                    cart_dictnosession = temp

                elif len(products_dict) > len(temp):
                    new_listofDict = []
                    new_listofKeys = []

                    for i in range(1, len(products_dict) + 1):
                        new_listofKeys.append(str(i))
                        i = dict()
                        new_listofDict.append(i)
                    cart_dictnosession = dict(zip(new_listofKeys, new_listofDict))

                    cart_dictnosession.update(temp)
            else:
                db1["Add_to_cartnosession"] = cart_dictnosession
        except:
            print("Error in retrieving Inventory from addtocart.db")

        shipping_dict = {}
        db2 = shelve.open("database/shipping", "c")
        try:
            if "Shipping" in db2:
                shipping_dict = db2["Shipping"]
            else:
                db2["Shipping"] = shipping_dict
        except:
            print("Error in retrieving Inventory from shipping.db")

        payment_dict = {}
        db3 = shelve.open("database/payment", "c")
        try:
            if "payment" in db3:
                payment_dict = db3["payment"]
            else:
                db3["payment"] = payment_dict
        except:
            print("Error in retrieving Sales from payment.db")

        nlistofDict = []
        nlistofKeys = []
        for i in range(1, len(products_dict) + 1):
            nlistofKeys.append(str(i))
            i = dict()
            nlistofDict.append(i)
        cart_dict = dict(zip(nlistofKeys, nlistofDict))

        db1['Add_to_cartnosession'] = cart_dict
        shipping_dict[0] = None
        db2["Shipping"] = shipping_dict
        payment_dict[0] = None
        db3["payment"] = payment_dict

        return redirect(url_for("home"))


# main shop
@app.route("/mainshop", methods=['GET', 'POST'])
def mainshop():
    global temp_product_id
    db = shelve.open("database/trees.db", "c")
    trees = db["Trees"]
    db.close()

    db = shelve.open("database/inventory.db", 'w')
    products_dict = db["Products"]
    db.close()

    productview = CreateProductView(request.form)
    if request.method == "POST":
        print(productview.product_id.data)
        temp_product_id = productview.product_id.data
        return redirect(url_for("bagbase"))

    return render_template("mainshop.html", products=products_dict, form=productview, trees=trees)


@app.route("/bagbase", methods=['GET', 'POST'])
def bagbase():
    db = shelve.open("database/trees.db", "c")
    trees = db["Trees"]
    db.close()

    db = shelve.open("database/inventory.db", 'w')
    products_dict = db["Products"]
    productList = []
    for x in products_dict:
        productList.append(products_dict[x])
    db.close()

    print(productList)

    listofDict = []
    listofKeys = []
    for i in range(1, len(products_dict) + 1):
        listofKeys.append(str(i))
        i = dict()
        listofDict.append(i)

    if "customer_session" in session:
        customer = session["customer_session"]
        db = shelve.open("database/user.db", "w")
        users_dict = db["Users"]
        customer_user = users_dict.get(customer)

        addtocart_dict = dict(zip(listofKeys, listofDict))

        x = temp_product_id
        addtocartform = CreateAddCartForm(request.form)
        if request.method == "POST":

            db = shelve.open("database/addtocart", "c")
            try:
                if "Add_to_cart" in db:
                    temp = db["Add_to_cart"]

                    if len(products_dict) == len(temp):
                        addtocart_dict = temp

                    elif len(products_dict) > len(temp):
                        new_listofDict = []
                        new_listofKeys = []

                        for i in range(1, len(products_dict) + 1):
                            new_listofKeys.append(str(i))
                            i = dict()
                            new_listofDict.append(i)
                        addtocart_dict = dict(zip(new_listofKeys, new_listofDict))

                        addtocart_dict.update(temp)

                else:
                    db["Add_to_cart"] = addtocart_dict
            except:
                print("Error in retrieving Inventory from addtocart.db")

            addtocart = Addtocart(addtocartform.name.data, addtocartform.description.data,
                                  int(addtocartform.price.data), int(addtocartform.quantity.data),
                                  addtocartform.category.data, int(addtocartform.discount.data),
                                  int(addtocartform.top.data))

            for x, j in zip(productList, range(1, len(productList)+1)):
                if addtocart.get_name() == x.get_name():
                    addtocart_dict[str(j)][addtocart.get_id()] = addtocart

            db["Add_to_cart"] = addtocart_dict
            db.close()
            return redirect(url_for("cart"))

        return render_template("bagbase.html", form=addtocartform, products=products_dict, x=x, trees=trees)

    else:
        addtocartnosession_dict = dict(zip(listofKeys, listofDict))

        x = temp_product_id
        addtocartform = CreateAddCartForm(request.form)
        if request.method == "POST":
            db = shelve.open("database/addtocartnosession", "c")
            try:
                if "Add_to_cartnosession" in db:
                    temp = db["Add_to_cartnosession"]

                    if len(products_dict) == len(temp):
                        addtocartnosession_dict = temp

                    elif len(products_dict) > len(temp):
                        new_listofDict = []
                        new_listofKeys = []

                        for i in range(1, len(products_dict) + 1):
                            new_listofKeys.append(str(i))
                            i = dict()
                            new_listofDict.append(i)
                        addtocartnosession_dict = dict(zip(new_listofKeys, new_listofDict))

                        addtocartnosession_dict.update(temp)

                else:
                    db["Add_to_cartnosession"] = addtocartnosession_dict
            except:
                print("Error in retrieving Inventory from addtocart.db")

            addtocart = Addtocart(addtocartform.name.data, addtocartform.description.data,
                                  int(addtocartform.price.data), int(addtocartform.quantity.data),
                                  addtocartform.category.data, int(addtocartform.discount.data),
                                  int(addtocartform.top.data))
            addtocart.set_picture(addtocartform.pic.data)

            for x, j in zip(productList, range(1, len(productList) + 1)):
                if addtocart.get_name() == x.get_name():
                    addtocartnosession_dict[str(j)][addtocart.get_id()] = addtocart

            db["Add_to_cartnosession"] = addtocartnosession_dict
            db.close()
            return redirect(url_for("cart"))

        return render_template("bagbase.html", form=addtocartform, products=products_dict, x=x, trees=trees)


@app.route("/auction", methods=['GET', 'POST'])
def auction():
    bid_dict = {}
    db = shelve.open('database/UserBid.db', 'c')

    try:
        bid_dict = db['UserBid']
        # for x in bid_dict:
        #     key = bid_dict.get(x)
        #     print(key)
    except:
        print("Error in retrieving userbid.db.")

    db.close()

    bid_list = []
    for key in bid_dict:
        # bid_dict.pop()
        user = bid_dict.get(key)
        bid_list.append(user)

    auction_dict = {}
    db = shelve.open('database/auction.db', 'c')
    auction_dict = db["Auction"]
    db.close()

    today = date.today().strftime('%Y-%m-%d')
    ongoing = ""
    expire_date = ""

    pre_expire = date.today() + timedelta(days=10)

    for keys, values in auction_dict.items():
        start = date.strftime(values.get_start_date(), '%Y-%m-%d')
        end = date.strftime(values.get_end_date(), '%Y-%m-%d')

        if start == today or today > start or start <= today and end <= today:
            ongoing = values

        end_date = values.get_end_date()
        if pre_expire > end_date:
            expire_date = abs((end_date - pre_expire).days)
        else:
            expire_date = 10


    db = shelve.open("database/trees.db", "c")
    trees = db["Trees"]
    db.close()

    return render_template('auction.html', auction_dict=auction_dict, bid_list=bid_list, ongoing=ongoing, trees=trees, expire_date=expire_date)


@app.route("/auctionForm", methods=['GET', 'POST'])
def auctionForm():
    db = shelve.open("database/trees.db", "c")
    trees = db["Trees"]
    db.close()

    create_bid_form = CreateBidForm(request.form)
    print("JUST PRINT SOMETHING")
    if request.method == 'POST' and create_bid_form.validate():
        bid_dict = {}
        db = shelve.open('database/userbid.db', 'c')

        try:
            bid_dict = db['UserBid']
        except:
            print("Error in retrieving userbid.db.")

        userbidID = UserBid(create_bid_form.bid_amount.data, create_bid_form.bid_user.data)
        print(userbidID)
        bid_dict[userbidID.get_bidId()] = userbidID
        db['UserBid'] = bid_dict

        # for x in bid_dict:
        #     print(x)

        db.close()

        return redirect(url_for("auction"))
    return render_template('auctionForm.html', form=create_bid_form, trees=trees)


@app.route("/deleteBid/<id>", methods=["POST"])
def delete_bid(id):
    db = shelve.open('database/UserBid.db', 'c')
    bid_dict = db['UserBid']

    bid_dict.pop(id)

    db['UserBid'] = bid_dict
    db.close()

    return redirect(url_for('auction'))


@app.route("/updateBid/<id>/", methods=['GET', 'POST'])
def update_bid(id):
    update_bid_form = CreateBidForm(request.form)
    if request.method == 'POST' and update_bid_form.validate():
        bid_dict = {}
        db = shelve.open('database/UserBid.db', 'w')
        bid_dict = db['UserBid']

        bid = bid_dict.get(id)
        bid.set_bidAmount(update_bid_form.bid_amount.data)
        bid.set_bidUser(update_bid_form.bid_user.data)

        db['UserBid'] = bid_dict
        db.close()
        for x in bid_dict:
            print(x)
            val = bid_dict.get(x)
            print(val)

        return redirect(url_for('auction'))
    else:
        bid_dict = {}
        db = shelve.open('database/UserBid.db', 'r')
        bid_dict = db['UserBid']
        db.close()
        customer = bid_dict.get(id)
        update_bid_form.bid_amount.data = customer.get_bidAmount()
        update_bid_form.bid_user.data = customer.get_bidUser()

        return render_template('updateBid.html', form=update_bid_form)


randomOTP = random.randint(111111, 999999)


@app.route("/forgetPassword", methods=["POST", "GET"])
def forget_password():
    create_forget_form = CreateForgetPassForm(request.form)

    # with open("templates/forgetPassword.html") as file:
    #     soup = BeautifulSoup(file, "html.parser")
    #
    # print(soup.find())
    # print(soup.prettify())

    db = shelve.open("database/user.db", "r")
    users_dict = db['Users']
    db.close()

    if request.method == 'POST' and create_forget_form.validate():
        userId = ""
        for userKey, userValue in users_dict.items():
            if create_forget_form.email.data == userValue.get_email():
                userId = userKey
                break

        if create_forget_form.newPass.data == create_forget_form.confirmPass.data and create_forget_form.otp.data == str(
                randomOTP):
            db = shelve.open("database/user.db", "w")
            users_dict = db['Users']

            users_dict.get(userId).set_password(create_forget_form.newPass.data)

            db['Users'] = users_dict
            db.close()

            return redirect(url_for("log_in"))

    db = shelve.open("database/trees.db", "c")
    trees = db["Trees"]
    db.close()

    return render_template("forgetPassword.html", form=create_forget_form, otpNum=randomOTP, trees=trees)


@app.route("/game")
def play_game():
    if "customer_session" in session:
        with shelve.open("database/game.db", "c") as db:
            try:
                leaderboard_dict = db["Leaderboard"]

                for key, values in leaderboard_dict.items():
                    if key == session["customer_session"]:

                        if values.get_total_points() == 0:
                            leaderboard_points = ""
                        else:
                            leaderboard_points = values.get_total_points()
                            break

                    else:
                        leaderboard_points = ""
            except:
                leaderboard_points = ""

            with shelve.open("database/game.db", "c") as db:

                try:
                    points_list = db['Points']
                except:
                    print("Error in retrieving Points.")

                if leaderboard_points == "":
                    stayWhile = True

                    while stayWhile:
                        count = 0
                        points_list = generate_points()

                        for j in points_list:
                            try:
                                count += 1
                                if int(list(j.values())[0]) and count == len(points_list):
                                    print("change false")
                                    stayWhile = False
                            except:
                                break
                else:
                    points_list = generate_points()

                db['Points'] = points_list

        with shelve.open('database/user.db', 'r') as db:
            try:
                users_details_dict = db['Users']
            except:
                print("Error in retrieving user.db.")

            user_details = users_details_dict.get(session["customer_session"])
            user_credit_points = user_details.get_points()

        db = shelve.open("database/trees.db", "c")
        trees = db["Trees"]

        return render_template("game.html", points_list=points_list, points=leaderboard_points,
                               credit_points=user_credit_points, trees=trees)
    else:
        return redirect(url_for("log_in"))


@app.route("/game/<int:key>", methods=["POST"])
def save_point(key):
    points = ""
    value = ''
    multiply = 0
    with shelve.open("database/game.db", "r") as db:
        points_list = db['Points']

        for i in points_list:
            if key == list(i.keys())[0]:
                value = i.get(key)
                break

        try:
            points = int(value)
        except:
            multiplier_dict = {"x5": 5, "x4": 4, "x3": 3, "x2": 2}

            multiply = multiplier_dict.get(value)

        with shelve.open("database/game.db", "c") as db2:
            game_user_dict = {}
            try:
                game_user_dict = db2["Leaderboard"]
            except:
                print("Error in retrieving game.db.")

            today = date.today().strftime('%Y-%m-%d')
            next_day = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

            if game_user_dict.get(session["customer_session"]):
                player_status = game_user_dict.get(session["customer_session"])
            else:
                player_status = PlayerStatus(session["customer_session"], today, next_day)

            try:
                if int(points) > 0:
                    player_status.calculate_total_points(points)
            except:
                player_status.calculate_total_points(0, multiply)

            # player_status.set_total_zero()

            game_user_dict[player_status.get_customer_id()] = player_status

            db2["Leaderboard"] = game_user_dict

            print(player_status.get_total_points())

            with shelve.open("database/user.db", "w") as db3:
                users_dict = {}
                try:
                    users_dict = db3['Users']
                except:
                    print("Error in retrieving user.db.")

                points = users_dict.get(session["customer_session"]).get_points()

                users_dict.get(session["customer_session"]).set_points(points-10)

                db3['Users'] = users_dict

    return redirect(url_for("checkout"))


@app.route("/game/continue/<int:key>", methods=["POST"])
def save_point(key):
    points = ""
    value = ''
    multiply = 0
    with shelve.open("database/game.db", "r") as db:
        points_list = db['Points']

        for i in points_list:
            if key == list(i.keys())[0]:
                value = i.get(key)
                break

        try:
            points = int(value)
        except:
            multiplier_dict = {"x5": 5, "x4": 4, "x3": 3, "x2": 2}

            multiply = multiplier_dict.get(value)

        with shelve.open("database/game.db", "c") as db2:
            game_user_dict = {}
            try:
                game_user_dict = db2["Leaderboard"]
            except:
                print("Error in retrieving game.db.")

            today = date.today().strftime('%Y-%m-%d')
            next_day = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

            if game_user_dict.get(session["customer_session"]):
                player_status = game_user_dict.get(session["customer_session"])
            else:
                player_status = PlayerStatus(session["customer_session"], today, next_day)

            try:
                if int(points) > 0:
                    player_status.calculate_total_points(points)
            except:
                player_status.calculate_total_points(0, multiply)

            # player_status.set_total_zero()

            game_user_dict[player_status.get_customer_id()] = player_status

            db2["Leaderboard"] = game_user_dict

            print(player_status.get_total_points())

            with shelve.open("database/user.db", "w") as db3:
                users_dict = {}
                try:
                    users_dict = db3['Users']
                except:
                    print("Error in retrieving user.db.")

                points = users_dict.get(session["customer_session"]).get_points()

                users_dict.get(session["customer_session"]).set_points(points - 10)

                db3['Users'] = users_dict

    return redirect(url_for("play_game"))


@app.route("/leaderboard")
def leaderboard():
    if "customer_session" in session:
        username_list = []
        users_dict = {}
        with shelve.open("database/game.db", "r") as db:
            try:
                game_user_dict = db["Leaderboard"]
            except:
                print("Error in retrieving game.db.")

            def sort_by_points(player):
                return player.get_total_points()

            sorted_list = sorted(game_user_dict.values(), key=sort_by_points, reverse=True)
            print(sorted_list)

            for p in sorted_list:
                print(p.get_total_points())

        with shelve.open("database/user.db", "r") as db2:
            try:
                users_dict = db2['Users']
            except:
                print("Error in retrieving user.db.")

            try:
                for player in sorted_list:
                    # print(users_dict.get(player.get_customer_id()).get_first_name(), users_dict.get(player.get_customer_id()).get_last_name())
                    username_list.append(users_dict.get(player.get_customer_id()).get_last_name())

                session_user = users_dict.get(session["customer_session"])
                print(session_user.get_last_name())

            except:
                sorted_list = []
                username_list = []

        db = shelve.open("database/trees.db", "c")
        trees = db["Trees"]

        return render_template("leaderboard.html", sorted_list=sorted_list, username_list=username_list, trees=trees)
    else:
        return redirect(url_for("log_in"))


# Admin Side
@app.route("/admin")
def admin():
    db = shelve.open("database/inventory.db", 'r')
    products_dict = db["Products"]
    db.close()

    time_now = datetime.now()

    sales_dict = {}
    db = shelve.open("database/sales", "c")
    try:
        if "sales" in db:
            sales_dict = db["sales"]
        else:
            db["sales"] = sales_dict
    except:
        print("Error in retrieving Sales from sales.db")
    db.close()

    salesList = []
    for x in sales_dict:
        salesList.append(sales_dict[x])

    customer_total = 0
    customer_totalList = []

    for i in range(0, len(salesList)):
        for j in salesList[i].get_cart():
            for y in salesList[i].get_cart()[j]:
                customer_total += salesList[i].get_cart()[j][y].get_price()

        customer_totalList.append(customer_total)
        customer_total = 0

    subtotal = 0
    for total in customer_totalList:
        subtotal += total

    db = shelve.open("database/trees.db", "c")
    db["Trees"] = subtotal / 5
    db.close()

    try:
        db = shelve.open('database/auction.db', 'r')
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

            if (start == today or today > start or start <= today) and end <= today:
                if today > end:
                    ongoing = ""
                else:
                    ongoing = values
            elif start > today and end > today:
                upcoming.append(values)

    auction_on = len(ongoing)

    from itertools import accumulate
    cumulative_total = list(accumulate(customer_totalList))
    forgraphvalue = cumulative_total
    for i in range(0, len(salesList)):
        for j in salesList[i].get_cart()["1"]:
            customer_total += salesList[i].get_cart()["1"][j].get_price()

        for j in salesList[i].get_cart()["2"]:
            customer_total += salesList[i].get_cart()["2"][j].get_price()

        forgraphvalue.append(customer_total)

    forgraphlabel = []
    for k in range(1, len(salesList) + 1):
        forgraphlabel.append(k)

    labels = forgraphlabel
    values = forgraphvalue
    orders_quantity = len(salesList)

    return render_template("adminDashboard.html", top4=products_dict, labels=labels, values=values, subtotal=subtotal, date=time_now, auction_on=auction_on, salesList=salesList, customer_totalList=customer_totalList, orders_quantity=orders_quantity)


@app.route("/adminAuction")
def admin_auction():
    try:
        db = shelve.open('database/auction.db', 'r')
        auction_dict = db["Auction"]
        db.close()
    except:
        auction_dict = {}

    today = date.today().strftime('%Y-%m-%d')
    upcoming = []
    ongoing = ""
    print(auction_dict)
    if auction_dict != {}:

        for keys, values in auction_dict.items():
            start = date.strftime(values.get_start_date(), '%Y-%m-%d')
            end = date.strftime(values.get_end_date(), '%Y-%m-%d')

            if (start == today or today > start or start <= today) and end <= today:
                if today > end:
                    print("empty")
                    ongoing = ""
                else:
                    print("ongoing")
                    ongoing = values
            elif start > today and end > today:
                print("upcoming")
                upcoming.append(values)
    return render_template("adminAuction.html", ongoing=ongoing, upcoming=upcoming)


@app.route("/createAuction", methods=['GET', 'POST'])
def create_auction():
    create_auction_form = CreateAuctionForm(request.form)

    if request.method == "POST" and create_auction_form.validate():
        create_auction_dict = {}
        db = shelve.open("database/auction.db", "c")

        try:
            if "Auction" in db:
                create_auction_dict = db["Auction"]
            else:
                db["Auction"] = create_auction_dict
        except:
            print("Error in retrieving Inventory from auction.db")

        auction_class = Auction(create_auction_form.product_name.data, create_auction_form.description.data,
                                create_auction_form.base_amount.data, create_auction_form.minimum_amount.data,
                                create_auction_form.start_date.data, create_auction_form.end_date.data)

        create_auction_dict[auction_class.get_auction_id()] = auction_class
        db["Auction"] = create_auction_dict

        db.close()

        return redirect(url_for("admin_auction"))

    return render_template("createAuction.html", form=create_auction_form)


@app.route("/updateAuction/<id>/", methods=['GET', 'POST'])
def update_auction(id):
    update_auction_form = CreateAuctionForm(request.form)
    if request.method == 'POST' and update_auction_form.validate():
        db = shelve.open("database/auction.db", 'w')
        auction_dict = db["Auction"]

        auction_dict.get(id).set_name(update_auction_form.product_name.data)
        auction_dict.get(id).set_description(update_auction_form.description.data)
        auction_dict.get(id).set_price(update_auction_form.base_amount.data)
        auction_dict.get(id).set_minimum_amount(update_auction_form.minimum_amount.data)
        auction_dict.get(id).set_start_date(update_auction_form.start_date.data)
        auction_dict.get(id).set_end_date(update_auction_form.end_date.data)

        db["Auction"] = auction_dict
        db.close()

        return redirect(url_for("admin_auction"))
    else:
        db = shelve.open("database/auction.db", 'r')
        auction_dict = db["Auction"]
        db.close()

        update_auction_form.product_name.data = auction_dict.get(id).get_name()
        update_auction_form.base_amount.data = auction_dict.get(id).get_price()
        update_auction_form.minimum_amount.data = auction_dict.get(id).get_minimum_amount()
        update_auction_form.start_date.data = auction_dict.get(id).get_start_date()
        update_auction_form.end_date.data = auction_dict.get(id).get_end_date()
        update_auction_form.description.data = auction_dict.get(id).get_description()

        return render_template("updateAuction.html", form=update_auction_form)


@app.route('/deleteAuction/<id>', methods=["POST"])
def delete_auction(id):
    db = shelve.open("database/auction.db", "w")
    auction_dict = db["Auction"]

    auction_dict.pop(id)

    db["Auction"] = auction_dict
    db.close()

    return redirect(url_for("admin_auction"))


@app.route("/adminOrders")
def admin_orders():
    sales_dict_keys = []
    keys_list = []
    values_list = []
    with shelve.open('database/sales', 'r') as db:
        print(db["sales"])
        try:
            if "sales" in db:
                sales_dict = db["sales"]
        except:
            print("Error in retrieving Sales from sales.db")

        for keys, values in sales_dict.items():
            print(values)

        # sales_dict.pop('e4116ad4-d0d3-4035-a358-9993d9241578')
        # db['sales'] = sales_dict
        # print(db["sales"])

        sales_dict_keys = list(sales_dict.keys())
        print(sales_dict_keys)
        if (len(sales_dict_keys) % 2) == 1:
            sales_dict_keys.append("")

        for sales in sales_dict_keys:

            if sales != "":
                sales_cart = sales_dict[sales].get_cart()
                sales_cart_keys_list = list(sales_cart.keys())

                sales_cart_values_list = list(sales_cart.values())
                count = 0
                print(sales_cart_values_list)
                for num in range(0, len(sales_cart_values_list)-1):
                    print(num)

                    if sales_cart_values_list[num] == {}:
                        sales_cart_values_list.pop(num)
                        sales_cart_keys_list.pop(num)

                values_list.append(sales_cart_values_list)

                # print(sales_cart_keys_list)
                print(sales_cart_values_list)
                # print(values_list)

    # sales_dict = sales_dict, sales_dict_keys = sales_dict_keys
    return render_template("adminOrders.html",sales_dict=sales_dict, sales_dict_keys=sales_dict_keys,
                           sales_cart_keys_list=sales_cart_keys_list, values_list=values_list)


@app.route("/adminOrders/pending")
def pending_order():
    return render_template("adminOrders.html")


@app.route("/adminOrders/accepted")
def accept_order():
    with shelve.open('database/sales', 'r') as db:
        print(db["sales"])
        try:
            if "sales" in db:
                sales_dict = db["sales"]
        except:
            print("Error in retrieving Sales from sales.db")


    return render_template("adminOrders.html")


@app.route("/adminCustomerManagement")
def admin_customer_management():
    db = shelve.open('database/user.db', 'r')
    users_dict = db['Users']
    db.close()
    customer_list = []
    for user in users_dict:
        if isinstance(users_dict[user], Customer):
            customer = users_dict[user]
            customer_list.append(customer)

    return render_template("adminCustomerManagement.html", count=len(customer_list), customer_list=customer_list)


@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    users_dict = {}
    db = shelve.open('database/user.db', 'w')
    users_dict = db['Users']
    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()
    return redirect(url_for('admin_customer_management'))


@app.route("/adminAdminManagement")
def admin_admin_management():
    db = shelve.open('database/user.db', 'r')
    users_dict = db['Users']
    db.close()
    admin_list = []
    for user in users_dict:
        if isinstance(users_dict[user], Admin):
            admin = users_dict[user]
            admin_list.append(admin)
    return render_template("adminAdminManagement.html", count=len(admin_list), admin_list=admin_list)


@app.route('/deleteAdmin/<int:id>', methods=['POST'])
def delete_admin(id):
    users_dict = {}
    db = shelve.open('database/user.db', 'w')
    users_dict = db['Users']
    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()
    return redirect(url_for('admin_admin_management'))


@app.route("/adminAccountCreation", methods=['GET', 'POST'])
def admin_creation():
    code = 0
    create_admin_form = CreateAdminForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and create_admin_form.validate():
        db = shelve.open('database/user.db', 'r')
        user_dict = db['Users']
        for user in user_dict:
            if create_admin_form.email.data.upper() == user_dict[user].get_email().upper():
                code = 1
                break
        if create_admin_form.register_password.data == create_admin_form.confirm_password.data and code == 0:
            admin_dict = {}
            db = shelve.open('database/user.db', 'c')
            try:
                admin_dict = db['Users']
            except:
                print("Error in retrieving Users from user.db")

            new_admin = Admin(create_admin_form.first_name.data, create_admin_form.last_name.data,
                              create_admin_form.email.data, create_admin_form.register_password.data,
                              create_admin_form.employee_id.data)
            admin_dict[new_admin.get_admin_id()] = new_admin
            if "profile_pic" in request.files:
                pic = create_admin_form.profile_pic.data
                fn = pic.filename.split(".")
                ext = fn[len(fn)-1]
                if ext == "jpg" or ext == "png":
                    print("hi")
                    pic_name = str(new_admin.get_admin_id()) + "." + str(ext)
                    try:
                        new_admin.set_picture(pic_name)
                        pic.save(os.path.join("static/images/profile_pics/", pic_name))
                        print("saved")
                    except:
                        print("upload failed")
            if "profile_picture" not in request.files:
                print("not saved")
            print(new_admin.get_picture())
            db['Users'] = admin_dict
            db.close()
            return redirect(url_for('admin_admin_management'))
        else:
            print("Password does not match!")
    return render_template("adminAdminCreation.html", form=create_admin_form, code=code)


@app.route("/adminAdminUpdate/<int:id>/", methods=["GET", "POST"])
def update_admin(id):
    update_admin_form = UpdateAdminForm(CombinedMultiDict((request.files, request.form)))
    error = ""
    code = 0
    db = shelve.open('database/user.db', 'w')
    users_dict = db['Users']
    admin = users_dict.get(id)
    if request.method == 'POST' and update_admin_form.validate():
        users_dict = {}

        # Make uuids for customers and admins the same method to retrieve
        for user in users_dict:
            if update_admin_form.email.data.upper() == users_dict[user].get_email().upper() and id != users_dict[
                user].get_admin_id():
                code = 1
                break
        hashed_password = hl.pbkdf2_hmac('sha256', str(update_admin_form.current_password.data).encode(), b'salt',
                                         100000).hex()
        if "profile_pic" in request.files:
                pic = update_admin_form.profile_pic.data
                fn = pic.filename.split(".")
                ext = fn[len(fn)-1]
                if ext == "jpg" or ext == "png":
                    pic_name = str(admin.get_admin_id()) + "." + str(ext)
                    try:
                        admin.set_picture(pic_name)
                        pic.save(os.path.join("static/images/profile_pics/", pic_name))
                        print("saved")
                    except:
                        print("upload failed")
        if "profile_picture" not in request.files:
            print("not saved")
        if update_admin_form.current_password.data == "" and code == 0:
            admin.set_first_name(update_admin_form.first_name.data)
            admin.set_last_name(update_admin_form.last_name.data)
            admin.set_email(update_admin_form.email.data)
            admin.set_employee_id(update_admin_form.employee_id.data)
            if update_admin_form.profile_pic.data:
                print("Saved?")
                picture_file = save_picture(update_admin_form.profile_pic.data, admin.get_admin_id())
                print("Def saved")
            db['Users'] = users_dict
            db.close()
            return redirect(url_for('admin_admin_management'))
        elif update_admin_form.current_password.data != "" and code == 0:
            if hashed_password == admin.get_password():
                admin.set_first_name(update_admin_form.first_name.data)
                admin.set_last_name(update_admin_form.last_name.data)
                admin.set_email(update_admin_form.email.data)
                admin.set_employee_id(update_admin_form.employee_id.data)
                admin.set_password(update_admin_form.new_password.data)
                if update_admin_form.profile_pic.data:
                    print("Saved?")
                    picture_file = save_picture(update_admin_form.profile_pic.data, admin.get_admin_id())
                    print("Def saved")
                db['Users'] = users_dict
                db.close()
                return redirect(url_for('admin_admin_management'))
            elif hashed_password != admin.get_password():
                error = "Wrong password entered"

    else:
        users_dict = {}
        db = shelve.open('database/user.db', 'r')
        users_dict = db['Users']
        db.close()

        admin = users_dict.get(id)
        update_admin_form.first_name.data = admin.get_first_name()
        update_admin_form.last_name.data = admin.get_last_name()
        update_admin_form.email.data = admin.get_email()
        update_admin_form.employee_id.data = admin.get_employee_id()
    return render_template("adminAdminUpdate.html", form=update_admin_form, error=error, code=code, admin=admin)


@app.route("/adminAccount", methods=["GET", "POST"])
def admin_logged_in():
    update_admin_form = UpdateAdminForm(CombinedMultiDict((request.files, request.form)))
    error = ""
    code = 0
    picture_status = 0

    if "admin_session" in session:
        admin = session["admin_session"]
        db = shelve.open('database/user.db', 'w')
        users_dict = db['Users']
        admin_user = users_dict.get(admin)
        path = "../static/images/profile_pics/"+str(admin_user.get_picture())
        print(path)
        if admin_user.get_picture() is not None:
            picture_status = 1
        if request.method == 'POST' and update_admin_form.validate():
            # Make uuids for customers and admins the same method to retrieve
            for user in users_dict:
                if isinstance(users_dict[user], Customer):
                    if update_admin_form.email.data.upper() == users_dict[user].get_email().upper() and admin != \
                            users_dict[user].get_customer_id():
                        code = 1
                        break
                if isinstance(users_dict[user], Admin):
                    if update_admin_form.email.data.upper() == users_dict[user].get_email().upper() and admin != \
                            users_dict[user].get_admin_id():
                        code = 1
                        break
            hashed_password = hl.pbkdf2_hmac('sha256', str(update_admin_form.current_password.data).encode(), b'salt',
                                             100000).hex()
            if "profile_pic" in request.files:
                pic = update_admin_form.profile_pic.data
                fn = pic.filename.split(".")
                ext = fn[len(fn)-1]
                if ext == "jpg" or ext == "png":
                    pic_name = str(admin_user.get_admin_id()) + "." + str(ext)
                    try:
                        admin_user.set_picture(pic_name)
                        pic.save(os.path.join("static/images/profile_pics/", pic_name))
                        print("saved")
                    except:
                        print("upload failed")
            if "profile_picture" not in request.files:
                print("not saved")
            if update_admin_form.current_password.data == "" and code == 0:
                admin_user.set_first_name(update_admin_form.first_name.data)
                admin_user.set_last_name(update_admin_form.last_name.data)
                admin_user.set_email(update_admin_form.email.data)
                admin_user.set_employee_id(update_admin_form.employee_id.data)
                db['Users'] = users_dict
                db.close()
                return redirect(url_for('admin_admin_management'))
            elif update_admin_form.current_password.data != "" and code == 0:
                if hashed_password == admin_user.get_password():
                    admin_user.set_first_name(update_admin_form.first_name.data)
                    admin_user.set_last_name(update_admin_form.last_name.data)
                    admin_user.set_email(update_admin_form.email.data)
                    admin_user.set_employee_id(update_admin_form.employee_id.data)
                    admin_user.set_password(update_admin_form.new_password.data)
                    db['Users'] = users_dict
                    db.close()
                    return redirect(url_for('admin_admin_management'))
                elif hashed_password != admin.get_password():
                    error = "Wrong password entered"

        else:
            update_admin_form.first_name.data = admin_user.get_first_name()
            update_admin_form.last_name.data = admin_user.get_last_name()
            update_admin_form.email.data = admin_user.get_email()
            update_admin_form.employee_id.data = admin_user.get_employee_id()
        return render_template("adminAccount.html", form=update_admin_form, error=error, code=code, picture_status=picture_status, path=path)
    else:
        return redirect(url_for('log_in'))


@app.route("/adminlogout", methods=['GET'])
def admin_log_out():
    session.pop("admin_session", None)
    return redirect(url_for('log_in'))


@app.route("/adminProductManagement")
def admin_product_management():
    db = shelve.open('database/inventory.db', 'r')
    products_dict = db['Products']
    db.close()
    product_list = []
    for products in products_dict:
        product = products_dict[products]
        product_list.append(product)
    return render_template("adminProductManagement.html", count=len(product_list), product_list=product_list)


@app.route("/adminProductCreation", methods=["GET", "POST"])
def admin_product_creation():
    create_product_form = CreateProductForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and create_product_form.validate():
        products_dict = {}
        db = shelve.open('database/inventory.db', 'c')
        try:
            products_dict = db['Products']
        except:
            print("Error in retrieving Products from inventory.db")

        new_product = Product(create_product_form.name.data, int(create_product_form.price.data),
                              int(create_product_form.quantity.data), create_product_form.category.data,
                              int(create_product_form.discount.data), create_product_form.description.data, 0)
        products_dict[new_product.get_product_id()] = new_product
        if "product_pic" in request.files:
            pic = create_product_form.product_pic.data
            fn = pic.filename.split(".")
            ext = fn[len(fn)-1]
            if ext == "jpg" or ext == "png":
                pic_name = str(new_product.get_product_id()) + "." + str(ext)
                try:
                    new_product.set_picture(pic_name)
                    pic.save(os.path.join("static/images/product_pics/", pic_name))
                    print("saved")
                except:
                    print("upload failed")
        if "product_picture" not in request.files:
            print("not saved")
        print(new_product.get_product_id())
        db['Products'] = products_dict
        db.close()
        return redirect(url_for('admin_product_management'))
    return render_template("adminProductCreation.html", form=create_product_form)


@app.route("/adminProductUpdate/<id>/", methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(CombinedMultiDict((request.files, request.form)))
    db = shelve.open("database/inventory.db", 'w')
    products_dict = db["Products"]
    product = products_dict.get(id)
    if request.method == 'POST' and update_product_form.validate():
        if "product_pic" in request.files:
            pic = update_product_form.product_pic.data
            fn = pic.filename.split(".")
            ext = fn[len(fn)-1]
            if ext == "jpg" or ext == "png":
                pic_name = str(product.get_product_id()) + "." + str(ext)
                try:
                    product.set_picture(pic_name)
                    pic.save(os.path.join("static/images/product_pics/", pic_name))
                    print("saved")
                except:
                    print("upload failed")
        if "product_picture" not in request.files:
            print("not saved")
        products_dict.get(id).set_name(update_product_form.name.data)
        products_dict.get(id).set_price(int(update_product_form.price.data))
        products_dict.get(id).set_quantity(int(update_product_form.quantity.data))
        products_dict.get(id).set_discount(int(update_product_form.discount.data))
        products_dict.get(id).set_category(update_product_form.category.data)
        products_dict.get(id).set_description(update_product_form.description.data)
        if update_product_form.top.data.upper() == "YES" or update_product_form.top.data.upper() == "Y":
            products_dict.get(id).set_top(1)
        elif update_product_form.top.data.upper() == "NO" or update_product_form.top.data.upper() == "N":
            products_dict.get(id).set_top(0)

        db["Products"] = products_dict
        db.close()

        return redirect(url_for("admin_product_management"))
    else:
        db = shelve.open("database/inventory.db", 'r')
        products_dict = db["Products"]
        db.close()
        id = products_dict.get(id).get_product_id()
        update_product_form.name.data = products_dict.get(id).get_name()
        update_product_form.price.data = products_dict.get(id).get_price()
        update_product_form.quantity.data = products_dict.get(id).get_quantity()
        update_product_form.discount.data = products_dict.get(id).get_discount()
        update_product_form.category.data = products_dict.get(id).get_category()
        update_product_form.description.data = products_dict.get(id).get_description()
        if products_dict.get(id).get_top() == 1:
            update_product_form.top.data = "YES"
        elif products_dict.get(id).get_top() == 0:
            update_product_form.top.data = "NO"
    return render_template("adminProductUpdate.html", form=update_product_form, product_id=id, product=product)


@app.route('/deleteProduct/<id>', methods=['POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('database/inventory.db', 'w')
    products_dict = db['Products']
    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()
    return redirect(url_for('admin_product_management'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errorPage.html"), 404


@app.route("/aboutUs", methods=['GET', 'POST'])
def aboutUs():
    return render_template("aboutUs.html")


if __name__ == "__main__":
    app.run(debug=True)
