from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-recipes.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(120), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    recipes = db.relationship('Recipe', backref='user', lazy=True, cascade='all, delete-orphan')

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hash is not readable")

    @password_hash.setter
    def password_hash(self, value):
        self._password_hash = bcrypt.generate_password_hash(value).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username is required')
        return username

    def __repr__(self):
        return f'<User {self.username}>'


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    serialize_rules = ('-user', '-user_id',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if not instructions or len(instructions) < 50:
            raise ValueError('Instructions must be at least 50 characters long')
        return instructions

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Title is required')
        return title

    def __repr__(self):
        return f'<Recipe {self.title}>'
