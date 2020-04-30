import os
import random



class Config:                       # 基类配置
    string = "".join(random.sample("abcdefghijklmnopqrstuvwxyz", 15))  # 生成随机字符串
    SECRET_KEY = string  # 为应用配置一个密钥，防止表单会话被非法篡
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # 从环境变量中导入
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPFORM_FOLDER = 'G:/flask_og/app/static/upform'
    UPFILE_FOLDER = 'G:/flask_og/app/static/upfile'
    ALLOWED_EXTENSIONS = set(['txt','docx','doc'])
    MAX_CONTENT_LENGTH = 16*1024*1024
    CKEDITOR_FILE_UPLOADER='main.upload'
    CKEDITOR_ENABLE_CSRF=True



class DevelopmentConfig(Config):       # 继承基类配置的内容，并根据具体的生产环境进行不同的配置
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('database')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('database_testing')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('database_production')


config={
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production':ProductionConfig,

    'default':DevelopmentConfig
}