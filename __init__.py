from flask import Flask, render_template, flash
from flask import Flask, render_template, request, redirect, url_for
import shelve
import random
import hashlib as hl
from bs4 import BeautifulSoup
from datetime import date
from Customer import Customer
from Admin import Admin
from User import User
from Product import Product
from addtocart import Addtocart
from Auction import Auction
from ProcessCart import PaymentProcess, ShippingProcess
from UserBid import UserBid
from Forms import CreateAdminForm, CreateLoginForm, CreateCustomerForm, CreateShipmentForm, CreatePaymentForm, CreateProductForm, CreateAddCartForm, CreateAuctionForm, UpdateAdminForm, CreateBidForm, CreateForgetPassForm
# create product function
from createProduct import load_product

app = Flask(__name__)
app.secret_key = "abc"

inventory_dict = {}
db = shelve.open("database/inventory", "c")
try:
    if "Inventory" in db:
        inventory_dict = db["Inventory"]
    else:
        db["Inventory"] = inventory_dict
except:
    print("Error in retrieving Inventory from inventory.db")


inventory = Product("Arkose 35L Modular Bacpack", "Everyday backpack + small camera insert", 120, 50, "Camera", 0, 1)
inventory_dict[0] = inventory
db["Inventory"] = inventory_dict

print(db["Inventory"])
# for x in inventory_dict:
#     print(inventory_dict[x])
db.close()


# Customer Side
@app.route("/")
def home():
    return render_template("home.html", top4=inventory_dict)


@app.route("/login", methods=['GET', 'POST'])
def log_in():
    error = ""
    create_log_in_form = CreateLoginForm(request.form)
    if request.method == 'POST' and create_log_in_form.validate():
        db = shelve.open('database/user.db', 'r')
        users_dict = db['Users']
        hashed_password = hl.pbkdf2_hmac('sha256', str(create_log_in_form.login_password.data).encode(), b'salt', 100000).hex()
        for user in users_dict:
            if users_dict[user].get_email().upper() == create_log_in_form.login_email.data.upper() and users_dict[user].get_password() == hashed_password:
                if isinstance(users_dict[user], Customer):
                    return redirect(url_for('home'))
                elif isinstance(users_dict[user], Admin):
                    return redirect((url_for('admin')))
            elif users_dict[user].get_email() != create_log_in_form.login_email.data or users_dict[user].get_password() != hashed_password:
                error = "Invalid email or password"
        db.close()
    return render_template("loginpage.html", form=create_log_in_form, error= error)


