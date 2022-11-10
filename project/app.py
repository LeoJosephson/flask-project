from flask import Flask
from flask_migrate import Migrate
from views.game.api import games
from views.user.api import users
from views.review.api import reviews
from views.category.api import categories
from extensions import db, ma
from flasgger import Swagger

from config import DevelopmentConfig

'''pytest
    pytest coverage
'''


swagger_config = {
    "headers": [
    ],
    "title": "Game api",
    "description": "Api using flask to study",
    "specs": [
        {
            "endpoint": 'APISpecification',
            "route": '/APISpecification',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "specs_route": "/apidocs/",
}

def create_app(config_class=DevelopmentConfig):

    app = Flask(__name__)
    swagger = Swagger(app, config=swagger_config, merge=True, template_file = 'docs/swagger.yaml')
    app.config.from_object(config_class)
    
    app.register_blueprint(games)
    app.register_blueprint(users)
    app.register_blueprint(reviews)
    app.register_blueprint(categories)

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
 
    return app

    