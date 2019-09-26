# import codecs
# import os
# import shelve

# from blog.config import BLOG_DAT, ARTICLE_PATH


# class ImportData(object):
#     _data = {}
#     data_path = BLOG_DAT
#     datafile = os.path.join(data_path, 'blog.dat')

#     @classmethod
#     def _load_data(cls):
#         """载入数据"""
#         with shelve.open(cls.datafile) as data:
#             for key, value in data.items():
#                 cls._data[key] = value

#             return cls._data

#     @classmethod
#     def get_data(cls):
#         """获取数据"""
#         if len(cls._data) == 0:
#             cls._load_data()

#         return cls._data

#     @classmethod
#     def reload_data(cls):
#         """重新载入数据"""
#         cls._load_data()


# def add_meta(file, data):
#     with codecs.open(file, 'r+', 'utf-8') as f:
#         old = f.read()
#         f.seek(0)
#         for key, value in data.items():
#             if key == 'tag':
#                 f.write('{}: {}\n'.format(key, value[0]))
#                 for t in value[1:]:
#                     f.write('    {}\n'.format(t))
#             else:
#                 f.write('{}: {}\n'.format(key, value))
#         f.write('\n' + old)
