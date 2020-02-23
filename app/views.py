from flask import Flask, render_template, request, flash, redirect, url_for, session
from app import app, db, login
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import Authorization, Cart, RegistrationForm
from app.models import User, Category, Meal, Order, StatusType
from datetime import timedelta

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def main():
    categories = Category.query.all()
    meals = dict()
    for category in categories:
        meals[category.rus_title] = Meal.query.filter_by(category=category.id).all()
    return render_template("main.html", meals=meals)

@app.route('/addtocart/<int:id>')
def addtocart(id):
    cart = session.get('cart', [])
    cart.append(id)
    session['cart'] = cart
    session.modified = True
    freq = {}
    for items in session.get('cart'):
        freq[items] = session.get('cart').count(items)
    
    return redirect(url_for('cart', items=freq))

@app.route('/deletefromcart/<int:id>')
def deletefromcart(id):
    new_cart = list(filter(lambda x: x!= id, session.get('cart')))
    session['cart'] = new_cart
    session.modified = True
    freq = {}
    for items in session.get('cart'):
        freq[items] = session.get('cart').count(items)
    return redirect(url_for('cart', items=freq))

@app.route('/cart/<items>/', methods=['GET','POST'])
def cart(items):
    items = eval(items)
    form = Cart()
    menu = dict()
    for key, value in items.items():
        meal = Meal.query.filter_by(id=key).first()
        menu[meal] = value
    if form.validate_on_submit():
        summ = 0
        order = Order(clientName = form.name.data,
                      clientPhone = form.phone.data,
                      clientAddress = form.address.data,
                      clientEmail = form.inputEmail.data
        )
        db.session.add(order)
        ordered_meals = []
        for meal, count in menu.items():
            for _ in range(value):
                order.meals.append(meal)
            summ = summ + meal.price * count
        order.summ = summ
        db.session.commit()
        session.pop('cart')
        menu = dict()
    return render_template("cart.html", form=form, title="Stepik | Cart", menu=menu)

@app.route('/account/')
@login_required
def account():
    return render_template("account.html", title='Аккаунт')

@app.route('/login/', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = Authorization()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.inputEmail.data).first()
        print(form.inputEmail.data)
        print(form.inputPassword.data)
        if user is None or not user.password_valid(form.inputPassword.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('account'))
    return render_template("auth.html", form=form, title='Stepik delivery')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route('/registration/', methods=["GET", "POST"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form=RegistrationForm()

    if form.validate_on_submit():
        user = User(name=form.username.data,
                    email=form.email.data,
                    address=form.address.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Ты зарегистрирован')
        return redirect(url_for('login'))
    return render_template("registration.html", title='Регистрация', form=form)


