from models.category import Category
from extensions import db

def test_post_category_with_valid_fields(app_with_data):
    name = "test_post_category"
    response = app_with_data.post("/categories/", json={
        "name": name,
        "description": "testing_post"
    })
    assert response.status_code == 200
    assert db.session.query(Category).filter(Category.name == name).first() != None

def test_post_category_with_invalid_name_min_range(app_with_db):
    response = app_with_db.post("/categories/", json={
        "name": "",
        "description": "testing_post_invalid"
    })
    assert response.status_code == 400
    assert "Name can't be an empty String" in response.get_json()["fields"]["_schema"]

def test_post_category_with_invalid_name_max_range(app_with_db):
    response = app_with_db.post("/categories/", json={
        "name": "u"*65,
        "description": "testing_post_invalid"
    })
    assert response.status_code == 400
    assert "Name can't have more than 64 chars" in response.get_json()["fields"]["_schema"]


def test_post_category_with_invalid_fields(app_with_data):
    name = 6723
    response = app_with_data.post("/categories/", json={
        "name": name,
        "description": "testing_post_invalid"
    })
    assert response.status_code == 400
    assert db.session.query(Category).filter(Category.description=="testing_post_invalid").first() == None

def test_post_category_without_fields(app_with_db):
    response = app_with_db.post("/categories/")
    assert response.status_code == 400

def test_get_all_categories(app_with_data):
    name = db.session.query(Category).first().name
    response = app_with_data.get("/categories/")
    res = response.get_json()
    assert response.status_code == 200
    assert res["categories"][0]["name"] == name

def test_get_category_with_valid_id(app_with_data):
    category = db.session.query(Category).first()
    response = app_with_data.get(f"/categories/{category.id}")
    assert response.status_code == 200
    assert response.get_json()["category"]["name"] == category.name

def test_get_category_with_invalid_id(app_with_db):
    response = app_with_db.get(f"/categories/1")
    assert response.status_code == 404

def test_delete_category_with_valid_id(app_with_category_model):
    category_id = db.session.query(Category).first().id
    response = app_with_category_model.delete(f"/categories/{category_id}")

    assert response.status_code == 200

def test_delete_category_with_invalid_id(app_with_db):
    response = app_with_db.delete(f"/categories/1")
    assert response.status_code == 404

def test_update_category_with_valid_id(app_with_data):
    category_id = db.session.query(Category).first().id
    response = app_with_data.put(f"/categories/{category_id}",
        json={
            "name":"Test_game_update"
        }
    )
    category_name = db.session.query(Category).filter(Category.name=="Test_game_update").first().name
    assert response.status_code == 200
    assert "Test_game_update" == category_name

def test_update_category_with_invalid_id(app_with_db):
    response = app_with_db.put(f"/categories/2",
        json={
            "name":"Test_game_update"
        }
    )
    assert response.status_code == 404

def test_update_category_with_invalid_fields(app_with_data):
    category = db.session.query(Category).first()
    name = category.name

    response = app_with_data.put(f"/categories/{category.id}",
        json={
            "name": 2
        }
    )
    category_name = db.session.query(Category).first().name
    assert response.status_code == 400
    assert name == category_name
