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


@app.route("/cart", methods=['GET', 'POST'])
def cart():
    userCart()
    if userCart.count == 0:
        return render_template("cart_empty.html")

    else:
        create_payment_form = CreatePaymentForm(request.form)
        if request.method == 'POST' and create_payment_form.validate():
            pass

        return render_template("cart.html", form=create_payment_form)


@app.route("/mainshop")
def mainshop():
    return render_template("mainshop.html")


if __name__ == "__main__":
    app.run(debug=True)
