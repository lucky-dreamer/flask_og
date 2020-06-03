from flask import render_template
from . import main

# @main.errorhandler(500)
# def internal_sever_error(e):
#     return '<h1>服务器异常</h1>', 500
#
#
# @main.errorhandler(404)
# def page_not_found():
#     return '<h1>访问页面未知</h1>', 404
#
# @main.errorhandler(413)
# def page_not_found():
#     return '<h1>上传文件过大</h1>', 413