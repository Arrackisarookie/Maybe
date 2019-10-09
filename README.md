## Maybe
*Flask 驱动个人博客，管理员在线增删改*  

---

### Todo

- [x] 文章显示
- [x] 分类，标签
- [x] 后台管理
- [x] about
- [ ] 优化前台页面
- [ ] 在线编辑文档
- [ ] 实时显示文档效果
- [ ] 说说
- [ ] 用户
- [ ] 留言板
- [ ] 文章点赞
- [ ] 文章评论
- [ ] 动态添加标签

---

### Version
#### Version 0.0.6

- 引入 [Flask-Admin](https://github.com/flask-admin/flask-admin) 管理后台，实现在线增删改
- 引入 [Flask-Moment](https://github.com/miguelgrinberg/Flask-Moment) 实现时间本地化
- 优化文章，分类，标签，用户管理
- 更新登录页面样式
- 移除 [Flask-Uploads](https://github.com/maxcountryman/flask-uploads) 取消上传文件功能
- 移除 [Bootstrap-Flask](https://github.com/greyli/bootstrap-flask)
- 移除遗留问题代码

Version 0.0.5  
  
- 引入 MySQL 存储文章，分类，标签，管理员信息
- 文章主体内容以 .md 文件形式存储
- articles 表，存储文章基本信息及文章主体的相对位置(相对于项目)
- users 表，存储管理员用户名及密码
- 标签-文章为多对多关系
- 分类-文章为一对多关系
- 以管理员身份登录后可上传 .md 格式文档，生成 html 网页
- 上传文档时，可为文档添加标签，会自动将新标签更新数据库到中


Version 0.0.4  
  
- 更改上传后的文件名
- 上传后只生成新文件
- 将已生成的 md 移出 source/_article
- 上传后更新 tag，category，index
- 使用 `Flask-WTF`，`Flask-Uploads` 重写表单
- 使用 `Flask-Bootstrap` 渲染表单
- 为上传文件加入 meta 信息(no tag, cate)
  
 Version 0.0.3 
  
- markdown 文件生成 html
- 管理员登录  
- 上传 markdown 文件
  
Version 0.0.2
  
- 增加分类显示
- 重构前端页面
  
 Version 0.0.1  
  
- 纯展示，包括首页和内容页
- 首页显示文章列表，实现分页
- 内容页简单陈列
