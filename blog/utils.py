import os
import shelve

from blog.config import BLOG_DAT


class ImportData(object):
    _data = {}
    data_path = BLOG_DAT
    datafile = os.path.join(data_path, 'blog.dat')

    @classmethod
    def _load_data(cls):
        """载入数据"""
        with shelve.open(cls.datafile) as data:
            for key, value in data.items():
                cls._data[key] = value

            return cls._data

    @classmethod
    def get_data(cls):
        """获取数据"""
        if len(cls._data) == 0:
            cls._load_data()

        return cls._data

    @classmethod
    def reload_data(cls):
        """重新载入数据"""
        cls._load_data()
