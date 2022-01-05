from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for
import shelve
from userCart import userCart
from Customer import Customer
from User import User
from Forms import CreateAdminForm, CreateCustomerForm, CreatePaymentForm, CreateProductForm

#create product function
from createProduct import load_product

app = Flask(__name__)


@app.route("/")
def home():
    #return render_template("adminAuction.html")
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        if create_customer_form.password.data == create_customer_form.confirm_password.data:
            customer_dict = {}
            db = shelve.open('user.db','c')
            try:
                customer_dict = db['Users']
            except:
                print("Error in retrieving Users from user.db")

            new_customer = Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                    create_customer_form.birthdate.data, create_customer_form.email.data, create_customer_form.password.data)
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

@app.route("/admin")
def admin():
    return render_template("adminDashboard.html")


@app.route("/adminAuction")
def adminAuction():
    return render_template("adminAuction.html")


@app.route("/adminOrders")
def adminOrders():
    return render_template("adminOrders.html")


@app.route("/adminUser")
def adminUser():
    return render_template("adminUser.html")


@app.route("/adminProductManagement")
def adminProductManagement():
    return render_template("adminProductManagement.html")


@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    create_payment_form = CreatePaymentForm(request.form)
    # if request.method == 'POST' and create_payment_form.validate():
    #     pass

    return render_template("checkout.html", form=create_payment_form)


@app.route("/mainshop")
def mainshop():
    return render_template("mainshop.html")


if __name__ == "__main__":
    app.run(debug=True)
