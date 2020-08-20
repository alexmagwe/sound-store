from app_store import db, login_manager
from flask import Blueprint, redirect, flash, url_for, render_template, request
from flask_login import login_user, current_user, logout_user, login_required
from app_store.shop.forms import AddToCartForm
from app_store.models import User, Item, Order, Cart


shop = Blueprint('shop', __name__)

@shop.route('/')
@shop.route('/index')
def index():
    items = Item.query.all()
    return render_template('shop/store.html', items = items )


@shop.route('/add_to_cart/<int:item_id>',methods=['POST'])
@login_required
def add_to_cart(item_id):
    if current_user.is_authenticated:
        form = AddToCartForm(request.form)
        if form.validate_on_submit():
            item = Item.query.filter(item_id == item.id)
            user_id = current_user.id
            cart_item = Cart(user_id = user_id, item_id=item, quantity = quantity )
            db.session.add(cart_item)
            db.session.commit()
            flash(f'Added to Cart','Success')
            return redirect(url_for('shop/index'))
    return redirect(url_for('user.login'))
    

@shop.route('/item_extra/<int:item_id>', methods=['GET','POST'])
def item_extra(item_id):
    item = Item.query.get_or_404(item_id)
    form = AddToCartForm()
    return render_template('shop/item_extra.html', item = item , title = 'item discription' , form=form)


@shop.route('/remove_from_cart/<int:item_id>', methods=['GET','POST'])
def remove_from_cart(item_id):
    item = Item.query.filter(Item.id == item_id)
    cart_item = CartItem(item=item)
    db.session.delete(cart_item)
    db.session.commit()
    flash(f'Removed from Cart')


@shop.route('/cart/<int:name>', methods=['GET','POST'])
@login_required
def cart(name):
    name = current_user.id
    user = User.query.get_or_404(name)
    carts = Cart.query.filter_by(user_id = current_user.username).all()
    if not user:
        return redirect(url_for('user.login'))
    return render_template('shop/cart.html', title = current_user.username, carts=carts)