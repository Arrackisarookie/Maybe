## [Blog](https://Arrack.pythonanywhere.com)
*一个简单的博客，由 Flask 驱动*

---
### 版本
#### Version 0.0.1

- 纯展示，包括首页和内容页
- 首页显示文章列表，实现分页
- 内容页简单陈列

### 踩坑
- 第一坑、Flask 程序发现机制

    当执行 flask run (或由 click 自定义的指令) 时，Flask 会默认寻找名为 app.py 或 wsgi.py 的文件，将它作为程序入口。  

    如果想使用其他文件作为程序入口，则需要设置系统环境变量 FLASK_APP 来告诉 Flask 哪个是入口。  

    **根据给定的参数，Flask 会寻找一个名为 app 或者 application 的应用实例。 如果找不到会继续寻找任意应用实例。如果找不到任何实例，会接着寻找名为 create_app 或者 make_app 的函数，使用该函数返回的实例。**  

    环境变量设置见[官方文档](https://dormousehole.readthedocs.io/en/latest/cli.html)

    **！！！ 注意 ！！！**  
    如果后来加上了 app.py 或 wsgi.py 之后，千万要记得将原来设置的 FLASK_APP 环境变量删掉！！不然每次启动可能都不是你想要的那种方式。  

  
- 第二坑、python-dotenv

    flask 会根据 .env 和 .flaskenv 中配置来设置环境变量。  

    **命令行设置的变量会重载 .env 中的变量， .env 中的变量会重载 .flaskenv 中的变量。**  

    flaskenv 应当用于公共变量，如 FLASK_APP 而 .env 则应用用于私有变量，并且不提交到储存库。  

    这些文件只能由``flask``命令或调用 run() 加载。  
    *如果想在生产运 行时加载这些文件，应该手动调用 load_dotenv() 。*  

- 第三坑、在 pythonanywhere.com 部署

    1. 关于数据库  
    pythonanywhere 中的 MySQL 数据库都是形如 Arrack$blog，  
    即 用户名$数据库名  

    pythonanywhere 中的 MySQL host 名都形如 Arrack.mysql.pythonanywhere-services.com  
    即 用户名.mysql.pythonanywhere-services.com
  
    2. 关于 SECRET_KEY  
    production 模式时，SECRET_KEY 尽量设置为随机密码，可由 Python 的 uuid.uuid4().hex 生成，然后以 SECRET_KEY=刚刚生成的密码 的形式放在 .env 中即可
