from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, HiddenField, validators
from wtforms.fields import EmailField, DateField, FloatField, IntegerField
import shelve


class CreateCustomerForm(Form):
    first_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()],render_kw={"placeholder": "First Name"})
    last_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()],render_kw={"placeholder": "Last Name"})
    email = EmailField('', [validators.Email(), validators.DataRequired()],render_kw={"placeholder": "Email"})
    birthdate = DateField('', format='%Y-%m-%d', render_kw={"placeholder": "DD/MM/YYYY"})
    register_password = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Confirm Password"})
    login_email = EmailField('', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email Address"})
    login_password = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Password"})



class CreateLoginForm(Form):
    login_email = EmailField('', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email Address"})
    login_password = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Password"})


class CreateProductForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = FloatField('Price', validators.DataRequired())
    quantity = IntegerField('Quantity', validators.DataRequired())
    category = StringField('Category', [validators.Length(min=1, max=150), validators.DataRequired()])
    discount = FloatField('Discount', validators.DataRequired())
    description = TextAreaField('Description', [validators.Length(min=1, max=300), validators.DataRequired()])


class CreateAdminForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = StringField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    employee_id = StringField('Employee ID', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateAddCartForm(Form):
    inventory_dict = {}
    db = shelve.open("inventory", "c")
    try:
        if "Inventory" in db:
                inventory_dict = db["Inventory"]
        else:
            db["Inventory"] = inventory_dict
    except:
        print("Error in retrieving Inventory from inventory.db")

    # for x in inventory_dict:
    #     print(inventory_dict[x])
    db.close()

    name = HiddenField('Name', [validators.Length(min=1, max=150)], default=inventory_dict[0])
    price = HiddenField('Price')
    quantity = HiddenField('Quantity')
    category = HiddenField('Category', [validators.Length(min=1, max=150)])
    discount = HiddenField('Discount')
    description = HiddenField('Description', [validators.Length(min=1, max=300)])


class CreatePaymentForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email"})
    country = SelectField("Country", choices=[("1", "SG"), ("2", "AU")], render_kw={"placeholder": "Country"})
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Last Name"})
    company = StringField("Company", [validators.Length(min=1, max=150)], render_kw={"placeholder": "Company (optional)"})
    address = TextAreaField('Mailing Address', [validators.optional(), validators.length(max=200)], render_kw={"placeholder": "Address"})
    apartment = StringField("Apartment", [validators.Length(min=1, max=150)], render_kw={"placeholder": "Apartment (optional)"})
    postal_code = StringField("Postal Code", [validators.Length(min=6, max=6), validators.DataRequired()], render_kw={"placeholder": "Postal Code"})
    city = StringField("City", [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "City"})
    phone = StringField("Phone", [validators.Length(min=8, max=8)], render_kw={"placeholder": "Phone (optional)"})
    discount = StringField("Gift card or discount code", [validators.Length(min=4, max=8)], render_kw={"placeholder": "Gift card or discount code"})


class CreateAuctionForm(Form):
    product_name = StringField('', [validators.Length(min=1, max=200), validators.DataRequired()], id="pName", render_kw={"placeholder": "Product Name"})
    base_amount = IntegerField('', [validators.NumberRange(min=1, max=100, message="The value should be between 1 - 100"), validators.DataRequired()], id="bAmt", render_kw={"placeholder": "Base Amount"})
    minimum_amount = IntegerField('', [validators.NumberRange(min=10, max=100, message="The value should be between 10 - 100"), validators.DataRequired()], id="mAmt", render_kw={"placeholder": "Minimum Amount"})
    start_date = DateField('Start Date:', format='%Y-%m-%d', render_kw={"placeholder": "DD/MM/YYYY"})
    end_date = DateField('', format='%Y-%m-%d', render_kw={"placeholder": "DD/MM/YYYY"})
