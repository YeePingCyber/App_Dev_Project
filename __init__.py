from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for
import shelve
from userCart import UserCart
from Customer import Customer
from User import User
from Forms import CreateAdminForm, CreateLoginForm,CreateCustomerForm, CreatePaymentForm, CreateProductForm

# create product function
from createProduct import load_product

app = Flask(__name__)


# Customer Side


@app.route("/")
def home():
    # return render_template("adminAuction.html")
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def create_customer_log_in():

    # if request.form['submit_button'] == "Create An Account":
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate() and request.form['submit_button'] == "Create An Account":
        # I have shift it here
        # if request.form['submit_button'] == "Create An Account":
        print("hello")
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
            db['Users'] = customer_dict
            for i in customer_dict:
                print(customer_dict[i])
            db.close()
            return redirect(url_for('home'))
        else:
            print("Password does not match!")
            # Ill fix this to a popup ltr -Dylan

        print("hi")
    return render_template("loginpage.html", form=create_customer_form)

    # return render_template("loginpage.html", form=create_customer_form)


@app.route("/cart")
def cart():
    # append new product here
    cartList = ["BagA"]

    if len(cartList) > 0:
        return render_template("cart.html")
    else:
        return render_template("cart_empty.html")


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    create_payment_form = CreatePaymentForm(request.form)
    # if request.method == 'POST' and create_payment_form.validate():
    #     pass

    return render_template("checkout.html", form=create_payment_form)


@app.route("/mainshop")
def mainshop():
    return render_template("mainshop.html")


# Admin Side

@app.route("/admin")
def admin():
    return render_template("adminDashboard.html")


@app.route("/adminAuction")
def adminAuction():
    return render_template("adminAuction.html")


@app.route("/createAuction")
def createAuction():
    return render_template("createAuction.html")


@app.route("/adminOrders")
def adminOrders():
    return render_template("adminOrders.html")


@app.route("/adminUser")
def adminUser():
    return render_template("adminUser.html")


@app.route("/adminProductManagement")
def adminProductManagement():
    return render_template("adminProductManagement.html")


if __name__ == "__main__":
    app.run(debug=True)
