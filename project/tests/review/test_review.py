from models.game import Game
from models.user import User
from models.review import Review
from extensions import db



def test_create_review(app_with_all_models):
    user_id = User.query.first().id
    game_id = Game.query.first().id

    response = app_with_all_models.post("/reviews/", json={
        "name": "testing review",
        "description": "testing review description",
        "user_id": user_id,
        "game_id": game_id,
        "rating": 10,
        "playtime": 10
    })

    res_js = response.get_json()

    assert response.status_code == 200
    assert res_js["review"]["name"] == "testing review"

def test_create_review_with_invalid_fields(app_with_db):

    response = app_with_db.post("/reviews/", json={
        "name": "testing review",
        "description": "testing review description",
        "user_id": 1,
        "game_id": 1,
        "rating": 10,
        "playtime": 10
    })

    res_js = response.get_json()
    
    assert response.status_code == 400



def test_get_all_reviews(app_with_all_models):
    review = db.session.query(Review).first()
    response = app_with_all_models.get("/reviews/")
    res_js = response.get_json()

    assert response.status_code == 200
    assert res_js["Reviews"][0]["name"] == review.name
    assert res_js["Reviews"][0]["game_id"] == review.game_id

def test_get_review_with_valid_id(app_with_all_models):
    review = db.session.query(Review).first()
    response = app_with_all_models.get(f"/reviews/{review.id}")
    res_js = response.get_json()

    assert response.status_code == 200
    assert res_js["review"]["name"] == review.name

def test_get_review_with_invalid_id(app_with_db):
    response = app_with_db.get("/reviews/1")
    assert response.status_code == 404

def test_update_review_with_valid_fields(app_with_all_models):

    review = db.session.query(Review).first()

    user_id = review.user_id
    game_id = review.game_id
    response = app_with_all_models.put(f"/reviews/{review.id}", json={
        "name": "test-reviews",
        "description": "test-review description",
        "rating": 10,
        "playtime": 100,
        "user_id": user_id,
        "game_id": game_id
    })
    review_new_name = db.session.query(Review).first().name
    assert review_new_name == "test-reviews"
    assert response.status_code == 200

def test_update_review_with_invalid_fields(app_with_all_models):

    review = db.session.query(Review).first()
    response = app_with_all_models.put(f"/reviews/{review.id}", json={
        "name": 50,
        "description": 3,
        "rating": 10,
        "playtime": 100,
    })
    assert "Not a valid string." in response.get_json()["fields"]["name"]
    assert "Not a valid string." in response.get_json()["fields"]["description"]
    assert response.status_code == 400

def test_update_review_with_invalid_relationships(app_with_all_models):

    review = db.session.query(Review).first()
    user_id = review.user_id
    game_id = review.game_id
    response = app_with_all_models.put(f"/reviews/{review.id}", json={
        "name": "testing",
        "description": "testing reviews",
        "rating": 10,
        "playtime": 100,
        'user_id': user_id+2,
        "game_id": game_id+2
    })
    assert "Game does not exists" in response.get_json()["fields"]["_schema"]
    assert "User does not exists" in response.get_json()["fields"]["_schema"]
    assert response.status_code == 400

def test_update_review_with_invalid_id(app_with_all_models):

    review = db.session.query(Review).first()
    response = app_with_all_models.put(f"/reviews/{review.id+2}", json={
        "name": "INVALID Test",
    })
    assert response.status_code == 404

def test_delete_review_with_valid_id(app_with_all_models):
    review = db.session.query(Review).first()
    response = app_with_all_models.delete(f"/reviews/{review.id}")
    assert response.status_code == 200

def test_delete_review_with_invalid_id(app_with_db):
    response = app_with_db.delete(f"/reviews/2")
    assert response.status_code == 404
