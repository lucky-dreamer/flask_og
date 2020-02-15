from flask_bootstrap import Bootstrap
from flask import Flask
from flask_moment import Moment
from flask_mail import Mail
from config import config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
bootstrap = Bootstrap()                              # 初始化flask-bootstrap
moment = Moment()
mail = Mail()
login_manager=LoginManager()
db = SQLAlchemy()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    mail.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    return app
