from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import EmailField, DateField, FloatField, IntegerField


class CreateCustomerForm(Form):
    first_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last-Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    login_email = EmailField('', [validators.Email(), validators.DataRequired()], render_kw={"placeholder": "Email Address"})
    email = EmailField('Register-Email', [validators.Email(), validators.DataRequired()])
    birthdate = DateField('birthdate', format='%Y-%m-%d')
    login_password = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={"placeholder": "Password"})
    register_password = StringField('Register-Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    confirm_password = StringField('Confirm-Password', [validators.Length(min=1, max=150), validators.DataRequired()])


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
