from flask import Blueprint, render_template


bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    return render_template('blog/index.html')


@bp.route('/about')
def about():
    return render_template('blog/about.html')


@bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('blog/category.html')


@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    return render_template('blog/post.html')
