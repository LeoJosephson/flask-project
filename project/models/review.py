from extensions.database import db
from extensions.schema import ma
from marshmallow import fields, validates_schema, ValidationError, EXCLUDE
from marshmallow.validate import Range, Length
from .user import User
from .game import Game


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String, nullable=True)
    playtime = db.Column(db.Float(precision=2), nullable=True, default=0)
    rating = db.Column(db.Float(precision=2), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    
    def __init__(self,name, description, playtime, rating, game_id, user_id):
        self.name = name
        self.description = description
        self.playtime = playtime
        self.rating = rating
        self.game_id = game_id
        self.user_id = user_id

    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "playtime": self.playtime,
            "rating": self.rating,
            "game_id": self.game_id,
            "user_id": self.user_id
        }

class ReviewSchema(ma.SQLAlchemySchema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True, validate=Length(min=3, max=64))
    description = fields.Str(required=True)
    playtime = fields.Float(required=True, validate=Range(min=0.1))
    rating = fields.Float(required= True, validate=Range(min=0, max=10))
    game_id = fields.Int(required = True)
    user_id = fields.Int(required = True)


    @validates_schema
    def validate_game_exists(self, data, **kwargs):
        if db.session.query(Game.id).filter_by(id=data["game_id"]).first() is None:
            raise ValidationError("Game does not exists")

    @validates_schema
    def validate_user_exists(self, data, **kwargs):
        if db.session.query(User.id).filter_by(id=data["user_id"]).first() is None:
            raise ValidationError("User does not exists")