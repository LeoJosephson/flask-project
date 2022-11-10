from flask import Blueprint, jsonify, request, abort
from marshmallow import ValidationError
import logging
from models.category import CategorySchema, Category
from extensions import db
from ..utils import createValidationErrorMessage
import os


categories = Blueprint('categories', __name__, url_prefix='/categories')

logging_format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logging_format, level=logging.DEBUG, datefmt='%d-%b-%y %H:%M:%S')

category_schema = CategorySchema()
path = os.path.realpath(os.path.dirname(__file__))

@categories.route('/', methods=['POST'])
def create_category():
    """ Create a new category """
    content = request.get_json()
    new_category = Category(
        name = content.get("name"),
        description = content.get("description")
    )

    try:
        category_schema.load(new_category.to_json()) # Validates the input

        db.session.add(new_category)
        db.session.commit()

        return jsonify({
            "message": "new category inserted",
            "category": category_schema.dump(new_category)
            }, 200)
    except ValidationError as e:
        return jsonify(createValidationErrorMessage(e)), 400

    
@categories.route('/', methods=['GET'])
def get_categories():
    """Returns all categories in json format."""
    categories = Category.query.all()

    category_schema_m = CategorySchema(many=True)

    return jsonify(
        {"categories":category_schema_m.dump(categories)}
        ), 200

@categories.route('/<id>', methods=['GET'])
def get_category_by_id(id):
    """Returns a game that has the same input id of <id> in json format"""
    category = Category.query.get_or_404(id) 
    return jsonify({"category": category_schema.dump(category)})

@categories.route('/<id>', methods=['DELETE'])
def delete_category_by_id(id):
    """ Delete a game that has the same input id of <id> """
    category = db.session.query(Category).filter(Category.id == id).delete()
    if (category == 1):
        db.session.commit()
        logging.info("Successful deletion")
        return jsonify({"message": "Successful deletion"}), 200
    else: 
        logging.error("Category not found")
        return abort(404)
    
@categories.route('/<id>', methods=['PUT'])
def category_update(id):
    category = Category.query.get_or_404(id)
    content = request.get_json()

    name = content.get("name", category.name)
    description = content.get("description", category.description)

    try:
        result = category_schema.load({
            "name": name,
            "description": description
        })
        category.name = name
        category.description = description
        db.session.commit()

        return jsonify({"category": result})
    except ValidationError as e:
        return jsonify(createValidationErrorMessage(e)), 400
    