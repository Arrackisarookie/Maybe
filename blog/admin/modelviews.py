from flask import redirect, request, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms.validators import DataRequired

from blog.models import Category, Tag


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
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['articles']


class ArticleView(AuthModelView):
    can_view_details = True
    column_list = [
        'id',
        'title',
        'add_time',
        'category',
        'tags',
        'url'
    ]
    column_labels = {
        'title': 'Title',
        'tags.name': 'Tags',
    }
    column_sortable_list = [
        'id',
        'title',
        'add_time',
    ]
    column_default_sort = ('id', True)
    form_excluded_columns = ['add_time']
    form_args = {
        'body': {
            'validators': [DataRequired()]
        }
    }
    form_widget_args = {
        'body': {
            'rows': 10
        }
    }


class TagView(AuthModelView):
    form_excluded_columns = ['articles']
    create_modal = True
    edit_modal = True


class UserView(AuthModelView):
    can_delete = False
    create_modal = True
    edit_modal = True
    column_exclude_list = ['password_hash']
