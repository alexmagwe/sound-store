from app_store import db, login_manager
from flask import Blueprint, redirect, flash, url_for, render_template
from flask_login import login_user, current_user, logout_user, login_required
from app_store.shop.forms import ShoppingCartForm
from app_store.models import User, Item, Order, CartItem


shop = Blueprint('shop', __name__)

@shop.route('/')
@shop.route('/index')
def index():
    item = Item.query.all()
    return render_template('shop/store.html', item=item)


@shop.route('/add_to_cart/<int:item_id>',methods=['POST'])
def add_to_cart(item_id):
    item = Item.query.filter(Item.id == item_id)
    cart_item = CartItem(item=item)
    db.session.add(cart_item)
    db.session.commit()
    flash(f'Added to Cart','Success')
    

@shop.route('/remove_from_cart/<int:item_id>', methods=['GET','POST'])
def remove_from_cart(item_id):
    item = Item.query.filter(Item.id == item_id)
    cart_item = CartItem(item=item)
    db.session.delete(cart_item)
    db.session.commit()
    flash(f'Removed from Cart')


@shop.route('/cart/<int:user_id>', methods=['GET','POST'])
@login_required
def cart(user_id):
    user = current_user
    item = Item.query_all()
    if not user:
        return redirect(url_for('user.login'))
    form = ShoppingCartForm()
    if form.validate_on_submit():
        for item in items:
            order = Order(user_address = form.user_address.data, item_quantity=form.item_quantity.data, payment=form.payment.data, consumer = current_user, purchased=item_id)
            db.session.add(order)
            db.session.commit()
        flash(f'Order placement succesful','succes')
        return redirect(url_for('shop.index'))
    return render_template('shop/cart.html', title = 'user_name', form=form)