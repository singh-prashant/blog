from flask import Flask, g
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_moment import Moment
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from flask_bcrypt import Bcrypt
from flask_restless  import APIManager

application = Flask(__name__)
application.config.from_object(Configuration)
db = SQLAlchemy(application)
migrate = Migrate(application, db)

manager = Manager(application)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(application)
login_manager.login_view = 'login'
bcrypt = Bcrypt(application)

api = APIManager(application, flask_sqlalchemy_db=db)

@application.before_request
def _before_request():
    g.user = current_user
