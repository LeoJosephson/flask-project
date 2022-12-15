import pytest

from app import create_app
from extensions.database import db
from models.category import Category
from models.game import Game
from models.user import User
from models.review import Review
from sqlalchemy import delete
from extensions import configuration

@pytest.fixture(scope="session")
def flask_app():
    app = create_app(configuration.TestingConfig)

    client =app.test_client()

    context = app.test_request_context()
    context.push()

    yield client

    context.pop()

@pytest.fixture(scope="session")
def app_with_db(flask_app):
    db.create_all()

    yield flask_app

    db.session.commit()
    db.drop_all()


@pytest.fixture
def app_with_data(app_with_db):
    category = Category(name="RTS", description="Real-Time Strategy")
    db.session.add(category)

    cat_id = db.session.query(Category).first().id
    game = Game(name="AOE", category_id=cat_id)
    db.session.add(game)

    db.session.commit()

    yield app_with_db

    db.session.execute(delete(Game))
    db.session.execute(delete(Category))
    db.session.commit()

@pytest.fixture
def app_with_category_model(app_with_db):
    category = Category(name="RTS", description="Real-Time Strategy")
    db.session.add(category)

    db.session.commit()

    yield app_with_db

    db.session.execute(delete(Category))
    db.session.commit()

@pytest.fixture
def app_with_all_models(app_with_db):
    category = Category(name="RTS", description="Real-Time Strategy")
    db.session.add(category)

    cat_id = db.session.query(Category).first().id
    game = Game(name="AOE", category_id=cat_id)
    db.session.add(game)

    user = User(username="UserTest", email="test@test@email.com", password="12345678")
    db.session.add(user)
    game_id = db.session.query(Game).first().id
    user_id = db.session.query(User).first().id

    review = Review(name="ReviewTest", description="ReviewTestDescription", playtime=10, rating=5, 
    user_id=user_id, game_id=game_id)
    db.session.add(review)


    db.session.commit()

    yield app_with_db

    db.session.execute(delete(Review))
    db.session.execute(delete(Game))
    db.session.execute(delete(User))
    db.session.execute(delete(Category))
    db.session.commit()
