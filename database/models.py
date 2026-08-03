# database/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    results = db.relationship('Result', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    skin_tone = db.Column(db.String(50), nullable=False)
    undertone = db.Column(db.String(50), nullable=False)
    undertone_description = db.Column(db.String(255))
    hex_colour = db.Column(db.String(10), nullable=False)
    image_path = db.Column(db.String(255))

    # Relationship to recommendations
    recommendations = db.relationship(
        'Recommendation', backref='result', lazy=True
    )

    def get_makeup(self):
        """Return makeup recommendations grouped by subcategory."""
        items = Recommendation.query.filter_by(
            result_id=self.id, category='makeup'
        ).all()
        grouped = {}
        for item in items:
            if item.subcategory not in grouped:
                grouped[item.subcategory] = []
            grouped[item.subcategory].append(item.colour_name)
        return grouped

    def get_clothing(self):
        """Return clothing colour list."""
        items = Recommendation.query.filter_by(
            result_id=self.id, category='clothing'
        ).all()
        return [item.colour_name for item in items]

    def get_hair(self):
        """Return hair colour list."""
        items = Recommendation.query.filter_by(
            result_id=self.id, category='hair'
        ).all()
        return [item.colour_name for item in items]

    def __repr__(self):
        return f'<Result {self.id} - {self.skin_tone}>'


class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(
        db.Integer, db.ForeignKey('results.id'), nullable=False
    )
    category = db.Column(db.String(20), nullable=False)
    subcategory = db.Column(db.String(50))
    colour_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Recommendation {self.category} - {self.colour_name}>'