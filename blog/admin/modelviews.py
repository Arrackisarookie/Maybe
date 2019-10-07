from flask import redirect, request, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return super(IndexView, self).index()


class AuthModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))


class CategoryView(AuthModelView):
    can_delete = False


class ArticleView(AuthModelView):
    can_view_details = True
    create_modal = True
    edit_modal = True


class TagView(AuthModelView):
    pass


class UserView(AuthModelView):
    column_exclude_list = ['password_hash', ]
