from flask import Blueprint, jsonify, request, Response, abort
import logging
from marshmallow import ValidationError
from models.review import ReviewSchema, Review
from extensions import db
from ..utils import createValidationErrorMessage
import os


reviews = Blueprint('reviews', __name__, url_prefix='/reviews')
review_schema = ReviewSchema()

@reviews.route('/', methods=['POST'])
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

    try:
        result = review_schema.load(new_review.to_json()) # Validates the input
        db.session.add(new_review)
        db.session.commit()

        logging.info("Review created - POST /reviews")
        return jsonify({
            "message": "new review inserted",
            "review": result
            })
    except ValidationError as e:
        logging.error("VALIDATION ERROR - POST /reviews")
        return jsonify(createValidationErrorMessage(e)), 400

@reviews.route('/', methods=['GET'])

def get_reviews():
    """Returns all reviews in json format."""
    reviews = Review.query.all()
    game_schema_m = ReviewSchema(many=True)

    return jsonify(
        {"Reviews":game_schema_m.dump(reviews)}
        ), 200

@reviews.route('/<id>', methods=['GET'])
def get_review_by_id(id):
    review = Review.query.get_or_404(id) 
    return jsonify({"review": review_schema.dump(review)})

@reviews.route('/<id>', methods=['PUT'])
def update_review(id):
    review = Review.query.get_or_404(id)
    content = request.get_json()

    review_update = Review(
        name = content.get("name", review.name),
        description = content.get("description", review.description),
        playtime = content.get("playtime", review.playtime),
        rating = content.get("rating", review.rating),
        game_id = content.get("game_id", review.game_id),
        user_id = content.get("user_id", review.user_id)
    )

    try:
        result = review_schema.load(review_update.to_json())
        review.name = review_update.name
        review.description = review_update.description
        review.playtime = review_update.playtime
        review.rating = review_update.rating
        review.game_id = review_update.game_id
        review.user_id = review_update.user_id
        db.session.commit()

        logging.info(f"Successful update - PUT /reviews/{id}")
        return jsonify({"review": result})
    except ValidationError as e:
        logging.error(f"VALIDATION ERROR - PUT /reviews/{id}")
        return jsonify(createValidationErrorMessage(e)), 400

@reviews.route('/<id>', methods=['DELETE'])
def delete_review_by_id(id):
    reviews = db.session.query(Review).filter(Review.id == id).delete()
    if (reviews == 1):
        db.session.commit()
        logging.info(f"Successful deletion - DELETE /reviews/{id}")
        return jsonify({"message": "Successful deletion"})
    else: 
        logging.error(f"Review not found - DELETE /reviews/{id}")
        return abort(404)
    

