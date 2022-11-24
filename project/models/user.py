from extensions import db, ma
from marshmallow import fields, validates_schema, ValidationError, EXCLUDE
from marshmallow.validate import Length

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_json(self):
        return {
        "id":self.id,
        "username":self.username,
        "email":self.email,
        "password": self.password
        }
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class UserSchema(ma.SQLAlchemySchema):

    class Meta:
        unknown = EXCLUDE
    username = fields.Str(required=True)
    email = fields.Email(required=True, validate=Length(max=64))
    password = fields.Str(required=True, validate=Length(min=7, max=50))

    @validates_schema
    def validate_name_length(self, data, **kwargs):
        if len(data["username"]) > 100:
            raise ValidationError("username can't have more than 100 chars")
        elif len(data["username"]) == 0:
            raise ValidationError("username can't be an empty String")

class UserSchemaView(ma.SQLAlchemySchema):

    class Meta:
        unknown = EXCLUDE
    username = fields.Str(required=True)
    email = fields.Email(required=True, validate=Length(max=64))

    @validates_schema
    def validate_name_length(self, data, **kwargs):
        if len(data["username"]) > 100:
            raise ValidationError("username can't have more than 100 chars")
        elif len(data["username"]) == 0:
            raise ValidationError("username can't be an empty String")