from flask_wtf import FlaskForm
from app_store.models import User, Item
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo
from flask_wtf.file import FileField ,FileAllowed


class AdminRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            return ValidationError('Username Taken')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            return ValidationError('Email Taken')

class ItemForm(FlaskForm):
    item_pic = FileField('Image File', validators=[FileAllowed(['jpg','png','jpeg'])])
    name = StringField('Item Name', validators=[DataRequired()])
    description = StringField('Item Description', validators=[DataRequired()])
    submit = SubmitField('Create Item')

