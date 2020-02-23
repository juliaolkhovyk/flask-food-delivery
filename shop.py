from app import app, db
from app.models import User, Meal, Category, Order

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Meal': Meal, 'Category': Category,
    'Order': Order}
