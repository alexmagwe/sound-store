from flask_wtf import FlaskForm 
from wtforms import  IntegerField, SubmitField
from wtforms.validators import DataRequired
from app_store.models import Cart


class AddToCartForm(FlaskForm):
    quantity = IntegerField('Set Quantity', validators=[DataRequired()])
    submit = SubmitField('Add to Cart')


