## Maybe
*Flask 驱动，静态个人博客，支持上传 markdown 文件生成 html*  

---
### Developing
- 优化用户登录
- 上传表单加入 tag, category
- 上传文件生成预览

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

- 在线编辑 markdown
- 优化文件转化过程
- 优化安全措施
- 优化界面
