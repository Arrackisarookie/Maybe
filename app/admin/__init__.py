from flask_admin import Admin

from app.extensions import db
from app.models.article import Article, Category, Tag
from app.models.others import About, Talk, Top
from app.models.user import User
from app.admin.modelviews import (
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
