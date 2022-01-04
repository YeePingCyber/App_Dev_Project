from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for
import shelve
from userCart import userCart
from Forms import CreateAdminForm, CreateCustomerForm, CreatePaymentForm, CreateProductForm

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("Home.html")


@app.route("/login")
def login():
    return render_template("loginpage.html")


@app.route("/admin")
def admin():
    return render_template("adminDashboard.html")


@app.route("/adminAuction")
def adminAuction():
    return render_template("adminAuction.html")


@app.route("/adminSupplier")
def adminSupplier():
    return render_template("adminSupplier.html")


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
