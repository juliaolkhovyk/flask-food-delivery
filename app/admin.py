from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from app import app
from app.models import Order, Meal, User, Category, Association
from app import db
from flask import redirect, url_for


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))       


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Association, db.session))

