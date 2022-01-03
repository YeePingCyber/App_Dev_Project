from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import EmailField, DateField, FloatField, IntegerField


class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    birthdate = DateField('birthdate', format='%Y-%m-%d')
    password = StringField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])


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
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    country = SelectField("Country", choices=[("1","SG"),("2","AU")])
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [validators.optional(), validators.length(max=200)])
    postal_code = StringField("Postal Code", [validators.Length(min=6, max=6), validators.DataRequired()])
    city = StringField("City", [validators.Length(min=1, max=150), validators.DataRequired()])