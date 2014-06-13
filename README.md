simpleshare
===========

A simple file share framework.

Demo: [http://share.phyng.com/](http://share.phyng.com/)

Simple is everything.

##功能
* 拖拽上传文件自动生成分享页面
* 多种格式自动预览

##支持的格式
* Markdown 文件和源代码或者纯文本自动渲染
* 图片/音频/视频自动播放
* PDF 使用浏览器插件自动打开
* doc/ppt/xls(x) 自动使用 Google Doc 预览
* 其他文件自动生成下载链接

##框架
* Flask + sqlite3 + Jinja2
* 可以使用 tornado + nginx 部署
* 前端使用 dropzone.js + pace.js

##安装
* 依赖的 Python 包 `Flask` ，部署 Flask 即可
* tornado + nginx 部署 Flask 参考[http://phyng.com/2014/06/07/nginx-tornado-flask/](http://phyng.com/2014/06/07/nginx-tornado-flask/)

##TODO
* process bar issue
* filedate, filesize

##License

The MIT License (MIT)