from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for
import shelve

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/cartEmpty")
def empty_cart():
    return render_template("cart_empty.html")\


@app.route("/login")
def login():
    return render_template("loginpage.html")


if __name__ == "__main__":
    app.run(debug=True)
