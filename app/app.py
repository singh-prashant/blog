from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_sqlalchemy import SQLAlchemy
from config import Configuration


application = Flask(__name__)
application.config.from_object(Configuration)
db = SQLAlchemy(application)
migrate = Migrate(application, db)

manager = Manager(application)
manager.add_command('db',MigrateCommand)
