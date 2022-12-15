from .game.api import games
from .user.api import users
from .review.api import reviews
from .category.api import categories

def init_app(app):
    with app.app_context():
        app.register_blueprint(games)
        app.register_blueprint(users)
        app.register_blueprint(reviews)
        app.register_blueprint(categories)