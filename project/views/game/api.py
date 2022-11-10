from flask import Blueprint, jsonify, request, Response, abort
from marshmallow import ValidationError
from ..utils import createValidationErrorMessage
import logging
from models.game import Game, GameSchema
from extensions import db
import os
games = Blueprint('games', __name__, url_prefix='/games')

logging_format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logging_format, level=logging.DEBUG, datefmt='%d-%b-%y %H:%M:%S')

path = os.path.realpath(os.path.dirname(__file__))
game_schema = GameSchema()

@games.route('/', methods=['POST'])
def create_game():
    """ Create a new game """
    content = request.get_json()

    name = content.get("name")
    category_id = content.get("category_id")
    new_game = Game(name=name, category_id=category_id)

    try:
        game_schema.load(new_game.to_json()) # Validates the input

        db.session.add(new_game)
        db.session.commit()

        return jsonify({
            "message": "new game inserted",
            "game": game_schema.dump(new_game)
            }),200
    except ValidationError as e:
        return jsonify(createValidationErrorMessage(e)), 400
    
@games.route('/', methods=['GET'])
def get_games():
    games = Game.query.all()

    game_schema_m = GameSchema(many=True)

    return jsonify(
        {"games": game_schema_m.dump(games)}
        ), 200
    

@games.route('/<id>', methods=['GET'])
def get_game_by_id(id):
    """Returns a game that has the same input id of <id> in json format"""
    game = Game.query.get_or_404(id)
    return jsonify({"game": game_schema.dump(game)})

@games.route('/<id>', methods=['DELETE'])
def delete_game_by_id(id):
    games = db.session.query(Game).filter(Game.id == id).delete()
    if (games == 1):
        db.session.commit()
        logging.info("Successful deletion")
        return jsonify({"message": "Successful deletion"})
    else: 
        logging.error("Game not found")
        return abort(404)
    
@games.route('/<id>', methods=['PUT'])
def game_update(id):

    game = Game.query.get_or_404(id)
    content = request.get_json()

    name = content.get("name", game.name)
    category_id = content.get("category_id", game.category_id)
    try:
        result = game_schema.load(
            {"name": name,
            "category_id": category_id}
        )
        game.name = name
        game.category_id = category_id
        db.session.commit()

        return jsonify({"game": result})
    except ValidationError as e:
        logging.error("Game update validation error")
        return jsonify(createValidationErrorMessage(e)), 400


