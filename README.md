## Maybe
*Flask 驱动个人博客，支持上传 markdown 文件生成 html*  

---
### Developing
- [x] 启用 MySQL 进行数据管理
- [x] 优化用户登录
- [x] 单元测试
- [x] 数据库版本迁移
- [x] 上传文件后以 .md 后缀保存在 source/
- [x] 文章信息存入数据库
- [x] 添加审核过程
    1. 显示所有文章审核情况，未审核已审核分开显示
    2. 将正在审核的文章由 md 格式生成 html 格式的临时文件
    3. 在网页中显示文章效果
    4. 审核完毕后点击提交会将文章正式生成为 html 格式文件保存在 templates/generated/
- [ ] 重构 blog 蓝图

---
### Version
#### Version 0.0.4

- 更改上传后的文件名
- 上传后只生成新文件
- 将已生成的 md 移出 source/_article
- 上传后更新 tag，category，index
- 使用 Flask-WTF，Flask-Uploads 重写表单
- 使用 Flask-Bootstrap 渲染表单
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

---
### todo

- 加入 tag, category
- 加入 moment
- 在线编辑 markdown
- 优化文件转化过程
- 优化安全措施
- 优化界面
