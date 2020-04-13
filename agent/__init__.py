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

    from agent.services.routes import services
    from agent.role.routes import role
    from agent.users.routes import users
    from agent.farmer.routes import farmer 
    from agent.agent.routes import agent
    from agent.status.routes import status
    from agent.order.routes import orders
    from agent.condition.routes import condition
    from agent.order_status.routes import order_status
    from agent.priority.routes import priority
    from agent.extraservices.routes import extraservices
    from agent.time.routes import time 
    from agent.ordercleaning.routes import ordercleaning 
    from agent.agent_login.routes import agent_login 
    from agent.main.routes import main 

    app.register_blueprint(services)
    app.register_blueprint(role)
    app.register_blueprint(users)
    app.register_blueprint(farmer)
    app.register_blueprint(agent)
    app.register_blueprint(status)
    app.register_blueprint(orders)
    app.register_blueprint(condition)
    app.register_blueprint(order_status)
    app.register_blueprint(priority)
    app.register_blueprint(extraservices)
    app.register_blueprint(time)
    app.register_blueprint(ordercleaning)
    app.register_blueprint(agent_login)
    app.register_blueprint(main)

    return app
    