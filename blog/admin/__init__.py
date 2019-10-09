from flask_admin import Admin

from blog.extensions import db
from blog.models import About, Article, Category, Tag, User
from blog.admin.modelviews import (
    IndexView, AboutView, ArticleView, CategoryView, TagView, UserView
)

admin = Admin(
    name='Maybe-Admin',
    index_view=IndexView(),
    template_mode='bootstrap3')


admin.add_view(ArticleView(Article, db.session))
admin.add_view(AboutView(About, db.session))
admin.add_view(CategoryView(Category, db.session))
admin.add_view(TagView(Tag, db.session))
admin.add_view(UserView(User, db.session))
