from app_store import login_manager, db, bcrypt
from flask import Blueprint, flash, render_template, url_for, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app_store.user.forms import LoginForm, RegisterForm
from app_store.models import User, Order



user = Blueprint('user', __name__)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('shop.index'))
    form = LoginForm()
    if  form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('shop.index'))
        else:
            flash('Login was Unsuccessful. Please check your Email and Password')
    return render_template('user/login.html', title = 'Sign In' ,form=form)        


@user.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('shop.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Registered Succesfully', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', title='Register' ,form=form)



@user.route('/account/<name>', methods=['GET','POST'])
@login_required
def account(name):
    order = Order.query.all()
    user = current_user
    if not user:
        return redirect(url_for('user.login'))
    return render_template('user/account.html', title = 'username', name=current_user.username ,order=order)


@user.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('shop.index'))
