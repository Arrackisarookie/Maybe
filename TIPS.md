### Tips

1. Sqlalchemy create 建表时，会将第一个不是外键的 Integer 主键列设置为自增。可以通过设置该列的 ``autoincrement=False`` 关闭这一特性