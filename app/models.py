from app import db
import enum
from datetime import datetime
from validate_email import validate_email
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def is_email_valid(self):
        return validate_email(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


class Association(db.Model):
    __tablename__ = 'orders_meals_association'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))

    # ... any other fields

    amount = db.Column(db.Integer)

    order = db.relationship('Order', back_populates="meals")
    meal = db.relationship('Meal', back_populates="orders")


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(32), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    orders = db.relationship('Association', back_populates="meal")

    def __repr__(self):
        return '<Meal {}>'.format(self.title)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    rus_title = db.Column(db.String(32))
    id_meal = db.relationship('Meal', backref='meal', lazy='dynamic')
    
    def __repr__(self):
        return '<Category {}>'.format(self.title)


class StatusType(enum.Enum):
    NEW = 'Новый'
    DELIVERING = 'Выполняется'
    ALREADY = 'Готово'


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    summ = db.Column(db.Integer)
    status = db.Column(db.Enum(StatusType), default=StatusType.NEW)
    clientName = db.Column(db.String(50))
    clientPhone = db.Column(db.String(50))
    clientAddress = db.Column(db.String(100))
    clientEmail = db.Column(db.String(100))
    meals = db.relationship('Association', back_populates="order")

    def __repr__(self):
        return '<Order {}'.format(self.summ)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

