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
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
