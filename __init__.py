from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for
import shelve
from userCart import userCart

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/cart")
def cart():
    userCart()
    if userCart.count == 0:
        return render_template("cart_empty.html")

    else:
        return render_template("cart.html")


if __name__ == "__main__":
    app.run(debug=True)