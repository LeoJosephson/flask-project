from extensions import db
from models.user import User

def test_post_user_with_valid_fields(app_with_db):

    response = app_with_db.post("/users/", json={
        "username": "test",
        "password": "password",
        "email": "email@email.com"
    })

    user = db.session.query(User).first()
    assert user != None
    assert user.password == "password"
    assert user.username == "test"
    assert user.email == "email@email.com"

def test_post_user_with_invalid_username_max_range(app_with_db):

    response = app_with_db.post("/users/", json={
        "username": "t"*101,
        "password": "password",
        "email": "email@email.com"
    })

    assert "username can't have more than 100 chars" in response.get_json()["fields"]["_schema"]

def test_post_user_with_invalid_username_min_range(app_with_db):

    response = app_with_db.post("/users/", json={
        "username": "",
        "password": "password",
        "email": "email@email.com"
    })

    assert "username can't be an empty String" in response.get_json()["fields"]["_schema"]

def test_post_user_with_invalid_email(app_with_db):

    response = app_with_db.post("/users/", json={
        "username": "leonardo",
        "password": "password",
        "email": "email.com"
    })

    assert "Not a valid email address." in response.get_json()["fields"]["email"]

def test_post_user_without_required_fields(app_with_db):

    response = app_with_db.post("/users/", json={
    })

    assert "Field may not be null." in response.get_json()["fields"]["email"]
    assert "Field may not be null." in response.get_json()["fields"]["password"]
    assert "Field may not be null." in response.get_json()["fields"]["username"]