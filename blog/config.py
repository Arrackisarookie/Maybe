import os


SITE_TITLE = '也许'
SITE_SUBTITLE = 'Everything is not too late.'

ARTICLE_PATH = './source/_article/'
PAGE_PATH = './source/_page/'
GENERATED_PATH = './static/generated/'

DEFAULT_CATEGORY = '未分类'
DEFAULT_TAG = ['其他']

BLOG_DAT = './static/generated/data.dat'


ADMIN_USERNAME = os.getenv('ADMIN_USERNAME') or 'Maybe'
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD') or 'whosyourdaddy'
