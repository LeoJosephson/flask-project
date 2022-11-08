from flask import Blueprint, jsonify, request, Response, abort
import logging
from marshmallow import ValidationError
from models.review import ReviewSchema, Review
from extensions import db
from ..utils import createValidationErrorMessage
import os
from flasgger import swag_from


reviews = Blueprint('reviews', __name__, url_prefix='/reviews')

path = os.path.realpath(os.path.dirname(__file__))

@reviews.route('/', methods=['POST'])
@swag_from(os.path.join(path, 'docs', 'post_review.yml'))
def create_review():
    """ Create a new review """
    content = request.get_json()

    name = content.get("name")
    description = content.get("description")
    playtime = content.get("playtime")
    rating = content.get("rating")
    game_id = content.get("game_id")
    user_id = content.get("user_id")
    new_review = Review(name=name, description=description, playtime=playtime, rating=rating, game_id=game_id, user_id=user_id)

    review_schema = ReviewSchema()

    try:
        review_schema.load(new_review.to_json()) # Validates the input

        db.session.add(new_review)
        db.session.commit()

        return jsonify({
            "message": "new review inserted",
            "review": review_schema.dump(new_review)
            })
    except ValidationError as e:
        return jsonify(createValidationErrorMessage(e)), 400

@reviews.route('/', methods=['GET'])
@swag_from(os.path.join(path, 'docs', 'get_reviews.yml'))
def get_reviews():
    """Returns all reviews in json format."""
    reviews = Review.query.all()

    game_schema = ReviewSchema(many=True)
    resp = game_schema.dump(reviews)

    return jsonify(
        {"Reviews":resp}
        ), 200


@reviews.route('/<id>', methods=['GET'])
@swag_from(os.path.join(path, 'docs', 'get_review.yml'))
def get_review_by_id(id):
    review = Review.query.get_or_404(id) 
    review_schema = ReviewSchema()
    return jsonify({"review": review_schema.dump(review)})

@reviews.route('/<id>', methods=['PUT'])
@swag_from(os.path.join(path, 'docs', 'update_review.yml'))
def update_review(id):
    review = Review.query.get_or_404(id)
    content = request.get_json()

    name = content.get("name", review.name)
    description = content.get("description", review.description)
    playtime = content.get("playtime", review.playtime)
    rating = content.get("rating", review.rating)
    game_id = content.get("game_id", review.game_id)
    user_id = content.get("user_id", review.user_id)
    
    review_schema = ReviewSchema()
    try:
        result = review_schema.load({
            "name": name,
            "description": description,
            "playtime": playtime,
            "rating": rating,
            "game_id": game_id,
            "user_id": user_id
        })
        review.name = name
        review.description = description
        review.playtime = playtime
        review.rating = rating
        review.game_id = game_id
        review.user_id = user_id
        db.session.commit()

        return jsonify({"review": result})
    except ValidationError as e:
        return jsonify(createValidationErrorMessage(e)), 400
@reviews.route('/<id>', methods=['DELETE'])
@swag_from(os.path.join(path, 'docs', 'delete_review.yml'))
def delete_review_by_id(id):
    reviews = db.session.query(Review).filter(Review.id == id).delete()
    if (reviews == 1):
        db.session.commit()
        logging.info("Successful deletion")
        return jsonify({"message": "Successful deletion"})
    else: 
        logging.error("Review not found")
        return abort(404)
    

