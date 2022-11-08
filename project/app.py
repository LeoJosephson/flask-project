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

def create_app(config_class=DevelopmentConfig):

    app = Flask(__name__)
    swagger = Swagger(app)
    app.config.from_object(config_class)
    
    app.register_blueprint(games)
    app.register_blueprint(users)
    app.register_blueprint(reviews)
    app.register_blueprint(categories)

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
 
    return app

    '''
    swagger
    https://github.com/rantav/flask-restful-swagger
    https://github.com/DenerRodrigues/flask-restful-api-example/blob/master/api/app.py
    https://editor.swagger.io/
    markdown editor
    '''
    