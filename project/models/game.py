from extensions.database import db
from extensions.schema import ma
from marshmallow import fields, validates_schema, ValidationError, EXCLUDE
from.category import Category

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    reviews = db.relationship('Review', backref='game', lazy=True)

    def __repr__(self):
        return f'<Game {self.name}>'

    def __init__(self,name, category_id):
        self.name = name
        self.category_id = category_id
    
    def to_json(self):
        return {
        "id":self.id,
        "name":self.name,
        "category_id":self.category_id,
        }

class GameSchema(ma.SQLAlchemySchema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True)
    category_id = fields.Int(required=True)

    @validates_schema
    def validate_name_length(self, data, **kwargs):
        if len(data["name"]) > 64:
            raise ValidationError("Name can't have more than 64 chars")
        elif len(data["name"]) == 0:
            raise ValidationError("Name can't be an empty String")

    @validates_schema
    def validate_category_exists(self, data, **kwargs):
        if db.session.query(Category.id).filter_by(id=data["category_id"]).first() is None:
            raise ValidationError("Category does not exists")







