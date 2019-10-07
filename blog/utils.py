from markdown import Markdown

from blog.models import Tag
from blog.extensions import db


def markdown_to_html(body):
    md = Markdown(extensions=[
        'admonition',       # 警告样式
        'codehilite',       # 语法高亮
        'fenced_code',      # 代码不用缩进
        'tables'])          # 表格
    content = md.convert(body)

    return content


def new_tag(t):
    tag = Tag(name=t)
    db.session.add(tag)
    db.session.commit()
    return tag
