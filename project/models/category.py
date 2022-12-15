from extensions.database import db
from extensions.schema import ma
from marshmallow import fields, validates_schema, ValidationError, EXCLUDE

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String, nullable=True)
    games = db.relationship('Game', backref='category', lazy=True)

    def __init__(self,name, description):
        self.name = name
        self.description = description
    
    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "description":self.description,
        }

    def __repr__(self):
        return f'<Category {self.name}>'

class CategorySchema(ma.SQLAlchemySchema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True)
    description = fields.Str(required=True)

    @validates_schema
    def validate_name_length(self, data, **kwargs):
        if len(data["name"]) > 64:
            raise ValidationError("Name can't have more than 64 chars")
        elif len(data["name"]) == 0:
            raise ValidationError("Name can't be an empty String")