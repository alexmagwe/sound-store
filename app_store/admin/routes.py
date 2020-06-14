import secrets
import os
from PIL import Image
from app_store import admin, login_manager, db, bcrypt
from app_store.models import User, Item, Order
from flask import Blueprint, render_template, redirect, url_for, flash
from app_store.admin.forms import AdminRegisterForm, ItemForm
from flask_login import login_user, current_user, logout_user, login_required

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

def save_picture(form_item_pic):
    random_hex = secrets.token_hex(10)
    _, f_ext = os.path.splitext(form_item_pic.filename)
    picture_fn = random_hex+f_ext
    size = (200,200)
    img = Image.open(form_item_pic)
    img.thumbnail(size)
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    if not os.path.exists(os.path.join(app.root_path,'static/images')):
        print('Directory does not exist, creating one...')
        os.mkdir(os.path.join(app.root_path, 'static/images'))
    img.save(picture_path)
    print('Image Saved')
    return picture_fn
    


@admin.route('/create_item', methods=['GET','POST'])
@login_required
def create_item():
    if current_user.is_admin:
        form = ItemForm()
        if form.validate_on_submit():
            image_file = save_picture(form.item_pic.data)
            item = Item(item_pic = image_file,  name = form.name.data, description = form.description.data, )
            db.session.add(item)
            db.session.commit()
            flash(f'Item, {form.name.data} succesfully added to database','success')
            return redirect(url_for('admin.create_item'))
        return render_template('admin/create_item.html', title='Add to Database', form=form)
    else:
        return redirect(url_for('errors.404'))
