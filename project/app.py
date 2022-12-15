from flask import Flask

import views
from extensions import database
from extensions import schema
from extensions import apidocs
from extensions import configuration
from extensions import migrate



def create_app(config_class=configuration.DevelopmentConfig):
    app = Flask(__name__)
    
    configuration.init_app(app, config_class)
    apidocs.init_app(app)
    views.init_app(app)
    database.init_app(app)
    schema.init_app(app)
    migrate.init_app(app)
    
 
    return app