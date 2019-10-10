from flask import redirect, request, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import PasswordField
from wtforms.validators import DataRequired


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


class AboutView(AuthModelView):
    can_view_details = True
    column_list = [
        'title',
        'slogan',
        'url',
        'add_time',
        'update_time',
    ]
    column_sortable_list = [
        'add_time',
        'update_time',
    ]
    column_default_sort = 'id'
    form_excluded_columns = ['add_time', 'update_time']
    form_args = {
        'body': {
            'validators': [DataRequired()]
        },
    }
    form_widget_args = {
        'body': {
            'rows': 10
        },
    }


class CategoryView(AuthModelView):
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['articles']
    column_list = [
        'name',
        'slogan'
    ]
    column_sortable_list = ('id', )


class ArticleView(AuthModelView):
    can_view_details = True
    column_list = [
        'id',
        'title',
        'category',
        'tags',
        'url',
        'add_time',
        'update_time',
    ]
    column_labels = {
        'title': 'Title',
        'tags.name': 'Tags',
    }
    column_sortable_list = [
        'id',
        'add_time',
        'update_time',
    ]
    column_editable_list = ['url', ]
    column_default_sort = 'id'
    form_excluded_columns = ['add_time', 'update_time']
    form_args = {
        'body': {
            'validators': [DataRequired()]
        },
    }
    form_widget_args = {
        'body': {
            'rows': 10
        },
    }
    column_details_list = [
        'id',
        'title',
        'category',
        'tags',
        'url',
        'add_time',
        'update_time',
    ]


class TagView(AuthModelView):
    form_excluded_columns = ['articles']
    create_modal = True
    edit_modal = True
    column_list = [
        'name',
        'slogan'
    ]
    column_sortable_list = ('id', )


class UserView(AuthModelView):
    can_delete = False
    create_modal = True
    edit_modal = True
    column_sortable_list = ('id', )
    column_exclude_list = ['password_hash']
    form_excluded_columns = ['password_hash']
    form_extra_fields = {
        'password': PasswordField('Password')
    }
