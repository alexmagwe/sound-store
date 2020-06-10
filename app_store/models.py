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
    orders = db.relationship('Order',backref='consumer', lazy=True )

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    item_pic = db.Column(db.String(80), nullable = False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(200), nullable=False)
    orders = db.relationship('Order',backref='purchased', lazy=True )
    cartitems = db.relationship('CartItem', backref='product')

    def __repr__(self):
        return f"User('{self.item_pic}','{self.name}','{self.description}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    user_address = db.Column(db.String(100), nullable = False)
    item_quantity = db.Column(db.Integer, default = 1)
    payment = db.Column(db.String(100), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable = False)

    def __repr__(self):
        return f"User('{self.id}','{self.date_posted}','{self.user_address}', '{self.item_quantity}','{self.payment}')"

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable = True)

    def __repr__(self):
        return f"User('{self.id}')

class Permissions(ModelView):

    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort

admin.add_view(ModelView(User, db.session)) 
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Order, db.session))  