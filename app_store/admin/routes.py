import secrets, os
from app_store import admin, login_manager, db, bcrypt
from app_store.models import User, Item, Order
from flask import Blueprint, render_template, redirect, url_for, flash
from app_store.admin.forms import AdminRegisterForm, ItemForm
from flask_login import login_user, current_user, logout_user, login_required
from app_store.admin.utils import save_picture1, save_picture2, save_picture3

admin = Blueprint('admin', __name__)


@admin.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return render_template('admin/dashboard.html', title = 'Admin')
    else:
        return redirect(url_for('errors.404'))   

@admin.route('/admin_register', methods=['GET','POST'])
def admin_register():
    if current_user.is_authenticated:
        return redirect(url_for('shop.index'))
    form = AdminRegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data, email=form.email.data, password = hashed_password, is_admin = True)
        db.session.add(user)
        db.session.commit()
        flash(f'Registered Successfully','success')
        return redirect(url_for('user.login'))
    return render_template('admin/admin_register.html', form=form, title='Admin-Registration')


@admin.route('/create_item', methods=['GET','POST'])
@login_required
def create_item():
    if current_user.is_admin:
        form = ItemForm()
        if form.validate_on_submit():
            image_file1 = save_picture1(form.item_pic1.data)
            image_file2 = save_picture2(form.item_pic2.data)
            image_file3 = save_picture3(form.item_pic3.data)
            item = Item(item_pic1 = image_file1, item_pic2 = image_file2, item_pic3 = image_file3, name = form.name.data, description = form.description.data, price = form.price.data )
            db.session.add(item)
            db.session.commit()
            flash(f'Item, {form.name.data} succesfully added to database','success')
            return redirect(url_for('admin.create_item'))
        return render_template('admin/create_item.html', title='Add to Database', form=form)
    else:
        return redirect(url_for('errors.404'))
