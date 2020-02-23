from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
migrate = Migrate()


app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)
csrf.init_app(app)
login = LoginManager(app)
login.login_view = 'login'
db.init_app(app)
migrate.init_app(app, db)
    

from app.models import User, Order, Category, Meal
from app import views
from app.admin import admin


