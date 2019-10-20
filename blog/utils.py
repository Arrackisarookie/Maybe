from markdown import Markdown
import hashlib
import os
import requests
import time
import uuid


def markdown_to_html(body):
    md = Markdown(extensions=[
        'fenced_code',
        'tables'])
    content = md.convert(body)

    return content


class Translator(object):

    url = 'https://openapi.youdao.com/api'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    trans_type = 'v3'

    _trans_key = os.environ['TRANSLATOR_KEY']
    _trans_secret = os.environ['TRANSLATOR_SECRET']

    def __init__(self, src='zh-CHS', dest='en'):
        self.data = {}
        self.data['from'] = src
        self.data['to'] = dest
        self.data['salt'] = str(uuid.uuid1())
        self.data['curtime'] = str(int(time.time()))

        self.data['appKey'] = self._trans_key
        self.data['signType'] = self.trans_type

    def encrypt(self, sign):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(sign.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def truncate(self, query):
        if query is None:
            return None
        size = len(query)
        if size < 21:
            res = query
        else:
            res = str(size).join([query[:10], query[size - 10:]])
        return res

    def translate(self, query):
        self.data['q'] = query

        sign_list = [
            self._trans_key, self.truncate(query), self.data['salt'],
            self.data['curtime'], self._trans_secret]
        sign = ''.join(sign_list)
        self.data['sign'] = self.encrypt(sign)

        response = requests.post(self.url, data=self.data, headers=self.headers)
        return response.json()['translation'][0]
