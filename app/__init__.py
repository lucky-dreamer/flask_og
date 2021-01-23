from flask_bootstrap import Bootstrap
from flask import Flask
from flask_moment import Moment
from flask_mail import Mail
from config import config
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
bootstrap = Bootstrap()                              # 初始化flask-bootstrap
moment = Moment()
mail = Mail()                  # 此时并没有传入实例，没有真正初始化
csrf=CSRFProtect()                # 在create——app中，先导 入配置，然后再用init方法真正初始化。（延迟初始化）
login_manager=LoginManager()
db = SQLAlchemy()
login_manager.login_view = 'auth.login'
ckeditor=CKEditor()             # 通过延迟初始化，从而使__name__和config name可选，可创造多个app和多种配置环境，动态修改。


def create_app(config_name):  # 此处标记与代码无关，属于面向对象编程的总结
    app = Flask(__name__)   # 传入name后，其实已经把类实例化，此时的对象是实例，不是类。
    app.config.from_object(config[config_name])   #封装：类把所有的方法定义到了内部，从而不用外部写操作来操作数据，从而实现了数据的内部封装。
    mail.init_app(app)  # 子类继承了所有父类的特性，多态：子类既是他自己,又是父类.
    moment.init_app(app)  # 多态的封闭特性：对扩展开放--允许增加父类的子类，
    bootstrap.init_app(app)                # 对修改封闭--不需要修改 操作父类的函数，只要是父类的子类，父类的函数都可以操作。
    login_manager.init_app(app)   # 其余：子类一定是父类，而父类不一定是子类
    db.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    return app
