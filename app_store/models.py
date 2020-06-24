from datetime import datetime
from app_store import db, admin, login_manager
from flask_login import UserMixin, LoginManager, current_user
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    username = db.Column(db.String(40), unique=True, nullable = False)
    email = db.Column(db.String(200), unique = True, nullable= False)
    password = db.Column(db.String(60), nullable= False)
    is_admin = db.Column(db.Boolean, default = False)
    address = db.Column(db.String(100), nullable = True)
    post_code = db.Column(db.String(100), nullable = True)
    county = db.Column(db.String(100), nullable = True)
    ward = db.Column(db.String(100), nullable = True)
    tell = db.Column(db.String(100), nullable = True)
    orders = db.relationship('Order',backref='consumer', lazy=True )
    carts = db.relationship('Order',backref='shopper', lazy=True )

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.address}','{self.tell}','{self.post_code}','{self.county}', '{self.ward}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    categoryname = db.Column(db.String(100), nullable = False)
    items = db.relationship('Item', backref='type', lazy = True )

    def __repr__(self):
        return f"Category('{self.categoryname}')"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    item_pic = db.Column(db.String(80), nullable = False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.DECIMAL, nullable=False)

    orders = db.relationship('Order',backref='buying', lazy=True )
    Ordereditems = db.relationship('Ordereditem',backref='paid_goods', lazy=True )
    carts = db.relationship('Cart', backref='product', lazy = True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = True)

    def __repr__(self):
        return f"Item('{self.item_pic}','{self.name}','{self.description}','{self.price}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    total_price = db.Column(db.DECIMAL, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __repr__(self):
        return f"Order('{self.order_date}','{self.total_price}','{self.userid}'')"

class Ordereditem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    order_id = db.Column(db.Integer,db.ForeignKey('order.id'), nullable=False)
    item_id = db.Column(db.Integer,db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Ordereditem('{self.orderid}','{self.productid}','{self.quantity}')"


class Cart(db.Model):
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable = False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False, primary_key=True)
    quantity = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Cart('{self.user_id}','{self.item_id}','{self.quantity}')"

class Permissions(ModelView):

    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort

admin.add_view(ModelView(User, db.session)) 
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Ordereditem, db.session))
admin.add_view(ModelView(Cart, db.session))


