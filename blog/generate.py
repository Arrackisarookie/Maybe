from datetime import datetime
import codecs
import os
import shelve
import shutil

from markdown import Markdown
from jinja2 import Environment, PackageLoader

from blog.config import (
    BLOG_DAT, GENERATED_PATH, PAGE_PATH, ARTICLE_PATH, SITE_TITLE, SITE_SUBTITLE, FINISHED_PATH
)
from blog.utils import ImportData


class Generate(object):
    def __init__(self):
        self._generated_folder = GENERATED_PATH
        self._article_folder = ARTICLE_PATH
        self._page_folder = PAGE_PATH
        self._env = Environment(loader=PackageLoader('blog', 'templates'))

        self._articles = {}
        self._tags = {}
        self._categories = {}

    def dump_data(self):
        data_path = BLOG_DAT
        if not os.path.exists(os.path.dirname(data_path)):
            os.makedirs(data_path)
        file = os.path.join(data_path, 'blog.dat')
        with shelve.open(file, writeback=True) as dat:

            self.update_data(dat, 'articles_data', self._articles)
            self.update_data(dat, 'categories_data', self._categories)
            self.update_data(dat, 'tags_data', self._tags)

    def update_data(self, dat, key, value):
        if key in dat:
            temp = dat[key].copy()
            temp.update(value)
            dat[key] = temp
        else:
            dat[key] = value

    def render_tag_articles(self):
        template = self._env.get_template('blog/tag.html')
        for tag, articles in self._tags.items():
            tag_articles = []
            for identifier in articles:
                tag_articles.append(self._articles[identifier])
                html = template.render(
                    articles=tag_articles,
                    tag=tag
                )
                self.save_page(tag + '.html', html, 'tag')

    def render_cate_articles(self):
        template = self._env.get_template('blog/category.html')
        for category, articles in self._categories.items():
            cate_articles = []
            for identifier in articles:
                cate_articles.append(self._articles[identifier])
                html = template.render(
                    articles=cate_articles,
                    category=category
                )
                self.save_page(category + '.html', html, 'category')

    def render_index(self):
        template = self._env.get_template('blog/index.html')
        html = template.render(
            articles=self._articles.values(),
            header_title=SITE_TITLE,
            header_subtitle=SITE_SUBTITLE
        )
        self.save_page('index.html', html)

    def render_about(self):
        filename = os.path.join(self._page_folder, 'about.md')
        content, data = self.parse_markdown(filename)
        self.move_generated_md(filename)
        template = self._env.get_template('blog/about.html')
        html = template.render(
            content=content,
            data=data,
            title='关于'
        )
        self.save_page('about.html', html)

    def render_tags(self):
        template = self._env.get_template('blog/tags.html')
        html = template.render(
            tags=self._tags,
            title='标签'
        )
        self.save_page('tags.html', html)

    def render_categories(self):
        template = self._env.get_template('blog/categories.html')
        html = template.render(
            categories=self._categories.keys(),
            title='分类'
        )
        self.save_page('categories.html', html)

    def update_tags(self, identifier, tag):
        for t in tag:
            if t in self._tags:
                self._tags[t].append(identifier)
            else:
                self._tags[t] = [identifier]

    def update_categories(self, identifier, category):
        if category in self._categories:
            self._categories[category].append(identifier)
        else:
            self._categories[category] = [identifier]

    def parse_meta(self, meta):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date = meta.get('datetime')[0] if meta.get('datetime') else now
        tag = meta.get('tag', ['其他'])
        category = meta.get('category')[0] if meta.get('category') else '无分类'
        title = meta.get('title')[0] if meta.get('title') else now
        summary = meta.get('summary')[0] if meta.get('summary') else '无描述'
        url = meta.get('url')[0] if meta.get('url') else title.replace(' ', '-').lower()
        url_prefix = '/'.join(date.split('-')[:2])

        data = {
            'title': title,
            'tag': tag,
            'category': category,
            'datetime': date,
            'summary': summary,
            'url': url,
            'url_prefix': url_prefix
        }
        return data

    def parse_markdown(self, filename):
        with codecs.open(filename, 'r', 'utf-8', 'ignore') as f:
            body = f.read()

            md = Markdown(extensions=[
                'admonition',       # 警告样式
                'codehilite',       # 语法高亮
                'fenced_code',      # 代码不用缩进
                'meta',             # 元信息
                'tables'])          # 表格
            article = md.convert(body)

            # meta 为 dict 类型
            # 其中 key   为 ':' 前的值，类型 str
            #      value 为 ':' 后的值，类型 list
            meta = md.Meta if hasattr(md, 'Meta') else {}
            data = self.parse_meta(meta)
            return article, data

    def markdown_to_html(self, filename):
        article, data = self.parse_markdown(filename)

        # md 文件名为上传时间，可作为识别码 如，190922112323.md
        identifier = os.path.splitext(os.path.basename(filename))[0]

        self._articles[identifier] = data

        self.update_tags(identifier, data['tag'])
        self.update_categories(identifier, data['category'])

        template = self._env.get_template('blog/article.html')
        html = template.render(
            article=article,
            data=data,
        )

        return html

    def save_page(self, basename, html, extra_path=None):

        path = os.path.join('page', extra_path) if extra_path else 'page'

        gen_addr = os.path.join(self._generated_folder, path)
        htmlfile = os.path.join(gen_addr, basename)

        if not os.path.exists(gen_addr):
            os.makedirs(gen_addr)

        with codecs.open(htmlfile, 'w', 'utf-8') as f:
            f.write(html)

    def save_article(self, basename, html):
        # md 文件名为上传时间，可作为识别码
        identifier = os.path.splitext(basename)[0]

        path = os.path.join('article', self._articles[identifier]['url_prefix'])
        gen_addr = os.path.join(self._generated_folder, path)
        gen_name = self._articles[identifier]['url'] + '.html'

        htmlfile = os.path.join(gen_addr, gen_name)

        if not os.path.exists(gen_addr):
            os.makedirs(gen_addr)

        with codecs.open(htmlfile, 'w', 'utf-8') as f:
            f.write(html)

    def load_folder(self, folder):
        for root, dirs, files in os.walk(folder):
            for file in files:
                if os.path.splitext(file)[1].lower() == '.md':
                    md = os.path.join(root, file)
                    yield md

    def generate_article(self):
        for filename in self.load_folder(self._article_folder):
            html = self.markdown_to_html(filename)

            # 将已转换的 markdown 文件移除资源目录
            self.move_generated_md(filename)

            # md 文件名为上传时间，可作为识别码
            self.save_article(os.path.basename(filename), html)
        # 如果 PAGE_PATH 有文章
        if os.listdir(PAGE_PATH):
            self.render_about()

    def generate_page(self):
        self.render_index()
        self.render_tags()
        self.render_categories()
        self.render_tag_articles()
        self.render_cate_articles()

    def move_generated_md(self, filename):
        if not os.path.exists(FINISHED_PATH):
            os.makedirs(FINISHED_PATH)
        shutil.move(filename, FINISHED_PATH)

    def main(self):
        # 如果 ARTICLE_PATH 有文章
        if os.listdir(ARTICLE_PATH):
            self.generate_article()
            self.dump_data()
        data = ImportData.get_data()
        self._articles = data['articles_data']
        self._categories = data['categories_data']
        self._tags = data['tags_data']
        self.generate_page()

    def __call__(self):
        self.main()
