from datetime import datetime
import codecs
import os

from markdown import Markdown


def parse_meta(file, meta):
    now = datetime.now().strftime('%Y-%m-%d')
    date = meta.get('datetime')[0] if meta.get('datetime') else now
    tag = meta.get('tag', '其他')
    category = meta.get('category')[0] if meta.get('category') else '无分类'
    title = meta.get('title')[0] if meta.get('title') else os.path.splitext(os.path.basename(file))[0]
    summary = meta.get('summary')[0] if meta.get('summary') else '无描述'
    url = meta.get('url')[0] if meta.get('url') else str(title)+'.html'

    param = {
        'category': category,
        'datetime': date,
        'summary': summary,
        'tag': tag,
        'title': title,
        'url': url
    }
    return param

def markdown_to_html(file):
    with codecs.open(file, 'r', 'utf-8', 'ignore') as f:
        body = f.read()
        md = Markdown(extensions=[
            'admonition',   # 警告样式
            'codehilite',   # 语法高亮
            'fenced_code',  # 代码不用缩进
            'meta',         # 元信息
            'tables'])      # 表格
        article = md.convert(body)
        meta = md.Meta if hasattr(md, 'Meta') else {}
        param = parse_meta(file, meta)
