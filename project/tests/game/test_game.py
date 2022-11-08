from models.game import Game, Category
from extensions import db


def test_post_game_with_invalid_category_id(app_with_data):
    category_id_that_does_not_exist = db.session.query(Category).first().id  + 5
    response = app_with_data.post("/games/", json={
        "name": "game_test",
        "category_id": category_id_that_does_not_exist + 1
    })
    assert db.session.query(Game).count() == 1
    assert response.status_code == 400

def test_post_game_with_invalid_name_type(app_with_data):
    category_id = db.session.query(Category).first().id
    response = app_with_data.post("/games/", json={
        "name": 356,
        "category_id": category_id
    })
    assert db.session.query(Game).count() == 1
    assert response.status_code == 400

def test_post_game_with_valid_fields(app_with_data):
    category_id = db.session.query(Category).first().id
    response = app_with_data.post("/games/", json={
        "name": "new_game",
        "category_id": category_id
    })

    assert db.session.query(Game).filter(Game.name == "new_game").first() != None
    assert response.status_code == 200

def test_post_game_with_invalid_name_min_range(app_with_data):
    category_id = db.session.query(Category).first().id
    response = app_with_data.post("/games/", json={
        "name": "",
        "category_id": category_id
    })
    assert response.status_code == 400
    assert db.session.query(Game).count() == 1
    assert "Name can't be an empty String" in response.get_json()["fields"]["_schema"]

def test_post_game_with_invalid_name_max_range(app_with_data):
    category_id = db.session.query(Category).first().id
    response = app_with_data.post("/games/", json={
        "name": "u"*65,
        "category_id": category_id
    })
    assert response.status_code == 400
    assert db.session.query(Game).count() == 1
    assert "Name can't have more than 64 chars" in response.get_json()["fields"]["_schema"]


def test_get_all_games(app_with_data):
    game = db.session.query(Game).first()
    response = app_with_data.get("/games/")
    assert game.name in response.get_json()["games"][0]["name"]
    assert response.status_code == 200

def test_get_game_by_id_without_data(app_with_db):
    response = app_with_db.get("/games/1")

    assert response.status_code == 404

def test_get_game_by_id_with_data(app_with_data):
    game = db.session.query(Game).first()
    response = app_with_data.get(f"/games/{game.id}")
    assert game.name in response.get_json()["game"]["name"]
    assert response.status_code == 200

def test_delete_game_with_invalid_id(app_with_db):
    response = app_with_db.delete("/games/2")
    assert response.status_code == 404

def test_delete_game_with_valid_id(app_with_data):
    game_id = db.session.query(Game).first().id
    response = app_with_data.delete(f"/games/{game_id}")
    assert response.status_code == 200
    assert db.session.query(Game).first() == None

def test_update_game(app_with_data):
    game_id = db.session.query(Game).first().id
    new_name = "testing update"
    response = app_with_data.put(f"/games/{game_id}", json={
        "name": new_name
    })
    game_name = db.session.query(Game).first().name
    assert game_name == new_name
    assert response.status_code == 200

def test_update_game_with_invalid_id(app_with_db):
    new_name = "testing update"
    response = app_with_db.put(f"/games/{1}", json={
        "name": new_name
    })
    assert response.status_code == 404

def test_update_game_with_invalid_fields(app_with_data):
    game = db.session.query(Game).first()
    old_name = game.name
    new_name = 32
    
    response = app_with_data.put(f"/games/{game.id}", json={
        "name": 32,
        "category_id": "error"
    })
    game_name = db.session.query(Game).first().name
    assert old_name == game_name
    assert "Not a valid integer" in response.get_json()["fields"]["category_id"][0]
    assert response.status_code == 400