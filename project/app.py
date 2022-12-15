from flask import Flask
from flask_migrate import Migrate
import os

import views
from extensions import database
from extensions import schema
from extensions import apidocs
from extensions import configuration

MIGRATION_DIR = os.path.join('project', 'migrations')

def create_app(config_class=configuration.DevelopmentConfig):
    app = Flask(__name__)
    
    configuration.init_app(app, config_class)
    apidocs.init_app(app)
    views.init_app(app)
    database.init_app(app)
    schema.init_app(app)

    migrate = Migrate(app, database.db, directory="project/migrations", compare_type=True)
 
    return app