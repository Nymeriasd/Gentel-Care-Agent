from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from agent.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)


    from agent.order.routes import orders
    from agent.main.routes import main 


    app.register_blueprint(orders)
    app.register_blueprint(main)

    return app
    