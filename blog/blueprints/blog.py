from flask import Blueprint, current_app, render_template, request

from blog.models import Article, Category, Comment


bp = Blueprint('blog', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    page_num = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_ARTICLE_PER_PAGE']
    page = Article.query.order_by(Article.timestamp.desc()).paginate(
        page_num, per_page, error_out=False)
    articles = page.items
    return render_template('blog/index.html', page=page, articles=articles)


@bp.route('/about')
def about():
    return render_template('blog/about.html')


@bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('blog/category.html', category_id=category_id)


@bp.route('/article/<int:article_id>', methods=['GET', 'POST'])
def article(article_id):
    article = Article.query.get_or_404(article_id)
    comment_page_num = request.args.get('page', 1, type=int)
    comment_per_page = current_app.config['BLOG_COMMENT_PER_PAGE']
    page = Comment.query.with_parent(article).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        comment_page_num, comment_per_page)
    comments = page.items

    return render_template('blog/article.html', article=article, page=page, comments=comments)
