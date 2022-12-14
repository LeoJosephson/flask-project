from flask import Flask
from flask_migrate import Migrate
from flasgger import Swagger
import logging
import os

from views import init_blueprints
from extensions import db, ma
from config import DevelopmentConfig

logging_format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logging_format, level=logging.DEBUG, datefmt='%d-%b-%y %H:%M:%S')
MIGRATION_DIR = os.path.join('project', 'migrations')

def create_app(config_class=DevelopmentConfig):

    app = Flask(__name__)
    swagger = Swagger(app, merge=True, template_file = 'docs/swagger.yaml')
    app.config.from_object(config_class)
    
    init_blueprints(app)

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db, directory="project/migrations", compare_type=True)
 
    return app