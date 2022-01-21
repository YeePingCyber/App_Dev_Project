from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, HiddenField, validators
from wtforms.fields import EmailField, DateField, FloatField, IntegerField, PasswordField
import shelve
from Product import Product


class CreateCustomerForm(Form):
    first_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()],
                             render_kw={"placeholder": "First Name"})
    last_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()],
                            render_kw={"placeholder": "Last Name"})
    email = EmailField('', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email"})
    birthdate = DateField('', format='%Y-%m-%d', render_kw={"placeholder": "DD/MM/YYYY"})
    register_password = PasswordField('', [validators.Length(min=8, max=15), validators.DataRequired(), validators.EqualTo('confirm_password', message='Passwords must match')],
                                      render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('', [validators.Length(min=8, max=15), validators.DataRequired()],
                                     render_kw={"placeholder": "Confirm Password"})


class CreateLoginForm(Form):
    login_email = EmailField('', [validators.Email(), validators.DataRequired()],
                             render_kw={"placeholder": "Email Address"})
    login_password = PasswordField('', [validators.Length(min=1, max=150), validators.DataRequired()],
                                   render_kw={"placeholder": "Password"})


class CreateProductForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    quantity = IntegerField('Quantity', [validators.DataRequired()])
    category = StringField('Category', [validators.Length(min=1, max=150), validators.DataRequired()])
    discount = FloatField('Discount', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.Length(min=1, max=300), validators.DataRequired()])


class CreateAdminForm(Form):
    first_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "First Name"})
    last_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Last Name"})
    email = EmailField('', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email"})
    register_password = PasswordField('', [validators.Length(min=8, max=15), validators.DataRequired(),validators.EqualTo('confirm_password', message='Passwords must match')],render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('', [validators.Length(min=8, max=15), validators.DataRequired()],render_kw={"placeholder": "Confirm Password"})
    employee_id = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Employee ID"})


class UpdateAdminForm(Form):
    first_name = StringField('', [validators.Length(min=1, max=150)], render_kw={"placeholder": "First Name"})
    last_name = StringField('', [validators.Length(min=1, max=150)], render_kw={"placeholder": "Last Name"})
    email = EmailField('', [validators.Email()], render_kw={"placeholder": "Email"})
    current_password = PasswordField('',[validators.Length(min=8, max=15), validators.Optional(strip_whitespace=True)],render_kw={"placeholder": "Current Password"})
    new_password = PasswordField('',[validators.Length(min=8, max=15), validators.Optional(strip_whitespace=True)],render_kw={"placeholder": "New Password"})
    employee_id = StringField('', [validators.Length(min=1, max=150)], render_kw={"placeholder": "Employee ID"})


class CreateAddCartForm(Form):
    product_id = HiddenField("")
    name = HiddenField('', [validators.Length(min=1, max=150)])
    price = HiddenField('')
    quantity = HiddenField('')
    category = HiddenField('', [validators.Length(min=1, max=150)])
    discount = HiddenField('')
    description = HiddenField('', [validators.Length(min=1, max=300)])
    top = HiddenField('')


class CreateShipmentForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email"})
    country = SelectField("Country", choices=[("1", "SG"), ("2", "AU")], render_kw={"placeholder": "Country"})
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Last Name"})
    company = StringField("Company", render_kw={"placeholder": "Company (optional)"})
    address = TextAreaField('Mailing Address', [validators.optional(), validators.length(max=200)], render_kw={"placeholder": "Address"})
    apartment = StringField("Apartment", render_kw={"placeholder": "Apartment (optional)"})
    postal_code = StringField("Postal Code", [validators.Length(min=6, max=6), validators.DataRequired()], render_kw={"placeholder": "Postal Code"})
    city = StringField("City", [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "City"})
    phone = StringField("Phone", [validators.Length(min=8, max=8)], render_kw={"placeholder": "Phone (optional)"})
    discount = StringField("Gift card or discount code", [validators.Length(min=4, max=8)], render_kw={"placeholder": "Gift card or discount code"})


class CreatePaymentForm(Form):
    card_num = StringField('', [validators.Length(min=16, max=16), validators.DataRequired()], render_kw={"placeholder": "Card number"})
    name_card = StringField("", [validators.DataRequired()], render_kw={"placeholder": "Name on card"})
    expire = DateField('', [validators.DataRequired()], render_kw={"placeholder": "Expiration date (MM / YY)"})
    ccv = StringField('', [validators.Length(min=3, max=3), validators.DataRequired()], render_kw={"placeholder": "Security code"})
    discount = StringField("Gift card or discount code", [validators.Length(min=4, max=8)], render_kw={"placeholder": "Gift card or discount code"})


class CreateAuctionForm(Form):
    product_name = StringField('', [validators.Length(min=1, max=200), validators.DataRequired()], id="pName", render_kw={"placeholder": "Product Name"})
    base_amount = IntegerField('', [validators.NumberRange(min=1, max=100, message="The value should be between 1 - 100"), validators.DataRequired()], id="bAmt", render_kw={"placeholder": "Base Amount"})
    minimum_amount = IntegerField('', [validators.NumberRange(min=10, max=100, message="The value should be between 10 - 100"), validators.DataRequired()], id="mAmt", render_kw={"placeholder": "Minimum Amount"})
    start_date = DateField('', format='%Y-%m-%d', render_kw={"placeholder": "DD/MM/YYYY"})
    end_date = DateField('', format='%Y-%m-%d', render_kw={"placeholder": "DD/MM/YYYY"})
    description = TextAreaField('', [validators.DataRequired()], id="desc",  render_kw={"rows": "5", "cols": "30", "placeholder": "Enter prduct description"})


class CreateBidForm(Form):
    bidAmount = IntegerField('', [validators.NumberRange(min=1, max=1000, message="The value should be higher than minimum amount"), validators.DataRequired()], render_kw={"placeholder": "Your Bid"})

class CreateForgetPassForm(Form):
    email = EmailField('', [validators.Email(), validators.DataRequired()], id="email", render_kw={"placeholder": "Email Address"})
    newPass = PasswordField('', [validators.Length(min=8, max=150), validators.DataRequired(),
                       validators.Optional(strip_whitespace=True)], id="NewPass", render_kw={"placeholder": "New Password"})
    confirmPass = PasswordField('', [validators.Length(min=8, max=150), validators.DataRequired(),
                       validators.Optional(strip_whitespace=True)], id="confirmPass", render_kw={"placeholder": "Confirm Password"})
    otp = PasswordField('', [validators.Length(min=6, max=150), validators.DataRequired(),
                       validators.Optional(strip_whitespace=True)], id="otpField", render_kw={"placeholder": "One Time Password"})

