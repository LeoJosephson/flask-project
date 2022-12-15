from flask import Flask
from flask_migrate import Migrate
import logging
import os

import views
from extensions import database
from extensions import schema
from extensions import apidocs
from config import DevelopmentConfig

logging_format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logging_format, level=logging.DEBUG, datefmt='%d-%b-%y %H:%M:%S')
MIGRATION_DIR = os.path.join('project', 'migrations')

def create_app(config_class=DevelopmentConfig):

    app = Flask(__name__)
    
    app.config.from_object(config_class)

    apidocs.init_app(app)
    views.init_app(app)
    database.init_app(app)
    schema.init_app(app)

    migrate = Migrate(app, database.db, directory="project/migrations", compare_type=True)
 
    return app