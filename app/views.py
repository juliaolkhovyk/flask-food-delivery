from flask import render_template, flash, redirect, url_for, session
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import Authorization, Cart, RegistrationForm
from app.models import User, Category, Meal, Order


def basket(freq_menu):
    if freq_menu:
        summ = len(set(freq_menu))
        sum_money = 0
        for item in set(freq_menu):
            meal = Meal.query.filter_by(id=item).first()
            sum_money += meal.price * freq_menu.count(item)
        return summ, sum_money


def basket_food(items):
    freq = dict()
    for item in items:
        meal = Meal.query.filter_by(id=item).first()
        freq[meal] = items.count(item)
    return freq


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/')
def main():
    categories = Category.query.all()
    meals = dict()
    for category in categories:
        meals[category.rus_title] = Meal.query.filter_by(category=category.id).all()
    return render_template("main.html", meals=meals,
                           basket=basket(session.get('cart')))


freq = {}


@app.route('/addtocart/<int:id>')
def addtocart(id):
    cart = session.get('cart') or []
    cart.append(id)
    session['cart'] = cart
    session.modified = True
    meal = Meal.query.filter_by(id=id).first()
    flash('Блюдо {} добавлено в корзину'.format(meal.title))
    return redirect(url_for('main'))

@app.route('/deletefromcart/<int:id>')
def deletefromcart(id):
    meal = Meal.query.filter_by(id=id).first()
    new_cart = list(filter(lambda x: x != id, session.get('cart')))
    session['cart'] = new_cart
    session.modified = True
    meal = Meal.query.filter_by(id=id).first()
    flash('Блюдо {} удалено с корзины'.format(meal.title))
    return redirect(url_for('cart', items=basket_food(session.get('cart'))))

@app.route('/cart/', methods=['GET', 'POST'])
def cart():
    form = Cart()

    if form.validate_on_submit():
        summ = 0
        order = Order(clientName=form.name.data,
                      clientPhone=form.phone.data,
                      clientAddress=form.address.data,
                      clientEmail=form.inputEmail.data
                      )
      
        for meal, count in basket_food(session.get('cart')).items():
            summ = summ + meal.price * count

        order.summ = summ
        db.session.add(order)
        db.session.commit()
        session.pop('cart')
  
    return render_template("cart.html", form=form, title="Stepik | Cart",
                           menu=basket_food(session.get('cart')),
                           basket=basket(session.get('cart')))


@app.route('/account/')
@login_required
def account():
    orders = Order.query.filter_by(clientEmail=current_user.email).all()
    return render_template("account.html", title='Аккаунт', orders=orders)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = Authorization()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.inputEmail.data).first()
        print(form.inputEmail.data)
        print(form.inputPassword.data)
        if user is None or not user.password_valid(form.inputPassword.data):
            flash("Неправильный логин или пароль")
            return redirect(url_for('login'))
        login_user(user)
        flash('Вы успешно вошли в свой аккаунт')
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
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(name=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Ты зарегистрирован')
        return redirect(url_for('login'))
    return render_template("registration.html", title='Регистрация', form=form)


