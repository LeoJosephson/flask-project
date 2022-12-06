from models.game import Game, Category
from views.game.api import get_games, get_game_by_id
from mock import patch
from extensions import db
        
@patch('flask_sqlalchemy.model._QueryProperty.__get__')
def test_get_all_games_mock(queryMock):
    #setup
    test_game1 = Game(name="mock game1", category_id=1)
    test_game2 = Game(name="mock game2", category_id=2)
    queryMock.return_value.all.return_value = [test_game1, test_game2]

    games = get_games()
    response = games[0].get_json()

    assert response["games"][0]["name"] == test_game1.name
    assert response["games"][1]["name"] == test_game2.name

@patch('flask_sqlalchemy.model._QueryProperty.__get__')
def test_get_game_by_id_mock(queryMock):

    test_game1 = Game(name="mock game1", category_id=1)
    queryMock.return_value.get_or_404.return_value = test_game1

    game = get_game_by_id(1)
    response = game.get_json()["game"]

    assert response["name"] == test_game1.name
    assert response["category_id"] == test_game1.category_id
    

def test_post_game_with_invalid_category_id(app_with_data):
    response = app_with_data.post("/games/", json={
        "name": "game_test",
        "category_id": db.session.query(Category).first().id  + 4 # dont exist
    })
    assert db.session.query(Game).count() == 1
    assert response.status_code == 400

def test_post_game_with_invalid_name_type(app_with_data):
    response = app_with_data.post("/games/", json={
        "name": 356,
        "category_id": db.session.query(Category).first().id
    })
    assert db.session.query(Game).count() == 1
    assert response.status_code == 400

def test_post_game_with_valid_fields(app_with_data):
    response = app_with_data.post("/games/", json={
        "name": "new_game",
        "category_id": db.session.query(Category).first().id
    })

    assert db.session.query(Game).filter(Game.name == "new_game").first() != None
    assert response.status_code == 200

def test_post_game_with_invalid_name_min_range(app_with_data):
    response = app_with_data.post("/games/", json={
        "name": "",
        "category_id": db.session.query(Category).first().id
    })
    assert response.status_code == 400
    assert db.session.query(Game).count() == 1
    assert "Name can't be an empty String" in response.get_json()["fields"]["_schema"]

def test_post_game_with_invalid_name_max_range(app_with_data):
    response = app_with_data.post("/games/", json={
        "name": "u"*65,
        "category_id": db.session.query(Category).first().id
    })
    assert response.status_code == 400
    assert db.session.query(Game).count() == 1
    assert "Name can't have more than 64 chars" in response.get_json()["fields"]["_schema"]

def test_get_all_games(app_with_data):
    response = app_with_data.get("/games/")
    assert db.session.query(Game).first().name in response.get_json()["games"][0]["name"]
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
    response = app_with_db.put(f"/games/{1}", json={
        "name": "testing update"
    })
    assert response.status_code == 404

def test_update_game_with_invalid_fields(app_with_data):
    game = db.session.query(Game).first()
    old_name = game.name
    
    response = app_with_data.put(f"/games/{game.id}", json={
        "name": 32,
        "category_id": "error"
    })
    game_name = db.session.query(Game).first().name
    assert old_name == game_name
    assert "Not a valid integer" in response.get_json()["fields"]["category_id"][0]
    assert response.status_code == 400