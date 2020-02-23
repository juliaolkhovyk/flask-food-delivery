from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class Authorization(FlaskForm):
    inputEmail = EmailField('Электропочта', validators=[
        DataRequired('Введите email'),
         Email('Недействительный email')],
         render_kw={'autofocus': True})

    inputPassword = PasswordField('Пароль', validators=[
        DataRequired('Введите пароль'),
        Length(min=8)])

    submit = SubmitField('Войти')

class Cart(FlaskForm):
    name = StringField('Ваше имя', validators=[
        DataRequired('Введите Ваше имя')
    ])

    address = StringField('Адрес', validators=[
        DataRequired('Введите Ваш адрес')
    ])

    inputEmail = EmailField('Электропочта', validators=[
        DataRequired('Введите email'),
         Email('Недействительный email')],
         render_kw={'autofocus': True})

    phone = TelField('Телефон', validators=[
        DataRequired('Введите номер телефона')
    ])

    submit = SubmitField('Оформить заказ')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired()
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email('Этот email недействительный')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, message="Пароль минимум с 8 символов")
    ])
    password2 = PasswordField('Повторите пароль', validators=[
        DataRequired(),
        EqualTo('password', message="Пароли должны совпадать.")
    ])
    submit = SubmitField('Регистрация')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста введите другой email.')



