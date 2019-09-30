import codecs
import os

from markdown import Markdown


def markdown_to_html(path, name):
    if not name.endswith('.md'):
        name += '.md'
    file = os.path.join(path, name)
    with codecs.open(file, 'r', 'utf-8', 'ignore') as f:
        body = f.read()

        md = Markdown(extensions=[
            'admonition',       # 警告样式
            'codehilite',       # 语法高亮
            'fenced_code',      # 代码不用缩进
            'tables'])          # 表格
        content = md.convert(body)

        return content


def save_html(html, path, name, verifying=False):
    if not os.path.exists(path):
        os.makedirs(path)
    if not name.endswith('.html'):
        name += '.html'
    file = os.path.join(path, name)
    print(file)

    with codecs.open(file, 'w', 'utf-8') as f:
        if verifying:
            f.write('{% extends "admin/verify_article.html" %}\n')
        else:
            f.write('{% extends "blog/article.html" %}\n')

        f.write('{% block article_body %}\n')
        f.write(html + '\n')
        f.write('{% endblock %}\n')