@app.route("/register", methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        if create_customer_form.register_password.data == create_customer_form.confirm_password.data:
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
            print(new_customer.get_password())
            db['Users'] = customer_dict
            db.close()
            return redirect(url_for('log_in'))
        else:
            print("Password does not match!")
    return render_template("register.html", form=create_customer_form)


@app.route("/cart")
def cart():
    productA = {}
    productB = {}
    cart_dict = {"1":productA, "2":productB}

    # use list so that i can delete by using method clear() while remaining the key
    productAList = []
    productBList = []
    cartList = []
    db = shelve.open("database/addtocart", "c")
    try:
        if "Add_to_cart" in db:
            cart_dict = db["Add_to_cart"]
        else:
            db["Add_to_cart"] = cart_dict
    except:
        print("Error in retrieving Inventory from addtocart.db")

    db.close()
    if len(cart_dict["1"]) or len(cart_dict["2"]) > 0:
        # organising it such that its [[productA],[productB]]
        for x in cart_dict["1"]:
            productAList.append(cart_dict["1"][x])

        for y in cart_dict["2"]:
            productBList.append(cart_dict["2"][y])

        cartList.append(productAList)
        cartList.append(productBList)

        subtotal = 0
        for total in range(0, len(cartList)):
            for x in cartList[total]:
                subtotal += x.get_price()

        return render_template("cart.html", cartList=cartList, subtotal=subtotal)
    else:
        return render_template("cart_empty.html")


@app.route('/updateAddCart/<int:id>', methods=['POST'])
def updateAddCart(id):
    productA = {}
    productB = {}
    cart_dict = {"1":productA, "2":productB}

    productAList = []
    productBList = []
    cartList = []
    db = shelve.open("database/addtocart", "c")
    try:
        if "Add_to_cart" in db:
            cart_dict = db["Add_to_cart"]
        else:
            db["Add_to_cart"] = cart_dict
    except:
        print("Error in retrieving Inventory from addtocart.db")

    for x in cart_dict["1"]:
        productAList.append(cart_dict["1"][x])

    for y in cart_dict["2"]:
        productBList.append(cart_dict["2"][y])

    cartList.append(productAList)
    cartList.append(productBList)

    if request.method == "POST":
        addtocart = Addtocart(cartList[id][0].get_name(),cartList[id][0].get_description(),cartList[id][0].get_price(), 1,cartList[id][0].get_category(), cartList[id][0].get_discount(),cartList[id][0].get_top())
        if id == 0:
            productA[addtocart.get_id()] = addtocart
            cart_dict[str(id + 1)].update(productA)
        if id == 1:
            productB[addtocart.get_id()] = addtocart
            cart_dict[str(id + 1)].update(productB)

        db["Add_to_cart"] = cart_dict
        db.close()

    return redirect(url_for("cart"))


@app.route('/updateSubCart/<int:id>', methods=['POST'])
def updateSubCart(id):
    productA = {}
    productB = {}
    cart_dict = {"1":productA, "2":productB}

    productAList = []
    productBList = []
    cartList = []
    db = shelve.open("database/addtocart", "c")
    try:
        if "Add_to_cart" in db:
            cart_dict = db["Add_to_cart"]
        else:
            db["Add_to_cart"] = cart_dict
    except:
        print("Error in retrieving Inventory from addtocart.db")

    for x in cart_dict["1"]:
        productAList.append(cart_dict["1"][x])

    for y in cart_dict["2"]:
        productBList.append(cart_dict["2"][y])

    cartList.append(productAList)
    cartList.append(productBList)

    # put it back into dictionary format to be saved in database
    # getting the key
    list_keyA = []
    list_keyB = []

    for x in cartList[0]:
        list_keyA.append(x.get_id())

    for x in cartList[1]:
        list_keyB.append(x.get_id())

    if request.method == "POST":
        print(cart_dict)
        if id == 0:
            productAList.pop()
            productAupdate = dict(zip(list_keyA, cartList[0]))
            productBupdate = dict(zip(list_keyB, cartList[1]))
            cart_dict = {"1": productAupdate, "2": productBupdate}
        if id == 1:
            productBList.pop()
            productAupdate = dict(zip(list_keyA, cartList[0]))
            productBupdate = dict(zip(list_keyB, cartList[1]))
            cart_dict = {"1": productAupdate, "2": productBupdate}

        db["Add_to_cart"] = cart_dict
        db.close()

    return redirect(url_for("cart"))


@app.route('/deleteCart/<int:id>', methods=['POST'])
def delete_item(id):
    productA = {}
    productB = {}
    cart_dict = {"1": productA, "2": productB}

    # use list so that i can delete by using method clear() while remaining the key
    productAList = []
    productBList = []
    cartList = []
    db = shelve.open("database/addtocart", "c")
    try:
        if "Add_to_cart" in db:
            cart_dict = db["Add_to_cart"]
        else:
            db["Add_to_cart"] = cart_dict
    except:
        print("Error in retrieving Inventory from addtocart.db")

    for x in cart_dict["1"]:
        productAList.append(cart_dict["1"][x])

    for y in cart_dict["2"]:
        productBList.append(cart_dict["2"][y])

    cartList.append(productAList)
    cartList.append(productBList)

    cartList[id].clear()

    # put it back into dictionary format to be saved in database
    # getting the key
    list_keyA = []
    list_keyB = []

    for x in cartList[0]:
        list_keyA.append(x.get_id())

    for x in cartList[1]:
        list_keyB.append(x.get_id())

    productAupdate = dict(zip(list_keyA, cartList[0]))
    productBupdate = dict(zip(list_keyB, cartList[1]))
    cart_dict = {"1":productAupdate, "2":productBupdate}

    db['Add_to_cart'] = cart_dict
    db.close()
    if len(cart_dict["1"]) or len(cart_dict["2"]) > 0:
        return redirect(url_for("cart"))

    else:
        return render_template("cart_empty.html")


# need fix checkout too
@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    productA = {}
    productB = {}
    cart_dict = {"1": productA, "2": productB}

    # use list so that i can delete by using method clear() while remaining the key
    productAList = []
    productBList = []
    cartList = []
    db = shelve.open("database/addtocart", "c")
    try:
        if "Add_to_cart" in db:
            cart_dict = db["Add_to_cart"]
        else:
            db["Add_to_cart"] = cart_dict
    except:
        print("Error in retrieving Inventory from addtocart.db")

    # organising it such that its [[productA],[productB]]
    for x in cart_dict["1"]:
        productAList.append(cart_dict["1"][x])

    for y in cart_dict["2"]:
        productBList.append(cart_dict["2"][y])

    cartList.append(productAList)
    cartList.append(productBList)

    print(cartList)

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
        shipping_dict[shipping.get_shippingid()] = shipping
        db["Shipping"] = shipping_dict
        print(shipping_dict)

        return redirect(url_for("payment"))

    return render_template("checkout.html", form=create_shipment_form, cartList=cartList, subtotal=subtotal, grandtotal=grandtotal)


@app.route("/checkout/payment", methods=['GET', 'POST'])
def payment():
    productA = {}
    productB = {}
    cart_dict = {"1": productA, "2": productB}

    productAList = []
    productBList = []
    cartList = []
    db = shelve.open("database/addtocart", "c")
    try:
        if "Add_to_cart" in db:
            cart_dict = db["Add_to_cart"]
        else:
            db["Add_to_cart"] = cart_dict
    except:
        print("Error in retrieving Inventory from addtocart.db")

    for x in cart_dict["1"]:
        productAList.append(cart_dict["1"][x])

    for y in cart_dict["2"]:
        productBList.append(cart_dict["2"][y])

    cartList.append(productAList)
    cartList.append(productBList)

    subtotal = 0
    for total in range(0, len(cartList)):
        for x in cartList[total]:
            subtotal += x.get_price()

    grandtotal = subtotal + 4

    db.close()

    # paymentProcess_dict = { key : (shipping + payment) object}
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

    return render_template("payment.html", form=create_payment_form, cartList=cartList, subtotal=subtotal, grandtotal=grandtotal, ship=shipping_dict, payment=payment_dict)


@app.route("/checkout/paymentdone")
def paymentdone():
    sales = {}
    db = shelve.open("database/sales", "c")
    try:
        if "sales" in db:
            sales = db["sales"]
        else:
            db["sales"] = sales
    except:
        print("Error in retrieving Sales from sales.db")

    cart_dict = {}
    db = shelve.open("database/addtocart", "c")
    try:
        if "Add_to_cart" in db:
            cart_dict = db["Add_to_cart"]
        else:
            db["Add_to_cart"] = cart_dict
    except:
        print("Error in retrieving Inventory from addtocart.db")

    cartList = []
    total = 0
    for x in cart_dict:
        cartList.append(cart_dict[x])
        total += cart_dict[x].get_price()

    grandtotal = total + 4

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

    return render_template("paymentdone.html", subtotal=total, grandtotal=grandtotal, ship=shipping_dict, payment=payment_dict, sales=sales, cart_list=cartList)


# main shop
@app.route("/mainshop", methods=['GET', 'POST'])
def mainshop():
    return render_template("mainshop.html")


@app.route("/bag1", methods=['GET', 'POST'])
def bag1():
    x = 0
    addtocartform = CreateAddCartForm(request.form)
    if request.method == "POST":
        productA = {}
        productB = {}
        addtocart_dict = {"1":productA, "2":productB}
        db = shelve.open("database/addtocart", "c")

        try:
            if "Add_to_cart" in db:
                addtocart_dict = db["Add_to_cart"]
            else:
                db["Add_to_cart"] = addtocart_dict
        except:
            print("Error in retrieving Inventory from addtocart.db")

        addtocart = Addtocart(addtocartform.name.data, addtocartform.description.data,
                              int(addtocartform.price.data), int(addtocartform.quantity.data),
                              addtocartform.category.data, int(addtocartform.discount.data),
                              int(addtocartform.top.data))

        # key 0 stores product A, key 1 stores product B... {1:{},2:{}}
        if addtocart.get_name() == "Arkose 35L Modular Bacpack":
            productA[addtocart.get_id()] = addtocart
            addtocart_dict["1"].update(productA)

        db["Add_to_cart"] = addtocart_dict
        print(addtocart_dict)
        return redirect(url_for("cart"))

    return render_template("bag1.html", form=addtocartform, product=inventory_dict, x=x)


@app.route("/bag2", methods=['GET', 'POST'])
def bag2():
    x = 1
    addtocartform = CreateAddCartForm(request.form)
    if request.method == "POST":
        productA = {}
        productB = {}
        addtocart_dict = {"1":productA, "2":productB}
        db = shelve.open("database/addtocart", "c")

        try:
            if "Add_to_cart" in db:
                addtocart_dict = db["Add_to_cart"]
            else:
                db["Add_to_cart"] = addtocart_dict
        except:
            print("Error in retrieving Inventory from addtocart.db")

        addtocart = Addtocart(addtocartform.name.data, addtocartform.description.data,
                              int(addtocartform.price.data), int(addtocartform.quantity.data),
                              addtocartform.category.data, int(addtocartform.discount.data),
                              int(addtocartform.top.data))

        if addtocart.get_name() == "Arkose 20L Modular Bacpack":
            productB[addtocart.get_id()] = addtocart
            addtocart_dict["2"].update(productB)

        db["Add_to_cart"] = addtocart_dict
        print(addtocart_dict)
        return redirect(url_for("cart"))

    return render_template("bag2.html", form=addtocartform, product=inventory_dict, x=x)


# @app.route("/auction", methods=['GET', 'POST'])
# def auction():
#     auction_dict = {}
#     db = shelve.open('database/auction.db', 'c')
#     auction_dict = db["Auction"]
#     db.close()
#
#     bid_dict = {}
#     db = shelve.open('database/UserBid.db', 'r')
#
#     try:
#         bid_dict = db['UserBid']
#     except:
#         print("Error in retrieving userbid.db.")
#
#     db.close()
#
#     bid_list = []
#     for key in bid_dict:
#         user = bid_dict.get(key)
#         bid_list.append(user)
#
#     print(bid_list)
#
#     today = date.today().strftime('%Y-%m-%d')
#     ongoing = ""
#
#     for keys, values in auction_dict.items():
#         start = date.strftime(values.get_start_date(), '%Y-%m-%d')
#         end = date.strftime(values.get_end_date(), '%Y-%m-%d')
#
#         if start == today or today > start or start <= today and end <= today:
#             ongoing = values
#
#     # check key values
#     # for key in auction_dict:
#     #     product = auction_dict.get(key)
#     #     print(key)
#
#     create_bid_form = CreateBidForm(request.form)
#     if request.method == 'POST' and create_bid_form.validate():
#         bid_dict = {}
#         db = shelve.open('database/UserBid.db', 'c')
#
#         try:
#             bid_dict = db['UserBid']
#         except:
#             print("Error in retrieving userbid.db.")
#
#         bid_list = []
#         for key in bid_dict:
#             user = bid_dict.get(key)
#             bid_list.append(user)
#
#         userbidID = UserBid(create_bid_form.bidAmount.data)
#         bid_dict[userbidID.get_bidId()] = userbidID
#         db['UserBid'] = bid_dict
#
#         # print(bid_dict)
#         print("Test")
#         db.close()
#
#         return render_template('auction.html', auction_dict=auction_dict, form=create_bid_form, bid_list=bid_list, ongoing=ongoing)
#
#     return render_template('auction.html',auction_dict=auction_dict, bid_list=bid_list, form=create_bid_form, ongoing=ongoing)

@app.route("/auction", methods=['GET', 'POST'])
def auction():
    auction_dict = {}
    db = shelve.open('database/auction.db', 'c')
    auction_dict = db["Auction"]
    db.close()

    bid_dict = {}
    db = shelve.open('database/UserBid.db', 'r')

    try:
        bid_dict = db['UserBid']
    except:
        print("Error in retrieving userbid.db.")

    db.close()

    bid_list = []
    for key in bid_dict:
        user = bid_dict.get(key)
        bid_list.append(user)

    print(bid_list)

    today = date.today().strftime('%Y-%m-%d')
    ongoing = ""

    for keys, values in auction_dict.items():
        start = date.strftime(values.get_start_date(), '%Y-%m-%d')
        end = date.strftime(values.get_end_date(), '%Y-%m-%d')

        if start == today or today > start or start <= today and end <= today:
            ongoing = values

    return render_template('auction.html',auction_dict=auction_dict, bid_list=bid_list, ongoing=ongoing)


@app.route("/auctionForm", methods=['GET', 'POST'])
def auctionForm():
    create_bid_form = CreateBidForm(request.form)
    if request.method == 'POST' and create_bid_form.validate():
        bid_dict = {}
        db = shelve.open('database/UserBid.db', 'c')

        try:
            bid_dict = db['UserBid']
        except:
            print("Error in retrieving userbid.db.")


        userbidID = UserBid(create_bid_form.bidAmount.data)
        bid_dict[userbidID.get_bidId()] = userbidID
        db['UserBid'] = bid_dict

        # print(bid_dict)
        print("Test")
        db.close()

        return redirect(url_for("auction"))
    return render_template('auctionForm.html', form=create_bid_form)


@app.route("/deleteBid/<id>", methods=["POST"])
def delete_bid(id):
    db = shelve.open('database/UserBid.db', 'c')
    bid_dict = db['UserBid']

    bid_dict.pop(id)

    db['UserBid'] = bid_dict
    db.close()

    return redirect(url_for('auction'))


randomOTP = random.randint(111111, 999999)

@app.route("/forgetPassword", methods=["POST", "GET"])
def forget_password():
    create_forget_form = CreateForgetPassForm(request.form)

    # with open("templates/forgetPassword.html") as file:
    #     soup = BeautifulSoup(file, "html.parser")
    #
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

        if create_forget_form.newPass.data == create_forget_form.confirmPass.data and create_forget_form.otp.data == str(randomOTP):
            db = shelve.open("database/user.db", "w")
            users_dict = db['Users']

            users_dict.get(userId).set_password(create_forget_form.newPass.data)

            db['Users'] = users_dict
            db.close()

            return redirect(url_for("log_in"))

    return render_template("forgetPassword.html", form=create_forget_form, otpNum=randomOTP)


@app.route("/game")
def play_game():
    return render_template("game.html")

# Admin Side
@app.route("/admin")
def admin():
    labels = ["Oct", "Nov", "Dec", "Jan", "Feb", "March"]
    values = [25000, 20000, 30000, 25000, 40000, 100000]
    return render_template("adminDashboard.html", top4=inventory_dict, labels=labels, values=values)


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

            if start == today or today > start or start <= today and end <= today:
                ongoing = values
            elif start > today and end > today:
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
    create_admin_form = CreateAdminForm(request.form)
    if request.method == 'POST' and create_admin_form.validate():
        if create_admin_form.register_password.data == create_admin_form.confirm_password.data:
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
            print(new_admin.get_password())
            db['Users'] = admin_dict
            db.close()
            return redirect(url_for('admin_admin_management'))
        else:
            print("Password does not match!")
    return render_template("adminAdminCreation.html", form=create_admin_form)


@app.route("/adminAdminUpdate/<int:id>/", methods=["GET", "POST"])
def update_admin(id):
    update_admin_form = UpdateAdminForm(request.form)
    error = ""
    if request.method == 'POST' and update_admin_form.validate():
        users_dict = {}
        db = shelve.open('database/user.db', 'w')
        users_dict = db['Users']
        admin = users_dict.get(id)
        hashed_password = hl.pbkdf2_hmac('sha256', str(update_admin_form.current_password.data).encode(), b'salt', 100000).hex()
        if update_admin_form.current_password.data == "":
            admin.set_first_name(update_admin_form.first_name.data)
            admin.set_last_name(update_admin_form.last_name.data)
            admin.set_email(update_admin_form.email.data)
            admin.set_employee_id(update_admin_form.employee_id.data)
            db['Users'] = users_dict
            db.close()
            return redirect(url_for('admin_admin_management'))
        elif update_admin_form.current_password.data != "":
            if hashed_password == admin.get_password():
                admin.set_first_name(update_admin_form.first_name.data)
                admin.set_last_name(update_admin_form.last_name.data)
                admin.set_email(update_admin_form.email.data)
                admin.set_employee_id(update_admin_form.employee_id.data)
                admin.set_password(update_admin_form.new_password.data)
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
    return render_template("adminAdminUpdate.html", form=update_admin_form, error = error)


@app.route("/adminProductManagement")
def admin_product_management():
    return render_template("adminProductManagement.html")


if __name__ == "__main__":
    app.run(debug=True)
