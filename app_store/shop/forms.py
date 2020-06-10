from flask_wtf import FlaskForm 
from wtforms import  StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired
from app_store.models import Order


class ShoppingCartForm(FlaskForm):
    user_address = StringField('Address', validators=[DataRequired()])
    item_quantity = RadioField('No of Items', validators=[DataRequired()])
    payment = SelectField('Payment Method', validators=[DataRequired()])
    submit = SubmitField('Order')


