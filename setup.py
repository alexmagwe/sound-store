from app_store import create_app, db, migrate
from flask_migrate import MigrateCommand
from flask_script import Manager, Shell
from app_store.models import User, Item, Order, Cart, Ordereditem, Category 


app = create_app()
manager=Manager(app)
@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Item':Item, 'Order':Order, 'Cart':Cart, 'Ordereditem':Ordereditem, 'Category': Category}
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

if __name__=='__main__':
    manager.run()
